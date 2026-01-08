"""
User handler for Robokassa SBP payments.
"""

import logging
import uuid
from datetime import datetime
from typing import Optional

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(F.data == "pay_sbp")
async def sbp_payment_handler(callback: types.CallbackQuery, state: FSMContext):
    """Handle SBP payment button click."""
    offer_text = "📄 <b>ПУБЛИЧНАЯ ОФЕРТА</b>\n\nОплачивая услугу, вы соглашаетесь с условиями публичной оферты."
    await callback.answer("SBP payment handler initialized", show_alert=False)