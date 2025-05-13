from django.contrib import admin
from guardian.shortcuts import assign_perm
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'assigned_to')

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        assign_perm('view_task', obj.created_by, obj)
        assign_perm('change_task', obj.created_by, obj)

        if obj.assigned_to:
            assign_perm('view_task', obj.assigned_to, obj)
            assign_perm('change_task', obj.assigned_to, obj)
