from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from bigbuilderapp.models import (
    Task,
    TaskPic,
    TaskPayment,
)
from .serializers import (
    TaskSerializer,
    TaskPicSerializer,
    TaskPaymentSerializer,
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)

from .permissions import (
    TaskPermission,
    UserPermission,
    TaskPicPermission,
    TaskPaymentPermission,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def get_permissions(self):
        user_permission_map = {
            "update": UserPermission,
            "forget_password": UserPermission,
            'list': IsAuthenticated,
        }
        if self.action in user_permission_map:
            self.permission_classes = [user_permission_map.get(self.action)]
        return super().get_permissions()

    def get_serializer_class(self):
        user_serializer_map = {
            "create": RegisterSerializer,
            "login": LoginSerializer,
            "password_change": ChangePasswordSerializer,
        }
        return user_serializer_map.get(self.action.lower(), UserSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        user = User.objects.filter(email=email).first()
        if not user:
            return response.Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        authenticated = user.check_password(password)
        if not authenticated:
            return response.Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("password changed successfully ", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]

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
    permission_classes = [IsAuthenticated, TaskPicPermission]


class TaskPaymentViewSet(ModelViewSet):
    queryset = TaskPayment.objects.all()
    serializer_class = TaskPaymentSerializer
    permission_classes = [IsAuthenticated, TaskPaymentPermission]

