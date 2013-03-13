from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if new_user is not None and new_user.is_active:
                auth.login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", 
                              {'form': form})
    
#def login(request):
#    username = request.POST.get('username', '')
#    password = request.POST.get('password', '')
#    user = auth.authenticate(username=username, password=password)
#    if user is not None and user.is_active:
#        # Correct password, and the user is marked "active"
#        auth.login(request, user)
#        # Redirect to a success page.
#        return HttpResponseRedirect("/")
#    else:
#        # Show an error page
#        return HttpResponseRedirect("/account/invalid/")