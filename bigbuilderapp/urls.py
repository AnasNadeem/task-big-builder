from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    UserViewSet,
    TaskViewSet,
    TaskPicViewSet,
    TaskPaymentViewSet,
)


router = routers.SimpleRouter(trailing_slash=False)
router.register(r"task", TaskViewSet, basename="task")
router.register(r"taskpic", TaskPicViewSet, basename="taskpic")
router.register(r"taskpayment", TaskPaymentViewSet, basename="taskpayment")
router.register(r"user", UserViewSet, basename="user")

urlpatterns = []

urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
