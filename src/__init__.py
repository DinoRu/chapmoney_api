from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.auth.routes import auth_router
from src.country.routes import country_router
from src.currency.routes import currency_router
from src.exchange_rates.routes import rate_router
from src.fees.routes import fee_router
from src.rates.routes import exchange_router
from src.receive_payment_method.routes import r_method_router
from src.send_payment_method.routes import sender_router
from src.transactions.routes import T_router
from src.websocket_manager import websocket_manager

version = 'v1'
app = FastAPI(
    title="Chapmoney",
    description="A REST API for CHAPMONEY service.",
    version=version,
    swagger_ui_parameters={
        "persistAuthorization": True
    },
)

@app.websocket("/ws/admin")
async def admin_websocket(websocket: WebSocket):
    await websocket_manager.connect_admin(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)


@app.websocket("/ws/client/{user_id}")
async def client_websocket(websocket: WebSocket, user_id: str):
    await websocket_manager.connect_client(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

@app.get("/test")
async def test():
    await websocket_manager.send_to_admins("Test message")
    return dict(message="Message sent to admins")

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['Auth'])
app.include_router(currency_router, prefix=f"/api/{version}/currency", tags=['Currency'])
app.include_router(country_router, prefix=f"/api/{version}/country", tags=["Country"])
app.include_router(rate_router, prefix=f"/api/{version}/rate", tags=['Rate'])
app.include_router(fee_router, prefix=f"/api/{version}/fee", tags=["Fee"])
app.include_router(r_method_router, prefix=f"/api/{version}/receiver_payment", tags=["Receiver payment"])
app.include_router(sender_router, prefix=f"/api/{version}/sender_payment", tags=["Sender payment"])
app.include_router(exchange_router, prefix=f"/api/{version}/exchange-rate", tags=["Exchange Rate"])
app.include_router(T_router, prefix=f"/api/{version}/transaction", tags=["Transaction"])