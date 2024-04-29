from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
)

from .forms import CustomUserCreationForm, TaskForm
from .models import Task


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    ordering = ['title'] 
    template_name = "home.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get('status')
        sortby = self.request.GET.get('sortby')
        queryset = queryset.filter(user=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        if sortby:
            queryset = queryset.order_by(sortby)

        return queryset


class TaskCreateView(CreateView):
    model = Task
    context_object_name = "task"
    form_class = TaskForm
    template_name = "task/task_create.html"
    success_url = reverse_lazy("home") 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['status_choices'] = Task.STATUS_CHOICES
        
        return context

# class TaskDetailView(DetailView):
#     model = Task
#     context_object_name = "task"


class TaskUpdateView(UpdateView):
    model = Task
    context_object_name = "task"
    form_class = TaskForm
    template_name = "task/task_create.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["status_choices"] = Task.STATUS_CHOICES

        return context


class TaskDeleteView(DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("home")
    template_name = "task/task_delete.html"
