from fastapi import FastAPI
from src.routers.authorization import router as router_authorization
from src.routers.authorization_vk import router as router_authorization_vk
from src.routers.validate_jwt import router as router_validate_jwt
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address, default_limits=["10/second"])

app = FastAPI(title="Регистрация")

app.include_router(router_authorization)

app.include_router(router_authorization_vk)

app.include_router(router_validate_jwt)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
