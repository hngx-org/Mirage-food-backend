
from django.urls import path
from .views import SearchUserView

urlpatterns = [
	path('search/<str:name_or_email>/', SearchUserView, name='search-user'),
]