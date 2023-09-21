from django.urls import path
# from .views import DeleteUserView
from lunches.views import LunchDetailView
urlpatterns = [
    # path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
]