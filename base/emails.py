from django.conf import settings
from django.core.mail import send_mail




def send_account_activation_email(email ,token):

    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{token}'
    send_mail(subject , message , email_from , [email])


def send_payment_confirmation_email(email, cart, total_amount):
    username = cart.cart_owner.user.username
    subject = 'Order Confirmation'
    email_from = settings.EMAIL_HOST_USER
    message = f'''Thank you for your order #{username}!
    
Your payment of ${total_amount} has been confirmed.

You can track your order here: http://127.0.0.1:8000/products/api/cart/

Best regards,
Your Store Team'''
    send_mail(subject, message, email_from, [email])