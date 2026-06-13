from django.urls import path
from .views import (
    PaymentListCreateView,
    PaymentDetailView,
    payment_history,
    simulate_payment,
)


urlpatterns = [
    path("", PaymentListCreateView.as_view(), name="payment-list-create"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("history/", payment_history, name="payment-history"),
    path("simulate/<int:enrollment_id>/", simulate_payment, name="simulate-payment"),
]