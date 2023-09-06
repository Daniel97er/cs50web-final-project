from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_view", views.register_view, name="register_view"),
    path("login_view", views.login_view, name="login_view"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("customers_view", views.customers_view, name="customers_view"),
    path("tasks_view", views.tasks_view, name="tasks_view"),
    path("customers_view/<int:customer_info_id>", views.customers_info, name="customers_info"),
    path("edit_customer_info_box", views.edit_customer_info_box, name="edit_customer_info_box"),
    path("tasks_view/<int:task_info_id>", views.task_info, name="task_info"),
    path("task_done", views.task_done, name="task_done"),
    path("tasks_archive", views.tasks_archive, name="tasks_archive")
]