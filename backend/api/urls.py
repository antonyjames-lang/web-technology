from django.urls import path
from . import views

urlpatterns = [
    path('taxonomy', views.get_taxonomy, name='taxonomy'),
    path('auth/request-otp', views.request_otp, name='request_otp'),
    path('auth/verify-otp', views.verify_otp, name='verify_otp'),
    path('me', views.get_current_user, name='get_current_user'),
    path('me/profile', views.update_profile, name='update_profile'),
    path('me/saved/<str:slug>', views.toggle_saved_scheme, name='toggle_saved_scheme'),
    path('schemes', views.get_schemes, name='get_schemes'),
    path('schemes/<str:slug>', views.get_scheme_detail, name='get_scheme_detail'),
]
