from typing import Dict, Any, Optional
from datetime import datetime

def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
) -> Dict[str, Any]:
    response = {
        "success": True,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    
    return response

def error_response(
    message: str = "An error occurred",
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 400
) -> Dict[str, Any]:
    response = {
        "success": False,
        "error": {
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    }
    
    if error_code:
        response["error"]["code"] = error_code
    
    if details:
        response["error"]["details"] = details
    
    return response

def paginated_response(
    items: list,
    total_count: int,
    page: int = 1,
    page_size: int = 50,
    message: str = "Success"
) -> Dict[str, Any]:
    total_pages = (total_count + page_size - 1) // page_size
    
    return {
        "success": True,
        "message": message,
        "data": {
            "items": items,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        },
        "timestamp": datetime.now().isoformat()
    }

def validation_error_response(
    field_errors: Dict[str, str],
    message: str = "Validation failed"
) -> Dict[str, Any]:
    return error_response(
        message=message,
        error_code="VALIDATION_ERROR",
        details={"field_errors": field_errors},
        status_code=422
    )

def not_found_response(
    resource: str,
    resource_id: Optional[str] = None
) -> Dict[str, Any]:
    message = f"{resource} not found"
    if resource_id:
        message += f" (ID: {resource_id})"
    
    return error_response(
        message=message,
        error_code="NOT_FOUND",
        status_code=404
    )

def unauthorized_response(
    message: str = "Unauthorized access"
) -> Dict[str, Any]:
    return error_response(
        message=message,
        error_code="UNAUTHORIZED",
        status_code=401
    )

def forbidden_response(
    message: str = "Access forbidden"
) -> Dict[str, Any]:
    return error_response(
        message=message,
        error_code="FORBIDDEN",
        status_code=403
    )

def internal_server_error_response(
    message: str = "Internal server error",
    error_id: Optional[str] = None
) -> Dict[str, Any]:
    details = {}
    if error_id:
        details["error_id"] = error_id
    
    return error_response(
        message=message,
        error_code="INTERNAL_ERROR",
        details=details if details else None,
        status_code=500
    )

def rate_limit_response(
    retry_after: int = 60
) -> Dict[str, Any]:
    return error_response(
        message="Rate limit exceeded. Please try again later.",
        error_code="RATE_LIMIT_EXCEEDED",
        details={"retry_after": retry_after},
        status_code=429
    )