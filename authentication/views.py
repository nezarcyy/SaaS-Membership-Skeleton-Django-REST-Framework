from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .serializers import CustomUserSerializer


@permission_classes([AllowAny])
class CustomUserView(UserViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ['get']