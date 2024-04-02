from celery import shared_task
from smtplib import SMTPException
import datetime
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q


from .models import Order


@shared_task(bind=True)
def send_order_confirmation_mail(self, target_mail, created_at):
    # may add the same mail exception handling as in send_remainder()
    send_mail(
        subject = 'Order confirmation',
        message=f'Order created at: {created_at.strftime("%Y-%m-%d %H:%M")}',
        from_email=settings.EMAIL_DEFAULT_FROM,
        recipient_list=[target_mail],
        fail_silently=False,
    )



@shared_task(bind=True)
def send_payment_remainder_mail(self):
    # send remainder one day before payment_deadline 
    notify_deadline = datetime.datetime.now() + datetime.timedelta(days=1)
    orders = Order.objects.filter(
        Q(
            Q(remainder_sent=False) & 
            Q(payment_deadline__date__lte=notify_deadline.date())  
         
        ) | 
        Q(remainder_force=True)
    )
    c = 0
    if orders.count() == 0:
        return 'no emails to send'
    for order in orders:
        try:
            send_mail(
                subject = 'Payment remainder',
                message=(
                    f'Order created at: {order.created_at.strftime("%Y-%m-%d %H:%M")}.\n'
                    f'Payment deadline: {order.payment_deadline.strftime("%Y-%m-%d %H:%M")}.'
                    ),
                from_email=settings.EMAIL_DEFAULT_FROM,
                recipient_list=[order.client.email],
                fail_silently=False,
            )
            

        except BadHeaderError:              # If mail's Subject is not properly formatted.
            return 'Invalid header found.'
        except SMTPException as e:          # It will catch other errors related to SMTP.
            return f'There was an error sending an email.\n {e}'
        except:                             # It will catch All other possible errors.
            return 'Mail Sending Failed!'
        order.remainder_sent = True
        order.remainder_force = False
        order.save()
        c += 1
    return f'{c} remainders sent' if c > 1 else f'{c} remainder sent'