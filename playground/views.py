from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    try:
        send_mail(subject='subject', message='message', from_email='from@test.com',
                  html_message= 'message',
                recipient_list=['recipient_1@test.com',
                    'recipient_2@test.com',
                    ],
                )
        mail_admins('subject', 'message', html_message= 'message')

        message = EmailMessage(
            subject='subject',
            body='message',
            from_email='from@test.com',
            to=['test_5@test.com']
        )      
        message.attach_file('playground/static/images/example.jpg')
        message.send()
    except BadHeaderError:
        pass       
    return render(request, 'hello.html', {'name': 'Mosh'})
