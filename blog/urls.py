from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('session/', views.session_status, name='session_status'),
    path('session/clear/', views.clear_session, name='clear_session'),
    path('testcookie/', views.cookie_session, name='testcookie'),
    path('deletecookie/', views.cookie_delete, name='deletecookie'),
    path('create/', views.create_session, name='create_session'),
    path('access/', views.access_session, name='access_session'),
    path('delete/', views.delete_session, name='delete_session'),
    path('flush/', views.flush_session, name='flush_session'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),  
    path("logout", views.logout_request, name="logout"), 
    path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]
