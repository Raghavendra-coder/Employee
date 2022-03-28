from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('employee-signup', views.employee_signup, name='employee_signup'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('leave-request', views.leave_request, name='leave_request'),
    path('logout', views.user_logout, name='user_logout'),
]
