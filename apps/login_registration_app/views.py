from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'login_registration_app/index.html')

def register(request):
    response = User.objects.validation(request.POST)
    print response
    
    if len(response):
        for tag,error in response.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('index')

    if User.objects.validation(request.POST):
        errorFlag = True
        return redirect ('success')
    else:
        errorFlag = False
        return redirect('index')

def success(request):
    if 'user_id' not in request.session :
        return redirect('index')

    return render(request, 'login_registration_app/success.html')

def login(request):
    response = User.objects.verifyUserLogin(request.POST)
    if response['errorFlag'] == True:
        for tag,error in response.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect ('index')
    else:
        for tag, error in response.iteritems():
            messages.error(request, error, extra_tags=tag)
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        print "user id: ", request.session['user_id']
        return redirect ('success')

def logout(request):
    print "session at the beginning of logout: ", request.session
    request.session.flush()
    print "session at the end of logout: ", request.session
    return redirect ('index')

