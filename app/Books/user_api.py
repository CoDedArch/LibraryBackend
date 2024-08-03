from ninja import Router
from django.contrib.auth.models import User
from .models import Reader
from .schemas import SignupSchema

router = Router()

@router.post("/create_reader")
def create_user(request, payload:SignupSchema):
    user = User.objects.create_user(username=payload.username, password=payload.password, email=payload.email)
    reader = Reader.objects.create(user=user, fullname=payload.fullname, date_of_birth=payload.date_of_birth, city=payload.city)
    return {"success": True, "user_id": user.id}
