from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('share/<int:share_id>', views.share, name='share'),
    path('good/<int:good_id>', views.good, name='good'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='sns/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('test', views.test, name='test'),
]

