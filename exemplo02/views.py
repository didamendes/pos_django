from django.http import HttpResponse


def index(request):
    return HttpResponse("AGORA EH EXEMPLO 02.")