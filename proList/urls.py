from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name="register"),
    path('newtask', views.newtask, name="newtask"),
    path('endtask',views.endtask, name="endtask"),
    path('addreminder',views.addreminder, name="addreminder"),
    path('endreminder',views.endreminder,name="endreminder"),
    path('taskgroup', views.taskgroup, name="taskgroup"),
    path('export', views.export, name="export"),
]