import asyncio
from src.database import init_db
from src.importer import run_import

async def start_process():
    print("正在初始化資料庫...")
    await init_db()
    
    print("正在掃描 inputs 並導入數據...")
    await run_import()
    
    print("所有流程已完成！")

if __name__ == "__main__":
    asyncio.run(start_process())