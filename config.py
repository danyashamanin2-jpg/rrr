from dataclasses import dataclass
from typing import Optional


@dataclass
class RobokassaConfig:
    """Configuration for Robokassa payment service."""
    merchant_login: str
    password1: str
    password2: str
    test_mode: bool = False


@dataclass
class Config:
    """Main application configuration."""
    robokassa: RobokassaConfig
