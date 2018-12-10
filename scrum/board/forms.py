from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model

from .models import Sprint, Task


User = get_user_model()


class NullFilter(filters.BooleanFilter):
    """Filter on a field set as null or not."""
    
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.field_name: value})
        return qs
        
        
class SprintFilter(filters.FilterSet):
    end_min = filters.DateFilter(field_name='end', lookup_expr='gte')
    end_max = filters.DateFilter(field_name='end', lookup_expr='lte')
    
    class Meta:
        model = Sprint
        fields = ('end_min', 'end_max', )


class TaskFilter(filters.FilterSet):
    
    backlog = NullFilter(name='sprint')
    
    class Meta:
        model = Task
        fields = ('sprint', 'status', 'assigned', 'backlog', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['assigned'].extra.update({'to_field_name': User.USERNAME_FIELD})