from django.shortcuts import render, redirect
from .models import User, Dava, Surec, Dosyalar

from django.contrib.auth import logout

from django.http import JsonResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated:

        if request.is_ajax():
            myfile = request.FILES.getlist('myfile')
            dosyaadi = request.POST.get('dosyaadi')
            dosyaaciklamasi = request.POST.get('dosyaaciklamasi')
            dosyadavasi = request.POST.get('dosyadavasi')

            dosyadavasi1 = Dava.objects.get(pk=dosyadavasi)

            for i in myfile:
                dosya = Dosyalar(user=request.user, dava=dosyadavasi1, dosya_adi=dosyaadi, dosya_aciklamasi=dosyaaciklamasi, dosya_dosyasi=i)
                dosya.save()

            return JsonResponse({'mesaj' : 'basarili'})

        u = User.objects.get(id= request.user.id)
        davalar= u.dava_set.all()
        context = { 'davalar' : davalar }
        return render(request, 'muvekkil/index.html', context)
    else:
        return redirect('login')

def davadetay(request, id):

    if request.user.is_authenticated:
        user = request.user
        davalar = user.dava_set.all()
        dava_ids = []

        for dava in davalar:
            dava_ids.append(dava.id)

        if id in dava_ids:
            davaGetir = Dava.objects.get(id=id)
            surecGetir = davaGetir.surec_set.all()
            context = {'dava' : davaGetir,
                       'surecler' : surecGetir}
            return render(request, 'muvekkil/davadetay.html', context)

        else:
            return redirect('/')

    else:
        return redirect('login')

def auth_logout(request):
    logout(request)
    return redirect('/login/?giris=basarilicikis')

from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
    response = render_to_response('muvekkil/404.html', {},
                              RequestContext(request))
    response.status_code = 404
    return response