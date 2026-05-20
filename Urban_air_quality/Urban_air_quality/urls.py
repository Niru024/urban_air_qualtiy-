from django.contrib import admin
from django.urls import path
from login import views
from dashboard import views as dashboard_views

urlpatterns = [
    path('', views.landing_page, name='home'),

    path('admin/', admin.site.urls),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register_view, name='register'),

    path('profile/', views.profile_view, name='profile'),

    path('aqi-map/', views.aqi_map, name='aqi_map'),

    path('landing-page/', views.landing_page, name='landing_page'),

    path('help/', views.help_page, name='help'),

    path('about/', views.about_page, name='about'),

    path('dashboard/', dashboard_views.dashboard, name='dashboard'),

    path('map/', dashboard_views.map_view, name='map'),

    path('api/aqi/', dashboard_views.api_aqi, name='api_aqi'),
]