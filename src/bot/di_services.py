"""Dependency injection for bot services."""
from dishka import Provider, Scope, provide

from ..configuration import Configuration
from .services.receipt_scanner import ReceiptScanner


class ServicesProvider(Provider):
    """Provider for bot services."""

    @provide(scope=Scope.APP)
    def provide_receipt_scanner(self, config: Configuration) -> ReceiptScanner:
        """Provide receipt scanner service.

        Args:
            config: Application configuration

        Returns:
            ReceiptScanner instance
        """
        return ReceiptScanner(storage_path=config.storage.receipts_path)
