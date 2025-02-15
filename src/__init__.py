from sys import prefix

from fastapi import FastAPI

from src.auth.routes import auth_router

version = 'v1'
app = FastAPI(
	title="Chapmoney",
	description="A REST API for CHAPMONEY service.",
	version=version
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['Auth'])
