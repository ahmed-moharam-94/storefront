from django.core.cache import cache
from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
import requests

class HelloView(APIView):
    @method_decorator(cache_page(10 * 60))
    def get(self, request):
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        return render(request, "hello.html", {"name": data}) 
    


# @cache_page(5 * 60)
# def say_hello(request):
#     #     try:
#     #         send_mail(subject='subject', message='message', from_email='from@test.com',
#     #                   html_message= 'message',
#     #                 recipient_list=['recipient_1@test.com',
#     #                     'recipient_2@test.com',
#     #                     ],
#     #                 )
#     #         mail_admins('subject', 'message', html_message= 'message')

#     #         message = EmailMessage(
#     #             subject='subject',
#     #             body='message',
#     #             from_email='from@test.com',
#     #             to=['test_5@test.com']
#     #         )
#     #         message.attach_file('playground/static/images/example.jpg')
#     #         message.send()

#     #         message = BaseEmailMessage(
#     #             template_name='emails/hello.html',
#     #             # used to pass data to our template
#     #             context={'name': "Moharam"}
#     #         )
#     #         message.send(['moharam@test.com'])
#     #     except BadHeaderError:
#     #         pass

#     # background task example
#     # notify_customers.delay('Test Message')

#     # low-level cache API
#     # key = "httpbin_result"
#     # if cache.get(key) is None:
#     #     # simulate a slow endpoint
#     #     response = requests.get("https://httpbin.org/delay/2")
#     #     data = response.json()
#     #     cache.set(key, data, 10 * 600)
    
#     # use cache decorator
#     response = requests.get("https://httpbin.org/delay/2")
#     data = response.json()
#     return render(request, "hello.html", {"name": data}) 
