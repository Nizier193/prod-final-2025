from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.config import config
from dotenv import load_dotenv
import uvicorn

from modules import endpoints

load_dotenv()

# API
app = FastAPI()
app.include_router(endpoints)

# Обработчик ошибок 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=str(exc)
    )


@app.get("/ping")
def say_hi():
    return JSONResponse(
        content={"status": "online"},
        status_code=200
    )

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=config.HOST,
        port=config.PORT
    )