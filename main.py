from fastapi import FastAPI, Request
import uvicorn

from endpoint.api_util import api_router as api_router_util


app = FastAPI()
app.include_router(api_router_util, prefix='/util', tags=['工具'])


@app.get("/")
async def root():
    return {"message": "Hello, celery monitor"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=5600, reload=True, workers=4)
