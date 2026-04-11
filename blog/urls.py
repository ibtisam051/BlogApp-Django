from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),  
    path("logout", views.logout_request, name="logout"), 
]
