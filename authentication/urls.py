from practice.views import UserRegistration,UserLogin,UserProfile,UserChangePassword,SendPasswordResetEmail,ResetPassword
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',UserRegistration.as_view()),
    path('login/',UserLogin.as_view()),
    path('profile/',UserProfile.as_view()),
    path('changepassword/',UserChangePassword.as_view()),
    path('sendresetemail/',SendPasswordResetEmail.as_view()),
    path('resetpassword/<uid>/<token>/',ResetPassword.as_view())
]
