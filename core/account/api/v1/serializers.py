from rest_framework import serializers
from account.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm=serializers.CharField(max_length=255,write_only=True)

    class Meta:
        model=User
        fields=['email','password','password_confirm']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"details":"passwords does not match"})
        
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as errors:
            raise serializers.ValidationError({'password':list(errors.messages)})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password_confirm',None)
        return User.objects.create_user(**validated_data)
    
class CustomAuthTokenSerializer(serializers.Serializer):
    email=serializers.CharField(label=_("Email"),write_only=True)
    password=serializers.CharField(label=_("password"),style={'input_type':'password'},trim_whitespace=False,write_only=True)
    token=serializers.CharField(label=_("token"),read_only=True)

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        if email and password:
            user=authenticate(request=self.context.get('request'),username=email,password=password)

            if not user:
                msg=_('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg,code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({"detail":"user is not verified"})
        else:
            msg=_('Must include "username" and "password".')
            raise serializers.ValidationError(msg,code='authorization')
        
        attrs['user']=user
        return attrs

    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data=super().validate(attrs)
        validated_data['email']=self.user.email
        validated_data['user_id']=self.user.id
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail":"user is not verified"})
        return validated_data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)
    confirm_new_password=serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_new_password'):
            raise serializers.ValidationError({'details':"passwords does not match"})
        
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
        
        return super().validate(attrs)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"error":"User with this email does not exist."})
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True,required=False)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_new_password"):
            raise serializers.ValidationError({"detail": "Passwords do not match."})

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs