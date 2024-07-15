# blog/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),  # URL para la vista de inicio de sesión
    path('register/', views.register, name='register'),  # URL para la vista de registro
    path('logout/', views.logout_view, name='logout'),  # URL para la vista de cierre de sesión
    path('pages/', views.pages_list, name='pages_list'),
    path('pages/<int:page_id>/', views.page_detail, name='page_detail'),
    path('pages/<int:page_id>/edit/', views.page_edit, name='page_edit'),
    path('pages/<int:page_id>/delete/', views.page_delete, name='page_delete'),
    path('pages/create/', views.page_create, name='page_create'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]