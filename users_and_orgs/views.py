from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users_and_orgs.models import CustomUser, Organization
from users_and_orgs.permissions import IsOwnerOrReadOnly, \
    IsAuthenticatedOrPostAndReadOnly
from users_and_orgs.serializers import UserSerializer, OrganizationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Custom user ViewSet for CRUD users"""

    queryset = CustomUser.objects.all().prefetch_related("organizations")
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrPostAndReadOnly)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrgsAPIView(ListCreateAPIView):
    """Get organizations list with list of related objects or create it"""

    queryset = Organization.objects.all().prefetch_related("employees")
    serializer_class = OrganizationSerializer
