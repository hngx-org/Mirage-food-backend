from django.urls import path
from users import views

urlpatterns = [
    path('<pk>', views.get_user, name='get_user'),
]