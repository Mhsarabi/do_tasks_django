from rest_framework import generics
from .serializers import RegistrationSerializer,CustomAuthTokenSerializer,CustomTokenObtainPairSerializer,ChangePasswordSerializer,PasswordResetConfirmSerializer,PasswordResetRequestSerializer
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
from mail_templated import EmailMessage
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidSignatureError
from account.api.utils import EmailThreading
from django.conf import settings
from django.urls import reverse
from account.api.utils import generate_encrypted_token,decrypt_encrypted_token
from django.http import HttpResponseRedirect



class RegistrationApiView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer
    
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email=serializer.validated_data['email']

            user_obj=get_object_or_404(User,email=email)
            token=self.get_token_for_user(user_obj)
            email_obj=EmailMessage('email/activation_email.tpl',{'token':token},'admin@admin.com',to=[email])
            EmailThreading(email_obj).start()
            data={
                'email': email,
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_token_for_user(self,user):
        refresh=RefreshToken.for_user(user)
        return str(refresh.access_token)

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

class ActivationApiView(APIView):
    def get(self,request,token,*args,**kwargs):
        try:
            token=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user_id=token.get("user_id")
        except ExpiredSignatureError:
            return Response({'details':'token has been expired'},status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'details':'token is not valid'},status=status.HTTP_400_BAD_REQUEST)
        
        user_obj=User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({'details':'your account has already verified'},status=status.HTTP_400_BAD_REQUEST)
        user_obj.is_verified=True
        user_obj.save()
        return HttpResponseRedirect('/account/login')
    

class ChangePasswordApiView(generics.GenericAPIView):
    model=User
    permission_classes=[IsAuthenticated]
    serializer_class=ChangePasswordSerializer

    def get_object(self):
        obj=self.request.user
        return obj
    
    def post(self,request,*args,**kwargs):
        self.object=self.get_object()
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password':'wrong password'},status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'details':'password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        token_data = {
            "user_id": user.id,
            "email": user.email,
        }

        token = generate_encrypted_token(token_data)

        reset_url = request.build_absolute_uri(
            reverse('account:Reset_password') + f"?token={token}"
        )

        email_obj = EmailMessage(
            'email/reset_password_email.tpl',
            {'reset_url': reset_url},
            'admin@admin.com',
            to=[email]
        )
        EmailThreading(email_obj).start()

        return Response({'detail': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)


class PasswordResetConfirmApiView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "detail": "Please send a POST request with new_password and confirm_new_password to reset your password."
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Missing token in URL."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "token": token,
            "new_password": request.data.get("new_password"),
            "confirm_new_password": request.data.get("confirm_new_password")
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            payload = decrypt_encrypted_token(token)
            user = User.objects.get(id=payload['user_id'])
        except (ValueError, User.DoesNotExist):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)