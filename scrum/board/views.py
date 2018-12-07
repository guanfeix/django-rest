from rest_framework import viewsets, permissions, authentication
from .models import *
from .serializers import *


class SprintViewSet(viewsets):
    """API endpoint for listing and creating sprints"""

    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer


class DefaultsMixin(object):
    "default setting for view authentication,permissions filtering and pagination"

    authentication_classes = (authentication.BasicAuthentication,
                              authentication.TokenAuthentication)

    permissions_classes = (permissions.IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # filter_class = TaskFilter
    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'order', 'started', 'due', 'completed',)


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing users."""

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD,)


