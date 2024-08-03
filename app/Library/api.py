from django.contrib.auth import authenticate
from ninja import NinjaAPI, Schema
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI
from ninja.errors import HttpError

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/books", "Books.api.router")
api.add_router("/user/", "Books.user_api.router")
# api.add_router("/genres", "Books.api.router")