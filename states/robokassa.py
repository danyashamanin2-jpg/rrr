"""
FSM states for Robokassa payment handling.

This module defines the finite state machine states and transitions
for managing Robokassa payment processing in the application.
"""

from enum import Enum


class RobokassaPaymentStates(str, Enum):
    """FSM states for Robokassa payment processing."""

    # Initial state
    PAYMENT_INITIAL = "payment:initial"
    
    # Payment creation and validation
    PAYMENT_PENDING = "payment:pending"
    PAYMENT_CREATED = "payment:created"
    PAYMENT_VALIDATION = "payment:validation"
    
    # Payment processing
    PAYMENT_PROCESSING = "payment:processing"
    PAYMENT_AWAITING_CALLBACK = "payment:awaiting_callback"
    
    # Successful completion
    PAYMENT_COMPLETED = "payment:completed"
    PAYMENT_CONFIRMED = "payment:confirmed"
    
    # Error and cancellation states
    PAYMENT_FAILED = "payment:failed"
    PAYMENT_CANCELLED = "payment:cancelled"
    PAYMENT_EXPIRED = "payment:expired"
    PAYMENT_REFUND_PENDING = "payment:refund_pending"
    PAYMENT_REFUNDED = "payment:refunded"
    
    # Final state
    PAYMENT_FINISHED = "payment:finished"


class RobokassaPaymentEvents(str, Enum):
    """Events that trigger state transitions in Robokassa payment FSM."""

    # Creation and validation events
    CREATE_PAYMENT = "create_payment"
    VALIDATE_PAYMENT = "validate_payment"
    VALIDATION_PASSED = "validation_passed"
    VALIDATION_FAILED = "validation_failed"
    
    # Processing events
    START_PROCESSING = "start_processing"
    PAYMENT_INITIATED = "payment_initiated"
    
    # Callback and confirmation events
    PAYMENT_SUCCESS_CALLBACK = "payment_success_callback"
    PAYMENT_FAILURE_CALLBACK = "payment_failure_callback"
    CONFIRM_PAYMENT = "confirm_payment"
    
    # Cancellation and expiration events
    CANCEL_PAYMENT = "cancel_payment"
    PAYMENT_EXPIRED_EVENT = "payment_expired"
    
    # Refund events
    INITIATE_REFUND = "initiate_refund"
    REFUND_COMPLETED = "refund_completed"
    REFUND_FAILED = "refund_failed"
    
    # Final events
    FINISH = "finish"
    RESET = "reset"


# FSM State Transitions Configuration
ROBOKASSA_STATE_TRANSITIONS = {
    RobokassaPaymentStates.PAYMENT_INITIAL: {
        RobokassaPaymentEvents.CREATE_PAYMENT: RobokassaPaymentStates.PAYMENT_PENDING,
    },
    RobokassaPaymentStates.PAYMENT_PENDING: {
        RobokassaPaymentEvents.VALIDATE_PAYMENT: RobokassaPaymentStates.PAYMENT_VALIDATION,
        RobokassaPaymentEvents.CANCEL_PAYMENT: RobokassaPaymentStates.PAYMENT_CANCELLED,
    },
    RobokassaPaymentStates.PAYMENT_VALIDATION: {
        RobokassaPaymentEvents.VALIDATION_PASSED: RobokassaPaymentStates.PAYMENT_CREATED,
        RobokassaPaymentEvents.VALIDATION_FAILED: RobokassaPaymentStates.PAYMENT_FAILED,
    },
    RobokassaPaymentStates.PAYMENT_CREATED: {
        RobokassaPaymentEvents.START_PROCESSING: RobokassaPaymentStates.PAYMENT_PROCESSING,
        RobokassaPaymentEvents.CANCEL_PAYMENT: RobokassaPaymentStates.PAYMENT_CANCELLED,
    },
    RobokassaPaymentStates.PAYMENT_PROCESSING: {
        RobokassaPaymentEvents.PAYMENT_INITIATED: RobokassaPaymentStates.PAYMENT_AWAITING_CALLBACK,
        RobokassaPaymentEvents.CANCEL_PAYMENT: RobokassaPaymentStates.PAYMENT_CANCELLED,
    },
    RobokassaPaymentStates.PAYMENT_AWAITING_CALLBACK: {
        RobokassaPaymentEvents.PAYMENT_SUCCESS_CALLBACK: RobokassaPaymentStates.PAYMENT_COMPLETED,
        RobokassaPaymentEvents.PAYMENT_FAILURE_CALLBACK: RobokassaPaymentStates.PAYMENT_FAILED,
        RobokassaPaymentEvents.PAYMENT_EXPIRED_EVENT: RobokassaPaymentStates.PAYMENT_EXPIRED,
    },
    RobokassaPaymentStates.PAYMENT_COMPLETED: {
        RobokassaPaymentEvents.CONFIRM_PAYMENT: RobokassaPaymentStates.PAYMENT_CONFIRMED,
    },
    RobokassaPaymentStates.PAYMENT_CONFIRMED: {
        RobokassaPaymentEvents.FINISH: RobokassaPaymentStates.PAYMENT_FINISHED,
        RobokassaPaymentEvents.INITIATE_REFUND: RobokassaPaymentStates.PAYMENT_REFUND_PENDING,
    },
    RobokassaPaymentStates.PAYMENT_REFUND_PENDING: {
        RobokassaPaymentEvents.REFUND_COMPLETED: RobokassaPaymentStates.PAYMENT_REFUNDED,
        RobokassaPaymentEvents.REFUND_FAILED: RobokassaPaymentStates.PAYMENT_CONFIRMED,
    },
    RobokassaPaymentStates.PAYMENT_REFUNDED: {
        RobokassaPaymentEvents.FINISH: RobokassaPaymentStates.PAYMENT_FINISHED,
    },
    RobokassaPaymentStates.PAYMENT_FAILED: {
        RobokassaPaymentEvents.RESET: RobokassaPaymentStates.PAYMENT_INITIAL,
    },
    RobokassaPaymentStates.PAYMENT_CANCELLED: {
        RobokassaPaymentEvents.RESET: RobokassaPaymentStates.PAYMENT_INITIAL,
    },
    RobokassaPaymentStates.PAYMENT_EXPIRED: {
        RobokassaPaymentEvents.RESET: RobokassaPaymentStates.PAYMENT_INITIAL,
    },
    RobokassaPaymentStates.PAYMENT_FINISHED: {
        # Final state - no further transitions
    },
}


# State categories for easy querying
INITIAL_STATES = {RobokassaPaymentStates.PAYMENT_INITIAL}
PROCESSING_STATES = {
    RobokassaPaymentStates.PAYMENT_PENDING,
    RobokassaPaymentStates.PAYMENT_VALIDATION,
    RobokassaPaymentStates.PAYMENT_CREATED,
    RobokassaPaymentStates.PAYMENT_PROCESSING,
    RobokassaPaymentStates.PAYMENT_AWAITING_CALLBACK,
}
SUCCESS_STATES = {
    RobokassaPaymentStates.PAYMENT_COMPLETED,
    RobokassaPaymentStates.PAYMENT_CONFIRMED,
}
ERROR_STATES = {
    RobokassaPaymentStates.PAYMENT_FAILED,
    RobokassaPaymentStates.PAYMENT_CANCELLED,
    RobokassaPaymentStates.PAYMENT_EXPIRED,
}
REFUND_STATES = {
    RobokassaPaymentStates.PAYMENT_REFUND_PENDING,
    RobokassaPaymentStates.PAYMENT_REFUNDED,
}
FINAL_STATES = {RobokassaPaymentStates.PAYMENT_FINISHED}
