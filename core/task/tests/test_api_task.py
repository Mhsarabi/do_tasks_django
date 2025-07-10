import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from account.models import User
from task.models import Task

@pytest.fixture
def api_client():
    client=APIClient()
    return client

@pytest.fixture
def common_user():
    user=User.objects.create_user(email='admin@admin.com',password='159736')
    return user

@pytest.mark.django_db
class TestTaskApi:

    def test_get_task_list_successful_response(self,api_client,common_user):
        url=reverse('task:api_v1:task-list')
        user=common_user
        api_client.force_authenticate(user=user)
        response=api_client.get(url)
        assert response.status_code==200

    
    def test_CRUD_specific_task_successful_response(self,api_client,common_user):
        # post a specific task
        url_post=reverse('task:api_v1:task-list')
        data={
            'task':'test',
            'done':False
        }
        user=common_user
        api_client.force_authenticate(user=user)
        response_post=api_client.post(url_post,data)

        # get a specific task
        url_get=reverse('task:api_v1:task-single',kwargs={'pk':response_post.data['id']})
        response_get=api_client.get(url_get)

        # update a specific task
        url_update=reverse('task:api_v1:task-single',kwargs={'pk':response_post.data['id']})
        data_update={
            'done':True
        }
        response_update=api_client.patch(url_update,data=data_update)

        # delete a specific task
        url_delete=reverse('task:api_v1:task-single',kwargs={'pk':response_post.data['id']})
        response_delete=api_client.delete(url_delete)

        assert response_post.status_code==201
        assert response_get.status_code==200
        assert response_update.status_code==200
        assert response_delete.status_code==204
