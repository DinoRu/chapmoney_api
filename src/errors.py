from typing import Any, Callable, Type
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

class TransactionException(Exception):
    """Base class for all transaction exceptions."""
    pass


class InvalidToken(TransactionException): pass
class RevokedToken(TransactionException): pass
class AccessTokenRequired(TransactionException): pass
class RefreshTokenRequired(TransactionException): pass
class UserAlreadyExist(TransactionException): pass
class InvalidCredentials(TransactionException): pass
class InsufficientPermission(TransactionException): pass
class CurrencyNotFound(TransactionException): pass
class InsufficientBalance(TransactionException): pass
class UserNotFound(TransactionException): pass
class AccountNotVerified(TransactionException): pass
class InvalidTransaction(TransactionException): pass


EXCEPTION_HANDLERS = {
    UserAlreadyExist: (status.HTTP_403_FORBIDDEN, "User with email already exists.", "user_exists"),
    UserNotFound: (status.HTTP_404_NOT_FOUND, "User not found.", "user_not_found"),
    InsufficientBalance: (status.HTTP_402_PAYMENT_REQUIRED, "Insufficient balance.", "insufficient_balance"),
    AccountNotVerified: (status.HTTP_403_FORBIDDEN, "Account not verified.", "account_not_verified"),
    CurrencyNotFound: (status.HTTP_404_NOT_FOUND, "Currency not found.", "currency_not_found"),
    InvalidCredentials: (status.HTTP_401_UNAUTHORIZED, "Invalid credentials.", "invalid_credentials"),
    InvalidTransaction: (status.HTTP_400_BAD_REQUEST, "Transaction is invalid.", "invalid_transaction"),
    AccessTokenRequired: (status.HTTP_401_UNAUTHORIZED, "Please provide a valid access token.", "access_token_required"),
    RefreshTokenRequired: (status.HTTP_401_UNAUTHORIZED, "Please provide a valid refresh token.", "refresh_token_required"),
    InsufficientPermission: (status.HTTP_401_UNAUTHORIZED, "You do not have permission to perform this action.", "insufficient_permission"),
}

def create_exception_handler(status_code: int, message: str, error_code: str) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: TransactionException):
        return JSONResponse(content={"message": message, "error": error_code}, status_code=status_code)
    return exception_handler

def register_all_error(app: FastAPI):
    for exception_class, (status_code, message, error_code) in EXCEPTION_HANDLERS.items():
        app.add_exception_handler(exception_class, create_exception_handler(status_code, message, error_code))

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(content={"message": "Oops! Something went wrong.", "error_code": "internal_server_error"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError):
        print(str(exc))
        return JSONResponse(content={"message": "Oops! Something went wrong.", "error_code": "database_error"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
