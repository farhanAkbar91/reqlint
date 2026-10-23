import logging
from typing import Any, Optional, List, Dict
from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("reqlint.errors")

class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: Optional[str] = None,
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.errors = errors
        super().__init__(message)

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    content: Dict[str, Any] = {
        "status": "error",
        "message": exc.message
    }
    if exc.error_code:
        content["error_code"] = exc.error_code
    if exc.errors:
        content["errors"] = exc.errors
    return JSONResponse(status_code=exc.status_code, content=content)

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    # If detail is already a dict, try to preserve custom structure
    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", "Terjadi kesalahan")
        error_code = exc.detail.get("error_code")
        errors = exc.detail.get("errors")
        content: Dict[str, Any] = {"status": "error", "message": message}
        if error_code:
            content["error_code"] = error_code
        if errors:
            content["errors"] = errors
        return JSONResponse(status_code=exc.status_code, content=content)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": str(exc.detail)
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors_list: List[Dict[str, Any]] = []
    first_message = "Validasi data gagal"
    first_field = None
    
    for err in exc.errors():
        loc = err.get("loc", [])
        field_name = loc[-1] if loc else "body"
        msg = err.get("msg", "Format input tidak valid")
        if not first_field and field_name != "body":
            first_field = str(field_name)
            first_message = msg
        errors_list.append({
            "field": str(field_name),
            "message": msg
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": first_message,
            "error_code": "VALIDATION_ERROR",
            "errors": errors_list
        }
    )

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled server error at {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Gagal membuat berkas unduhan, silakan coba beberapa saat lagi" if "export" in str(request.url.path) else "Terjadi kesalahan pada server",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )
