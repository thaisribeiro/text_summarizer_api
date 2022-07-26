import uvicorn
from fastapi import FastAPI
from api.routers import api_router

app = FastAPI(title='Sumarizador')

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1:8000', port='8000', reload=True)