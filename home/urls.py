from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("",views.register,name='register'),
    path("student_register",views.student_register,name="student_register"),
    path("login",views.login,name="login"),
    path("teacher_register",views.teacher_register,name="teacher_register"),
    path("person_register",views.person_register,name="person_register"),
    path("verification",views.verification,name="verification"),
    path('register',views.register,name="register"),
    path('password_validation',views.password_validation, name="password_validation"),
    path('password_verify',views.password_verify,name="password_verify"),
    path('forgot_password',views.forgot_password, name="forgot_password"),
]
