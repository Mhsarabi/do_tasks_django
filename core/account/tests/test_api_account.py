import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from account.models import User
from account.api.utils import generate_encrypted_token

@pytest.fixture
def api_client():
    client=APIClient()
    return client

@pytest.fixture
def common_user():
    user=User.objects.create_user(email='admin@admin.com',password='Ms*#15973')
    user.is_verified=True
    user.save()
    return user

@pytest.mark.django_db
class TestAccountApi:

    def test_register_api(self,api_client):
        url_register=reverse('account:api_v1:registration-token')
        data={
            'email':'admin@admin.com',
            'password':'Ms*#15973',
            'password_confirm':'Ms*#15973'
        }
        response_register=api_client.post(url_register,data)
        assert response_register.status_code==201


    def test_login_api(self,api_client,common_user):
        url_login=reverse('account:api_v1:login')
        data={
            'email':'admin@admin.com',
            'password':'Ms*#15973',
        }
        response_login=api_client.post(url_login,data)
        assert response_login.status_code==200

    def test_logout_api(self,api_client,common_user):
        url_logout=reverse('account:api_v1:logout')
        api_client.force_authenticate(user=common_user)
        response_logout=api_client.post(url_logout)
        assert response_logout.status_code==204

    def test_change_password_api(self,api_client,common_user):
        url_password_change=reverse('account:api_v1:change_password')
        data={
            'old_password':'Ms*#15973',
            'new_password':'Mo*#15973',
            'confirm_new_password':'Mo*#15973'
        }
        api_client.force_authenticate(user=common_user)
        response_password_change=api_client.post(url_password_change,data)
        print(response_password_change.data)
        assert response_password_change.status_code==200
    
    def test_reset_password_api(self,api_client,common_user):
        url_reset_password=reverse('account:api_v1:password-reset')
        data={
            'email':common_user.email
        }
        response_reset_password=api_client.post(url_reset_password,data)
        assert response_reset_password.status_code == 200
        assert 'Password reset link sent to your email' in response_reset_password.data['detail']
    
    def test_reset_password_confirm(self,api_client,common_user):
        token = generate_encrypted_token({
        'user_id': common_user.id,
        'email': common_user.email
        })
        url_reset_password_confirm=reverse('account:api_v1:password-reset-confirm')+ f'?token={token}'
        data = {
        'new_password': '147Mo963',
        'confirm_new_password': '147Mo963'
        }
        response_reset_password_confirm=api_client.post(url_reset_password_confirm,data)
        assert response_reset_password_confirm.status_code == 200
        assert 'Password has been reset successfully.' in response_reset_password_confirm.data['detail']
       




