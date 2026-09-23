from typing import Any


class RetainAIError(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(RetainAIError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, code="NOT_FOUND")


class ValidationError(RetainAIError):
    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(message, code="VALIDATION_ERROR")


class AuthenticationError(RetainAIError):
    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, code="AUTHENTICATION_ERROR")


class AuthorizationError(RetainAIError):
    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message, code="AUTHORIZATION_ERROR")


class DatabaseConnectionError(RetainAIError):
    def __init__(self, message: str = "Database connection failed") -> None:
        super().__init__(message, code="DATABASE_ERROR")


class ConfigurationError(RetainAIError):
    def __init__(self, message: str = "Configuration error") -> None:
        super().__init__(message, code="CONFIGURATION_ERROR")
