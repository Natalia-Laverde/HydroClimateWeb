from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the odm2admin index.")