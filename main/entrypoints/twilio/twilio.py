from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def twilio_callback(request):
    print '=============RECEIVED TWILIO TEXT============'
    print request.POST

    return HttpResponse(status=200)