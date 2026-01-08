"""
FSM states for Robokassa payment handling.
"""

from aiogram.fsm.state import State, StatesGroup


class RobokassaPaymentStates(StatesGroup):
    """States for Robokassa payment processing workflow."""

    # Initial state for payment initiation
    waiting_for_payment_amount = State()
    
    # Payment processing states
    payment_initiated = State()
    payment_pending = State()
    payment_processing = State()
    
    # Success states
    payment_completed = State()
    payment_confirmed = State()
    
    # Failure/Error states
    payment_failed = State()
    payment_cancelled = State()
    payment_timeout = State()
    
    # Refund states
    refund_requested = State()
    refund_processing = State()
    refund_completed = State()
    
    # Additional states
    waiting_for_confirmation = State()
    error_occurred = State()
