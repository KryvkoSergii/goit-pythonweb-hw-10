from fastapi import FastAPI
from api.contacts import router as contacts_router
from errors import ContactNotFoundError

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from schemas import ErrorContent, ErrorsContent

app = FastAPI(title="Contacts App")

app.include_router(contacts_router, prefix="/api")


@app.exception_handler(ContactNotFoundError)
def item_not_found_error_handler(request: Request, exc: ContactNotFoundError):
    error = ErrorContent(message=str(exc))
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorsContent(errors=[error]).model_dump()
    )


@app.exception_handler(ValueError)
def item_not_found_error_handler(request: Request, exc: ValueError):
    error = ErrorContent(message=str(exc))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorsContent(errors=[error]).model_dump()
    )


def handle_validation(validation_error) -> ErrorContent:
    message = f"{validation_error['msg']} '{'.'.join(validation_error['loc'][1:])}'"
    return ErrorContent(message = message)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [handle_validation(err) for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorsContent(errors=errors).model_dump()
    )


@app.exception_handler(Exception)
def item_not_found_error_handler(request: Request, exc: Exception):
    error = ErrorContent(message=str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorsContent(errors=[error]).model_dump()
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
