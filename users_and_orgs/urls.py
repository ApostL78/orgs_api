from django.urls import include, path
from rest_framework import routers

from users_and_orgs.views import UserViewSet, OrgsAPIView

router = routers.SimpleRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("organizations/", OrgsAPIView.as_view(), name="orgs"),
]
