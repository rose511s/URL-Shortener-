from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('example/<slug:name>', example_view),
    path('task/', task_view),
    path('', shorten_url, name="Home"),
    path('all_analytics', all_analytics, name="Analytics"),
    path('login', loginFunc, name="Login"),
    path('register', registerFunc, name="Register"),
    path('logout', logoutFunc, name="Logout"),
    path('<slug:shorturl>', redirect_url),
    path('<slug:short_url>/analytics', analytics),
]
# slug very important feature
