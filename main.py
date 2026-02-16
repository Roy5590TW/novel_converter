import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.database import init_db
from src.importer import run_import
from src.app import router
from src.logger_config import logger

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("--- 系統啟動中 ---")
    await init_db()
    await run_import()
    logger.info("--- 資料準備就緒 ---")

app.include_router(router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)