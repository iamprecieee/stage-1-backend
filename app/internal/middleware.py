from .config import settings
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


middleware = None if settings.use_middleware.lower() == "false" else [
    Middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins.split(","),
        allow_credentials=True,
        allow_methods=["GET", "OPTIONS"]
    ),
    Middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts.split(","))
]