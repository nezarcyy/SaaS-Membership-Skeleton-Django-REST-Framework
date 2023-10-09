from rest_framework.views import APIView
from rest_framework.response import Response

class CheckUserStatus(APIView):
    def get(self, request):
        # Assuming you have the user object in your request context
        user = request.user

        if user.is_active:
            return Response({'is_active': True})
        else:
            return Response({'is_active': False})
