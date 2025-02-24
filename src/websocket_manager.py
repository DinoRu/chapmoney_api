from typing import Dict, List
from fastapi import WebSocket


class WebSocketManager:
	def __init__(self):
		self.active_connections: Dict[str, List[WebSocket]] = {
			"admin": [],
			"clients": {}
		}

	async def connect_admin(self, websocket: WebSocket):
		await websocket.accept()
		self.active_connections['admin'].append(websocket)

	async def connect_client(self, websocket: WebSocket, user_id: str):
		await websocket.accept()
		if user_id not in self.active_connections["clients"]:
			self.active_connections["clients"][user_id] = []
		self.active_connections["clients"][user_id].append(websocket)


	async def send_to_admins(self, message: str):
		"""send push notifications to the admins"""
		for websocket in self.active_connections['admin']:
			await websocket.send_text(message)

	async def send_to_client(self, user_id: str, message: str):
		"""Notification for special user"""
		if user_id in self.active_connections['clients']:
			for websocket in self.active_connections['clients'][user_id]:
				await websocket.send_text(message)


	def disconnect(self, websocket: WebSocket):
		if websocket in self.active_connections['admin']:
			self.active_connections['admin'].remove(websocket)
		for user_id in self.active_connections['clients']:
			if websocket in self.active_connections['clients'][user_id]:
				self.active_connections['clients'][user_id].remove(websocket)


websocket_manager = WebSocketManager()