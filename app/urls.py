from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from app import views
from .views import EventDetailView, payment_view


urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('create_event/', views.create_event, name='create_event'),
    path('upgrade_seller/', views.upgrade_seller, name='upgrade_seller'),
    path('event_page/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('category/<str:category_name>', views.category_view, name='category_view'),
    path('seller/', views.seller_application_view, name='seller'),
    path('availability/<int:event_id>', views.available_page, name='availability'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('create-payment/', views.create_payment, name="create_payment"),
    path('verify-payment/', views.verify_payment, name="verify_payment"),
    path('about/', views.about, name='about'),
]


urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)