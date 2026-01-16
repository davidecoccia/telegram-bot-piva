"""This package is used for a bot logic implementation."""
from .help import help_router
from .receipt_handler import receipt_router
from .start import start_router

routers = (start_router, help_router, receipt_router)
