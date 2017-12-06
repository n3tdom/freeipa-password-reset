# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.template import loader
from django.utils.safestring import mark_safe

from pwdmanager import *

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

class GetToken(View):
    def post(self, request, *args, **kwargs):
        try:
            PasswdManager().first_phase(request.POST['uid'])
        except Exception as e:
            template = loader.get_template('index.html')
            context = {
                'msg': e,
                'error': True
            }
            return HttpResponse(template.render(context, request))
        else:
            return redirect("/reset/setpassword/?uid={0}".format(request.POST['uid']))


class SetPassword(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('setpassword.html')
        context = {
            'uid': request.GET['uid']
        }
        return HttpResponse(template.render(context, request))
    
    def post(self, request, *args, **kwargs):
        try:
            PasswdManager().second_phase(request.POST['uid'], request.POST['token'], request.POST['password1'])
        except Exception as e:
            template = loader.get_template('setpassword.html')
            context = {
                'msg': e,
                'error': True,
                'uid': request.POST['uid']
                
            }
        else:
            template = loader.get_template('setpassword.html')
            context = {
                'msg': mark_safe('Password successfully changed. <a href="/ipa/ui/">You can login here.</a>'),
                'error': False,
                'uid': request.POST['uid']
                
            }
        return HttpResponse(template.render(context, request))
