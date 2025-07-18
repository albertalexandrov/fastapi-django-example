from web.api.examples.auth import router as auth_examples_router
from web.api.examples.permissions import router as permissions_examples_router
from web.api.examples.session import router as session_examples_router
from web.api.examples.crud import router as crud_examples_router

__all__ = [
    "auth_examples_router",
    "permissions_examples_router",
    "session_examples_router",
    "crud_examples_router",
]