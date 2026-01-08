"""
Payment keyboards module for handling various payment methods.
Includes support for Robokassa and other payment providers.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_payment_keyboard() -> InlineKeyboardMarkup:
    """
    Creates a payment method selection keyboard.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with available payment methods
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Robokassa",
                    callback_data="payment_robokassa"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 YooMoney",
                    callback_data="payment_yoomoney"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏦 Bank Transfer",
                    callback_data="payment_bank"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Stripe",
                    callback_data="payment_stripe"
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Back",
                    callback_data="back_to_menu"
                )
            ]
        ]
    )
    return keyboard


def get_robokassa_keyboard() -> InlineKeyboardMarkup:
    """
    Creates a keyboard for Robokassa payment method selection.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with Robokassa options
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔐 Proceed to Robokassa",
                    callback_data="robokassa_proceed"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Payment Info",
                    callback_data="robokassa_info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Back",
                    callback_data="back_to_payment"
                )
            ]
        ]
    )
    return keyboard


def get_yoomoney_keyboard() -> InlineKeyboardMarkup:
    """
    Creates a keyboard for YooMoney payment method selection.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with YooMoney options
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔐 Proceed to YooMoney",
                    callback_data="yoomoney_proceed"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Payment Info",
                    callback_data="yoomoney_info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Back",
                    callback_data="back_to_payment"
                )
            ]
        ]
    )
    return keyboard


def get_bank_transfer_keyboard() -> InlineKeyboardMarkup:
    """
    Creates a keyboard for bank transfer payment method.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with bank transfer options
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Get Bank Details",
                    callback_data="bank_details"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Payment Info",
                    callback_data="bank_info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Back",
                    callback_data="back_to_payment"
                )
            ]
        ]
    )
    return keyboard


def get_stripe_keyboard() -> InlineKeyboardMarkup:
    """
    Creates a keyboard for Stripe payment method selection.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with Stripe options
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔐 Proceed to Stripe",
                    callback_data="stripe_proceed"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Payment Info",
                    callback_data="stripe_info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Back",
                    callback_data="back_to_payment"
                )
            ]
        ]
    )
    return keyboard


def get_payment_confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Creates a keyboard for payment confirmation.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with confirmation options
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Confirm Payment",
                    callback_data="confirm_payment"
                ),
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data="cancel_payment"
                )
            ]
        ]
    )
    return keyboard


def get_payment_status_keyboard() -> InlineKeyboardMarkup:
    """
    Creates a keyboard for checking payment status.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with status options
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Check Status",
                    callback_data="check_payment_status"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📧 Contact Support",
                    callback_data="contact_support"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="main_menu"
                )
            ]
        ]
    )
    return keyboard
