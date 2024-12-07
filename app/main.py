# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import task_routes, reminder_routes, user_routes, composite_routes, motivation_quote_routes
from app.graphql.schema import schema as graphql_schema
from strawberry.fastapi import GraphQLRouter
import logging
import time
app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register routes
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(reminder_routes.router,
                   prefix="/reminders", tags=["Reminders"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])

app.include_router(composite_routes.router,
                   prefix="/composite", tags=["Composite Operations"])
app.include_router(motivation_quote_routes.router,
                   prefix="/quote", tags=["Quotes"])

# Register GraphQL route
graphql_app = GraphQLRouter(graphql_schema)
app.include_router(graphql_app, prefix="/graphql")

# Set up CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to log requests before and after


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Response status: {response.status_code} | Time: {process_time:.4f}s")
    return response
