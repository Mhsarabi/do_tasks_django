from rest_framework import generics
from .serializers import RegistrationSerializer,CustomAuthTokenSerializer,CustomTokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationApiView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer
    
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()

            token, create = Token.objects.get_or_create(user=user)

            refresh = RefreshToken.for_user(user)
            data={
                'email': user.email,
                'token': token.key,                      
                'access': str(refresh.access_token),     
                'refresh': str(refresh),
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class=CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })
    
class CustomDiscardAuthToken(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer