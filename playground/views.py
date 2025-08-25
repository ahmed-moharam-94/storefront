from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
import requests


def say_hello(request):
#     try:
#         send_mail(subject='subject', message='message', from_email='from@test.com',
#                   html_message= 'message',
#                 recipient_list=['recipient_1@test.com',
#                     'recipient_2@test.com',
#                     ],
#                 )
#         mail_admins('subject', 'message', html_message= 'message')

#         message = EmailMessage(
#             subject='subject',
#             body='message',
#             from_email='from@test.com',
#             to=['test_5@test.com']
#         )      
#         message.attach_file('playground/static/images/example.jpg')
#         message.send()

#         message = BaseEmailMessage(
#             template_name='emails/hello.html',
#             # used to pass data to our template
#             context={'name': "Moharam"}
#         )
#         message.send(['moharam@test.com'])
#     except BadHeaderError:
#         pass       


    # background task example
    # notify_customers.delay('Test Message')

    # simulate a slow endpoint
    requests.get('https://httpbin.org/delay/2')
    return render(request, 'hello.html', {'name': 'Mosh'})
