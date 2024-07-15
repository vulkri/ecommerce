from celery import shared_task
from smtplib import SMTPException
import datetime
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.db.models import Q


from .models import Order


@shared_task(bind=True)
def send_order_confirmation_mail(self, target_mail, created_at):
    """
    Sends an order confirmation email to the specified email address.
    
    Args:
        target_mail (str): The email address to send the confirmation to.
        created_at (datetime.datetime): The datetime the order was created.
    
    Returns:
        str: A message indicating the result of the email send operation. Possible return values are:
            - 'Mail sent successfully.'
            - 'Invalid header found.'
            - 'There was an error sending an email.'
            - 'Mail Sending Failed.'
    """
    try:
        send_mail(
            subject = 'Order confirmation',
            message=f'Order created at: {created_at.strftime("%Y-%m-%d %H:%M")}',
            from_email=settings.EMAIL_DEFAULT_FROM,
            recipient_list=[target_mail],
            fail_silently=False,
        )
        return 'Mail sent successfully.'
    except BadHeaderError:              # If mail's Subject is not properly formatted.
        return 'Invalid header found.'
    except SMTPException as e:          # It will catch other errors related to SMTP.
        return f'There was an error sending an email.\n {e}'
    except:                             # It will catch All other possible errors.
        return 'Mail Sending Failed.'



@shared_task(bind=True)
def send_payment_remainder_mail(self):
    """
    Sends a payment remainder email to clients who have an order with a payment deadline within the next day, and have not yet received a remainder email.
    
    This task is executed asynchronously using Celery. It queries the Order model to find all orders that meet the following criteria:
    - The order's `remainder_sent` flag is False, and the order's `payment_deadline` is within the next 24 hours.
    - The order's `remainder_force` flag is True, regardless of the `remainder_sent` flag or payment deadline.
    
    For each qualifying order, it sends an email to the client with the order creation date and payment deadline. After the email is sent successfully, the `remainder_sent` flag is set to True and the `remainder_force` flag is set to False.
    
    The function returns a message indicating the number of remainder emails sent, or 'no emails to send' if there are no qualifying orders.
    
    Args:
        self (celery.Task): The Celery task instance.
    
    Returns:
        str: A message indicating the result of the email send operation.
    """

    notify_deadline = datetime.datetime.now() + datetime.timedelta(days=1)
    orders = Order.objects.filter(
        Q(
            Q(remainder_sent=False) & 
            Q(payment_deadline__date__lte=notify_deadline.date())  
         
        ) | 
        Q(remainder_force=True)
    )
    emails_sent_count = 0
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
            return 'Mail Sending Failed.'
        order.remainder_sent = True
        order.remainder_force = False
        order.save()
        emails_sent_count += 1
    return f'{emails_sent_count} remainders sent' if emails_sent_count > 1 else f'{emails_sent_count} remainder sent'