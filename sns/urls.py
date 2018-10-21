from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('top', views.top, name='top'),
    path('board', views.board, name='board'),
    path('board/<int:num>', views.board, name='board'),
    path('post', views.post, name='post'),
    path('good/<int:good_id>', views.good, name='good'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='sns/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('news', views.news, name='news'),
    path('ranking', views.ranking, name='ranking')
]

