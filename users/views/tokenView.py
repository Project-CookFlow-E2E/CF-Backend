from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers.tokenSerializer import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer