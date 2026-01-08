"""
Robokassa Payment Handler

Complete implementation for Robokassa payment gateway integration.
Handles payment initialization, verification, and callback processing.
"""

import hashlib
import logging
from typing import Dict, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from urllib.parse import urlencode

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class RobokassaEnvironment(Enum):
    """Robokassa environment types."""
    PRODUCTION = "https://auth.robokassa.ru/Merchant/PaymentMethods/"
    SANDBOX = "https://test.robokassa.ru/Merchant/PaymentMethods/"


class RobokassaCurrency(Enum):
    """Supported currencies."""
    RUB = "RUB"  # Russian Ruble (default)
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro
    BYN = "BYN"  # Belarusian Ruble


class PaymentStatus(Enum):
    """Payment status codes."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


@dataclass
class RobokassaConfig:
    """Configuration for Robokassa payment handler."""
    merchant_login: str
    password1: str
    password2: str
    test_password1: Optional[str] = None
    test_password2: Optional[str] = None
    use_sandbox: bool = False
    timeout: int = 30
    
    def get_environment_url(self) -> str:
        """Get the appropriate environment URL."""
        if self.use_sandbox:
            return RobokassaEnvironment.SANDBOX.value
        return RobokassaEnvironment.PRODUCTION.value
    
    def get_password1(self) -> str:
        """Get password1 for current environment."""
        if self.use_sandbox and self.test_password1:
            return self.test_password1
        return self.password1
    
    def get_password2(self) -> str:
        """Get password2 for current environment."""
        if self.use_sandbox and self.test_password2:
            return self.test_password2
        return self.password2


@dataclass
class PaymentRequest:
    """Payment request data."""
    merchant_login: str
    sum_amount: float
    inv_id: str
    description: str
    currency: str = RobokassaCurrency.RUB.value
    email: Optional[str] = None
    is_test: int = 0
    receipt_only: int = 0
    
    def __post_init__(self):
        """Validate payment request data."""
        if self.sum_amount <= 0:
            raise ValueError("Payment amount must be positive")
        if not self.inv_id:
            raise ValueError("Invoice ID is required")
        if not self.merchant_login:
            raise ValueError("Merchant login is required")


class RobokassaSignatureValidator:
    """Validates Robokassa payment signatures."""
    
    @staticmethod
    def calculate_signature(
        merchant_login: str,
        amount: float,
        invoice_id: str,
        password: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Calculate signature for payment verification.
        
        Format: MD5(MerchantLogin:Sum:InvId:Password[:Param1_value[:Param2_value...]])
        
        Args:
            merchant_login: Merchant login
            amount: Payment amount
            invoice_id: Invoice ID
            password: Password for signature
            extra_params: Additional parameters for signature
        
        Returns:
            MD5 hash signature
        """
        signature_parts = [merchant_login, str(amount), str(invoice_id), password]
        
        if extra_params:
            for key in sorted(extra_params.keys()):
                signature_parts.append(str(extra_params[key]))
        
        signature_string = ":".join(signature_parts)
        return hashlib.md5(signature_string.encode()).hexdigest()
    
    @staticmethod
    def verify_callback_signature(
        merchant_login: str,
        amount: float,
        invoice_id: str,
        signature: str,
        password: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Verify callback signature from Robokassa.
        
        Args:
            merchant_login: Merchant login
            amount: Payment amount
            invoice_id: Invoice ID
            signature: Signature from callback
            password: Password for signature
            extra_params: Additional parameters
        
        Returns:
            True if signature is valid, False otherwise
        """
        calculated_signature = RobokassaSignatureValidator.calculate_signature(
            merchant_login, amount, invoice_id, password, extra_params
        )
        return calculated_signature.lower() == signature.lower()


class RobokassaPaymentHandler:
    """
    Robokassa payment gateway handler.
    
    Handles payment initialization, URL generation, and callback verification.
    """
    
    def __init__(self, config: RobokassaConfig):
        """
        Initialize Robokassa payment handler.
        
        Args:
            config: RobokassaConfig instance
        """
        self.config = config
        self.signature_validator = RobokassaSignatureValidator()
        self.session = requests.Session()
        self.session.timeout = config.timeout
    
    def get_payment_url(
        self,
        amount: float,
        invoice_id: str,
        description: str,
        currency: str = RobokassaCurrency.RUB.value,
        email: Optional[str] = None,
        is_test: int = 0,
        extra_params: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Generate payment URL for redirect.
        
        Args:
            amount: Payment amount
            invoice_id: Unique invoice ID
            description: Payment description
            currency: Currency code
            email: Customer email
            is_test: Test mode flag (0 or 1)
            extra_params: Additional parameters to pass
        
        Returns:
            Complete payment URL for redirect
        
        Raises:
            ValueError: If parameters are invalid
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not invoice_id:
            raise ValueError("Invoice ID is required")
        
        # Prepare signature parameters
        signature_params = extra_params.copy() if extra_params else {}
        
        # Calculate signature
        signature = self.signature_validator.calculate_signature(
            self.config.merchant_login,
            amount,
            invoice_id,
            self.config.get_password1(),
            signature_params
        )
        
        # Build URL parameters
        url_params = {
            'MerchantLogin': self.config.merchant_login,
            'Sum': amount,
            'InvId': invoice_id,
            'Description': description,
            'SignatureValue': signature,
            'IsTest': is_test,
        }
        
        if currency != RobokassaCurrency.RUB.value:
            url_params['Currency'] = currency
        
        if email:
            url_params['Email'] = email
        
        # Add extra parameters
        if extra_params:
            for key, value in extra_params.items():
                url_params[f'Shp_{key}'] = value
        
        base_url = self.config.get_environment_url()
        return f"{base_url}?{urlencode(url_params)}"
    
    def verify_payment(
        self,
        merchant_login: str,
        amount: float,
        invoice_id: str,
        signature: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Verify payment using primary password.
        
        Args:
            merchant_login: Merchant login
            amount: Payment amount
            invoice_id: Invoice ID
            signature: Signature to verify
            extra_params: Additional parameters
        
        Returns:
            True if payment is verified, False otherwise
        """
        return self.signature_validator.verify_callback_signature(
            merchant_login,
            amount,
            invoice_id,
            signature,
            self.config.get_password1(),
            extra_params
        )
    
    def verify_payment_secondary(
        self,
        merchant_login: str,
        amount: float,
        invoice_id: str,
        signature: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Verify payment using secondary password.
        
        Args:
            merchant_login: Merchant login
            amount: Payment amount
            invoice_id: Invoice ID
            signature: Signature to verify
            extra_params: Additional parameters
        
        Returns:
            True if payment is verified, False otherwise
        """
        return self.signature_validator.verify_callback_signature(
            merchant_login,
            amount,
            invoice_id,
            signature,
            self.config.get_password2(),
            extra_params
        )
    
    def process_success_callback(
        self,
        merchant_login: str,
        amount: float,
        invoice_id: str,
        signature: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        Process successful payment callback (Result URL).
        
        Args:
            merchant_login: Merchant login from callback
            amount: Payment amount from callback
            invoice_id: Invoice ID from callback
            signature: Signature from callback
            extra_params: Additional parameters from callback
        
        Returns:
            Tuple of (is_valid, response_message)
        """
        if not self.verify_payment(merchant_login, amount, invoice_id, signature, extra_params):
            logger.warning(
                f"Invalid signature for invoice {invoice_id}: {signature}"
            )
            return False, "Invalid signature"
        
        logger.info(f"Payment successful for invoice {invoice_id}, amount: {amount}")
        return True, f"OK{invoice_id}"
    
    def process_fail_callback(
        self,
        merchant_login: str,
        amount: float,
        invoice_id: str,
        signature: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        Process failed payment callback (Fail URL).
        
        Args:
            merchant_login: Merchant login from callback
            amount: Payment amount from callback
            invoice_id: Invoice ID from callback
            signature: Signature from callback
            extra_params: Additional parameters from callback
        
        Returns:
            Tuple of (is_valid, response_message)
        """
        if not self.verify_payment_secondary(
            merchant_login, amount, invoice_id, signature, extra_params
        ):
            logger.warning(
                f"Invalid signature for failed payment invoice {invoice_id}"
            )
            return False, "Invalid signature"
        
        logger.info(f"Payment failed for invoice {invoice_id}")
        return True, "FAIL"
    
    def process_status_callback(
        self,
        merchant_login: str,
        amount: float,
        invoice_id: str,
        signature: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        Process status callback (Check URL).
        
        Args:
            merchant_login: Merchant login from callback
            amount: Payment amount from callback
            invoice_id: Invoice ID from callback
            signature: Signature from callback
            extra_params: Additional parameters from callback
        
        Returns:
            Tuple of (is_valid, response_message)
        """
        if not self.verify_payment_secondary(
            merchant_login, amount, invoice_id, signature, extra_params
        ):
            logger.warning(
                f"Invalid signature for status check invoice {invoice_id}"
            )
            return False, "Invalid signature"
        
        logger.debug(f"Status check for invoice {invoice_id}")
        return True, f"OK{invoice_id}"
    
    def get_operation_status(
        self,
        merchant_login: str,
        operation_id: int,
        signature: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get operation status from Robokassa API.
        
        Args:
            merchant_login: Merchant login
            operation_id: Operation ID to check
            signature: MD5(MerchantLogin:OperationId:Password2)
        
        Returns:
            Operation details or None if failed
        """
        url = "https://auth.robokassa.ru/Merchant/OperationStatus/"
        
        params = {
            'MerchantLogin': merchant_login,
            'OperationId': operation_id,
            'Signature': signature,
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            # Parse response (format: OperationId;OperationStatus[;Details])
            data = response.text.strip().split(';')
            
            if len(data) < 2:
                logger.error(f"Invalid operation status response: {response.text}")
                return None
            
            return {
                'operation_id': int(data[0]),
                'status': data[1],
                'details': data[2] if len(data) > 2 else None,
            }
        except RequestException as e:
            logger.error(f"Failed to get operation status: {e}")
            return None
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class RobokassaCallbackHandler:
    """Handles incoming Robokassa callbacks."""
    
    def __init__(self, payment_handler: RobokassaPaymentHandler):
        """
        Initialize callback handler.
        
        Args:
            payment_handler: RobokassaPaymentHandler instance
        """
        self.payment_handler = payment_handler
    
    def extract_callback_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract callback data from request.
        
        Args:
            request_data: Request data from Robokassa
        
        Returns:
            Extracted callback data
        """
        return {
            'merchant_login': request_data.get('MerchantLogin'),
            'amount': float(request_data.get('Sum', 0)),
            'invoice_id': request_data.get('InvId'),
            'signature': request_data.get('SignatureValue'),
            'extra_params': {
                k[4:]: v for k, v in request_data.items() if k.startswith('Shp_')
            },
        }
    
    def handle_success_callback(
        self,
        request_data: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Handle success callback (Result URL).
        
        Args:
            request_data: Request data from Robokassa
        
        Returns:
            Tuple of (is_valid, response_message)
        """
        data = self.extract_callback_data(request_data)
        return self.payment_handler.process_success_callback(
            data['merchant_login'],
            data['amount'],
            data['invoice_id'],
            data['signature'],
            data['extra_params']
        )
    
    def handle_fail_callback(
        self,
        request_data: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Handle fail callback (Fail URL).
        
        Args:
            request_data: Request data from Robokassa
        
        Returns:
            Tuple of (is_valid, response_message)
        """
        data = self.extract_callback_data(request_data)
        return self.payment_handler.process_fail_callback(
            data['merchant_login'],
            data['amount'],
            data['invoice_id'],
            data['signature'],
            data['extra_params']
        )
    
    def handle_status_callback(
        self,
        request_data: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Handle status callback (Check URL).
        
        Args:
            request_data: Request data from Robokassa
        
        Returns:
            Tuple of (is_valid, response_message)
        """
        data = self.extract_callback_data(request_data)
        return self.payment_handler.process_status_callback(
            data['merchant_login'],
            data['amount'],
            data['invoice_id'],
            data['signature'],
            data['extra_params']
        )
