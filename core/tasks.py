from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email(order_id, email):
    order = Order.objects.get(id=order_id)
    subject = f"Order Confirmation - #{order.order_number}"
    message = f"Thank you for your order!\n\nOrder Number: {order.order_number}\nTotal: ${order.total_price}\n\nWe'll notify you when your order ships."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )