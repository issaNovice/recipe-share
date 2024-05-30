from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"), 
    path('home/', views.home, name="home"),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('post_meep/', views.post_meep, name="post_meep"), 
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('meep_like/<int:pk>', views.meep_like, name="meep_like"),
    path('meep_show/<int:pk>', views.meep_show, name="meep_show"),
    path('delete_meep/<int:pk>', views.delete_meep, name="delete_meep"),
    path('search/', views.search, name='search'),
    path('liked_posts/', views.liked_posts, name='liked_posts'),
]
