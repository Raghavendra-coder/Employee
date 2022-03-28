from django.urls import path
from . import views


urlpatterns = [
    path('leave-request/', views.LeaveRequest.as_view()),
    path('employee-detail/<pk>/', views.EmployeeDetail.as_view()),
    path('employee-detail/', views.EmployeeDetail.as_view()),
    path('employee-list/', views.EmployeeList.as_view()),
]