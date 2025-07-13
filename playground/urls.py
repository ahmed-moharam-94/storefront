from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # path takes a string the path that will be called & the view function that will be excuted 
    # when this path is called (we only pass a refernce to this function not calling the function)
    path("hello/", views.say_hello)
]

