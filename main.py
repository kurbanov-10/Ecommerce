import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routes.users import users_router
from routes.Profiles import profiles_router
from routes.Products import products_router
from routes.Categories import categories_router
from routes.Tags import tags_router

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.headers['user-agent']}")
    if 'Postman' in request.headers['user-agent']:
        print("Request from Postman")
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    print(f"Response: {end_time - start_time} seconds")
    response.headers["X-Process-Time"] = str(end_time - start_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(tags_router)
