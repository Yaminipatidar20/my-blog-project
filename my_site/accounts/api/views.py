from rest_framework.generics import CreateAPIView
from .serializers import UserCreateSerializer

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

user_create_api_view = UserCreateAPIView().as_view()

