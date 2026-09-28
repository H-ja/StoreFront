# running docker server --> cmd: docker run --rm -it -p 3000:80 -p 2525:25 rnwood/smtp4dev

from django.shortcuts import render
# BOTH send_mail and mail_admins inherit from EmailMessage class
from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
# django.core.mail methods:
# mail_admins
# mail_managers
# send_mail --> starts a new connection for each mail
# send_mass_mail --> starts one connection and send all mails through that connection

# using django_templated_mail
from templated_mail.mail import BaseEmailMessage

# using celery
from .tasks import notify_customers


def say_hello(request):
    # try:
    #     both methods have an argument < html_message > which is html_content
    #     send_mail('subject', 'message', 'info@moshbuy.com', ['bob@moshbuy.com'], html_message='some html message 1')
    #     mail_admins('subject', 'message', html_message='some html message 2')
    #     NOTE: using mail_admins we should specify the admin in settings.py
    #     NOTE: first html_message is shown then plain_text if html_message was not readable for user --> devices with less functionality

    #     send_mail or mail_admins methods are shortcuts to all these:
    #     =================================================================================================
    #     using EmailMessage class for custom email sending methods with file attachment and other features
    #     message = EmailMessage('subject', 'message', 'from@moshbuy.com', ['john@moshbuy.com'])
    #     message.attach_file('playground/static/images/test.png')
    #     NOTE: path should be relavent to current project
    #     message.send()
    #     =================================================================================================

    #     installing django-templated-mail for optimizations in emails body('message')

    # except BadHeaderError:
    #     pass

    # try:
        # # context is the data we want to pass to html file
        # message = BaseEmailMessage(template_name='emails/hello.html', context={'name': 'Hamid'})
        # message.send(to=['john@moshbuy.com'])

    # except:
    #     pass

    # using < CELERY >: completing task in parrarel so client doesn't need to be waiting for an action like sending videos to complete
    # so we just announce the user when the task is completed and run these tasks in BACKGROUND

    # MESSAGE BROKER(middleman) --> passing messages between applications in a reliable way
    # reliable way: for example it transfers a message form app A to app B
    # now if app B is unavailable message broker will keep that message and tries sending it again
    # problem: what if a message broker goes down itself?
    # answer: we will use several message brokers in case one goes down others will replace 

    # some popular brokers for django apps:
    # 1. Redis: actually this is not a message broker but an 'in memory data store' so we can either
    # use it as a database, cache, or message_broker
    # 2. RabbitMQ: is a real message_broker and has many extra features that Redis doesn't have but it is costly

    # installing Redis with docker:
    # docker run -d(detached_mode: in the background) -p(port_mapping: from local host to Redis)
    # cmd: docker run -d -p 6379:6379 redis
    # NOTE: 6379 is the standart port that Redis listens on

    notify_customers.delay('Hello')


    return render(request, 'index.html', {'name': 'Hamid'})
