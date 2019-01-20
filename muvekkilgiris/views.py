from django.shortcuts import render, redirect
from muvekkil.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def login(request):


        """
        try:
            m = User.objects.get(email= request.POST['email'])
            print(m)
            print(request.POST['pass'])
        except User.DoesNotExist:

            from django.contrib import messages

            messages.add_message(request, messages.ERROR, 'Böyle Bir Kullanıcı Bulunmuyor.')

            return render(request, 'muvekkilgiris/index.html')
        """
        if request.user.is_authenticated:
            return redirect('/')

        if (request.method == "POST"):
            email = request.POST['email']
            password = request.POST['pass']

            user = authenticate(email= email, password= password)
            if user is not None:
                request.session.set_expiry(86400)
                auth_login(request, user)

                return redirect('/?giris=olumlu')
            else:
                return redirect('/login/?giris=olumsuz')

        return render(request, 'muvekkilgiris/index1.html')