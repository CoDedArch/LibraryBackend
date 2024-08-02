from ninja import NinjaAPI, Schema
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/books", "Books.api.router")
# api.add_router("/genres", "Books.api.router")

class UserSchema(Schema):
    username: str
    is_authenticated: bool

@api.get('/hello')
def hello(request):
    return "Hello world"

@api.get('/me', response=UserSchema, auth=JWTAuth())
def me(request):
    return request.user