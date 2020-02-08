from random import randint

from django.shortcuts import render

# from sms.models import OFO_user
# from sms.utils import send_matching_sms
#
#
# def send_sms(request):
#     user1 = OFO_user()
#     user1.phone = "01023071821"
#     send_matching_sms(user1)
from sms.models import AuthSms
from sms.utils import AuthSmsSendView


def send_sms(request):
    assv = AuthSmsSendView()
    assv.send_sms("01071497833", "1234")


def certificate_phone(request):
    assv = AuthSmsSendView()
    assv.post(request, request.user.profile.phone_number)


def certificate_phone_done(request):
    if request.POST.get('auth_number_input') == AuthSms[request.user.profile.phone_number]:
        return render(request, 'sms/certificate_phone_done')