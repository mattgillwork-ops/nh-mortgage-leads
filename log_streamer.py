import asyncio
import os

async def read_logs(file_path):
    with open(file_path, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                await asyncio.sleep(1)
                continue
            yield line.strip()

async def log_streamer(websocket, file_path):
    async for log_line in read_logs(file_path):
        await websocket.send_text(log_line)
