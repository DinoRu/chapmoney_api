import logging
import uuid
from typing import Any
from datetime import datetime, timedelta

import jwt
from itsdangerous import URLSafeTimedSerializer
from passlib.context import CryptContext

from src.config import Config

passwd_context = CryptContext(schemes=['bcrypt'])


ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password: str) -> str:
	pwd_hash = passwd_context.hash(password)

	return pwd_hash


def verify_password(password: str, pwd_hash: str) -> bool:
	return passwd_context.verify(password, pwd_hash)


def create_access_token(
		user_data: dict,
		expiry: timedelta = None,
		refresh: bool = False
):
	payload = {}

	payload["user"] = user_data
	payload['exp'] = datetime.now() + (
		expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
	)
	payload["jti"] = str(uuid.uuid4())
	payload["refresh"] = refresh
	token = jwt.encode(
		payload=payload, key=Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM
	)
	return token

def decode_token(token: str) -> Any | None:
	try:
		token_data = jwt.decode(
			jwt=token, key=Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
		)
		return token_data
	except jwt.PyJWTError as e:
		logging.exception(e)
		return None

serializer = URLSafeTimedSerializer(
	secret_key=Config.JWT_SECRET, salt="email-configuration"
)

def create_url_safe_token(data: dict):

	token = serializer.dumps(data)
	return token

def decode_url_safe_token(token: str):
	try:
		token_data = serializer.loads(token)
		return token_data
	except Exception as e:
		logging.error(str(e))

