from functools import wraps
from fastapi import HTTPException
import logging
import uuid
import inspect

logger = logging.getLogger(__name__)

class OrderNotFoundError(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order {order_id} not found")

class InvalidOrderDataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class AIServiceError(Exception):
    def __init__(self, message: str, provider: str = None):
        self.message = message
        self.provider = provider
        super().__init__(message)

class RateLimitError(Exception):
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")

class ExceptionContext:
    def __init__(self, default_value=None, log_errors=True):
        self.default_value = default_value
        self.log_errors = log_errors
        self.exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.exception = exc_val
            if self.log_errors:
                logger.error(f"Exception in context: {str(exc_val)}")
            return True
        return False

EXCEPTION_MAP = {
    OrderNotFoundError: (404, lambda e: str(e)),
    InvalidOrderDataError: (400, lambda e: e.message),
    AIServiceError: (503, lambda e: f"AI service unavailable: {e.message}"),
    RateLimitError: (429, lambda e: str(e)),
    ValueError: (400, lambda e: str(e)),
    FileNotFoundError: (404, lambda e: "Resource not found"),
    PermissionError: (403, lambda e: "Access forbidden"),
    TimeoutError: (504, lambda e: "Request timeout. Please try again."),
    ConnectionError: (503, lambda e: "Service temporarily unavailable"),
}

def _get_exception_details(exception: Exception) -> tuple[int, str, dict]:

    exception_type = type(exception)
    if exception_type in EXCEPTION_MAP:
        status_code, message_func = EXCEPTION_MAP[exception_type]
        detail = message_func(exception)
        # Special handling for rate limit
        headers = {}
        if isinstance(exception, RateLimitError):
            headers["Retry-After"] = str(exception.retry_after)
        
        return status_code, detail, headers
    
    error_id = str(uuid.uuid4())
    logger.error(f"Unexpected error (ID: {error_id}): {str(exception)}", exc_info=True)
    return 500, f"An unexpected error occurred. Error ID: {error_id}", {}

def handle_exceptions(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            status_code, detail, headers = _get_exception_details(e)
            
            if status_code >= 500:
                logger.error(f"Server error in {func.__name__}: {str(e)}")
            elif status_code >= 400:
                logger.warning(f"Client error in {func.__name__}: {str(e)}")
            
            raise HTTPException(
                status_code=status_code,
                detail=detail,
                headers=headers if headers else None
            )
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            status_code, detail, headers = _get_exception_details(e)
            
            if status_code >= 500:
                logger.error(f"Server error in {func.__name__}: {str(e)}")
            elif status_code >= 400:
                logger.warning(f"Client error in {func.__name__}: {str(e)}")
            
            raise HTTPException(
                status_code=status_code,
                detail=detail,
                headers=headers if headers else None
            )
    return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

def log_and_raise_http_exception(
    status_code: int,
    detail: str,
    context: str = None
):
    log_message = f"HTTP {status_code}: {detail}"
    if context:
        log_message += f" (Context: {context})"
    
    if status_code >= 500:
        logger.error(log_message)
    elif status_code >= 400:
        logger.warning(log_message)
    
    raise HTTPException(status_code=status_code, detail=detail)

def safe_execute(func, default_value=None, log_errors=True):
    try:
        return func()
    except Exception as e:
        if log_errors:
            logger.error(f"Error in safe_execute: {str(e)}")
        return default_value

def validate_and_raise(condition: bool, exception_class: type, *args, **kwargs):
    if not condition:
        raise exception_class(*args, **kwargs)

def is_client_error(status_code: int) -> bool:
    return 400 <= status_code < 500

def is_server_error(status_code: int) -> bool:
    return status_code >= 500

def get_error_severity(status_code: int) -> str:
    if status_code >= 500:
        return "error"
    elif status_code >= 400:
        return "warning"
    else:
        return "info"