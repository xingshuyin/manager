from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import View
from .models import User, Token
from tools.tools import secret
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'index/index.html')


class login(View):

    def get(self, request):
        return render(request, 'index/login.html')

    def post(self, request):
        print(request.POST)
        verify = request.POST.get('verify')
        name = request.POST.get('name')
        password = request.POST.get('password')
        if u := User.objects.filter(name=name, password=password):
            request.session['user'] = u[0].name
            return HttpResponseRedirect(reverse('index'))
        return JsonResponse({'status': 'false'})


class change(View):
    def get(self, request):
        return render(request, 'index/change.html')

    def put(self, request):
        print(request.POST)
        name, password, new_password = request.POST
        user = get_object_or_404(User, name=name, password=password)
        user.password = new_password
        user.save()
        return HttpResponseRedirect(reverse('index'))


class signup(View):
    template_name = 'index/signup.html'

    def get(self, request):
        return render(request, 'index/signup.html')

    def post(self, request):
        name, password, code = request.data['name', 'password', 'code']
        u = User.objects.create(name=name, password=password)
        return JsonResponse({'status': 'success'})


def logout(request):
    request.session['user']=None
    return HttpResponseRedirect(reverse('login'))
