from sys import prefix

from fastapi import FastAPI

from src.auth.routes import auth_router
from src.country.routes import country_router
from src.currency.routes import currency_router
from src.exchange_rates.routes import rate_router
from src.fees.routes import fee_router
from src.receive_payment_method.routes import r_method_router

version = 'v1'
app = FastAPI(
	title="Chapmoney",
	description="A REST API for CHAPMONEY service.",
	version=version
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['Auth'])
app.include_router(currency_router, prefix=f"/api/{version}/currency", tags=['Currency'])
app.include_router(country_router, prefix=f"/api/{version}/country", tags=["Country"])
app.include_router(rate_router, prefix=f"/api/{version}/rate", tags=['Rate'])
app.include_router(fee_router, prefix=f"/api/{version}/fee", tags=["Fee"])
app.include_router(r_method_router, prefix=f"/api/{version}/receiver_payment", tags=["Receiver payment"])
