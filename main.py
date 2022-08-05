import uvicorn
from fastapi import FastAPI
from api.routers import api_router

app = FastAPI(title='Sumarizador')

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app)