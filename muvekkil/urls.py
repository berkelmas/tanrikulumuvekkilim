from django.urls import path
from .views import home, davadetay, auth_logout

urlpatterns = [
    path('', home, name="index"),
    path('davadetay/<int:id>/', davadetay, name="davadetay"),
    path('logout/', auth_logout, name='logout')
]