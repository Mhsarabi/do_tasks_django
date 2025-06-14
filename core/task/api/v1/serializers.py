from rest_framework import serializers
from ...models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'
        read_only_fields=['id','user']

    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
        return super().create(validated_data)