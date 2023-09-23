from django.urls import path
from .views import LoginView
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView, UserViewSet
from lunches.views import LunchDetailView
from .views import SearchUserView
from .views import UserRegistrationView, UserDetailView


urlpatterns = [
    path('organization/<int:org_id>/user/<int:user_id>', UserViewSet.as_view, name='get-org_user'),
    path("users/all", UserListViewSet.as_view(), name="users-list"),
    path("users/<int:id>/", DeleteUserView.as_view()),
    path(
        "users/<int:user_id>/lunches/<int:lunch_id>",
        LunchDetailView.as_view(),
        name="lunch-detail",
    ),
    path("search/<str:name_or_email>/", SearchUserView.as_view(), name="search-users"),
    path("auth/user/signup/", UserRegistrationView.as_view(), name="user-signup"),
    path("users/login/", LoginView.as_view(), name="login"),
    path("user/profile/<int:user_id>/", UserDetailView.as_view(), name="user-profile"),
]
