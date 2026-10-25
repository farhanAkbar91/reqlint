from typing import Any, Optional, List, Dict
from pydantic import BaseModel
from fastapi.responses import JSONResponse

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    data: Optional[Any] = None

class ErrorItem(BaseModel):
    field: Optional[str] = None
    message: str

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    error_code: Optional[str] = None
    errors: Optional[List[Dict[str, Any]]] = None

def success_response(message: str, data: Any = None, status_code: int = 200) -> JSONResponse:
    content = {
        "status": "success",
        "message": message,
        "data": data if data is not None else {}
    }
    return JSONResponse(status_code=status_code, content=content)

def error_response(
    message: str,
    error_code: Optional[str] = None,
    errors: Optional[List[Dict[str, Any]]] = None,
    status_code: int = 400
) -> JSONResponse:
    content = {
        "status": "error",
        "message": message
    }
    if error_code is not None:
        content["error_code"] = error_code
    if errors is not None:
        content["errors"] = errors
    return JSONResponse(status_code=status_code, content=content)
