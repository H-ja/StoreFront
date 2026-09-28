from time import sleep
# celery automatically discovers this module
# we should decorate this function with one of celery decorators

# first_way(tutorials)
# from storefront.celery import celery as cl
# @cl.task
# def notify_customers(message):
#     print('sending 10k email...')
#     print(message)
#     sleep(10)
#     print('Emails were successfully sent!')

# problem: playground app is dependent on storefront app

# second way
from celery import shared_task
@shared_task
def notify_customers(message):
    print('sending 10k email...')
    print(message)
    sleep(10)
    print('Emails were successfully sent!')
