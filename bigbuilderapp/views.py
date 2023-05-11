from django.conf import settings
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    TaskSerializer,
    TaskPicSerializer,
    TaskPaymentSerializer,
)

from .models import (
    Task,
    TaskPic,
    TaskPayment,
)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=["get"])
    def pics(self, request, pk=None):
        task = self.get_object()
        pics = TaskPic.objects.filter(task=task)
        serializer = TaskPicSerializer(pics, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"])
    def payments(self, request, pk=None):
        task = self.get_object()
        payments = TaskPayment.objects.filter(task=task)
        serializer = TaskPaymentSerializer(payments, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class TaskPicViewSet(ModelViewSet):
    queryset = TaskPic.objects.all()
    serializer_class = TaskPicSerializer


class TaskPaymentViewSet(ModelViewSet):
    queryset = TaskPayment.objects.all()
    serializer_class = TaskPaymentSerializer
