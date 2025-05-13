from rest_framework import viewsets, permissions
from guardian.shortcuts import assign_perm, get_objects_for_user
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'tasks.view_task')

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        assign_perm('view_task', self.request.user, task)
        assign_perm('change_task', self.request.user, task)
        assign_perm('view_task', task.assigned_to, task)
        assign_perm('change_task', task.assigned_to, task)



