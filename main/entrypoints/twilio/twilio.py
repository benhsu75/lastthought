from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def twilio_callback(request):
    print '=============RECEIVED TWILIO TEXT============'
    print request.POST