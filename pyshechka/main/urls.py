from django.urls import path
from .views import ChangeUserInfoView
from .views import DeleteUserView
from .views import index
from .views import other_page
from .views import PortionCreateView
from .views import ProductCreateView
from .views import ProductDeleteView
from .views import ProductDetailView
from .views import ProductList
from .views import profile
from .views import PyLoginView
from .views import PyLogoutView
from .views import PyPasswordChangeView
from .views import PyPasswordResetConfirmView
from .views import PyPasswordResetView
from .views import RegisterDoneView
from .views import RegisterUserView
from .views import user_activate

app_name = 'main'
urlpatterns = [
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/password/reset/<uidb64>/<token>/', PyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password/reset/', PyPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password/change/', PyPasswordChangeView.as_view(), name='password_change'),
    path('accounts/logout/', PyLogoutView.as_view(), name='logout'),
    path('accounts/login/', PyLoginView.as_view(), name='login'),
    path('product/all/', ProductList.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('portion/create/', PortionCreateView.as_view(), name='portion_create'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
