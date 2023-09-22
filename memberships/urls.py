from django.urls import path
from . import views

app_name = 'memberships'  # Add your app name here

urlpatterns = [
    path('api/profile/', views.profile_view, name='profile'),
    path('api/memberships/', views.MembershipSelectView.as_view(), name='membership-list'),
    path('api/payment/', views.payment_view, name='payment'),
    path('api/update-transactions/<str:subscription_id>/', views.update_transaction_records, name='update-transactions'),
    path('api/cancel-subscription/', views.cancel_subscription, name='cancel-subscription'),
]