from rest_framework import serializers
from bigbuilderapp.models import (
    Task,
    TaskPic,
    TaskPayment,
)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "user",
            "created_at",
            "asked_amount",
            "completed",
        )


class TaskPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPic
        fields = (
            "id",
            "task",
            "pic",
        )


class TaskPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPayment
        fields = (
            "id",
            "task",
            "payment",
            "payment_date",
        )
