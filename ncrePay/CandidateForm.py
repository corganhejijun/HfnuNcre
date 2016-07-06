# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

import csv

from .models import Candidate


class CandidateForm(forms.Form):
    username = forms.CharField(
        label=u'用户名',
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        ),
    )

    name = forms.CharField(
        label=u'姓名',
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        ),
    )

    def logout(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))

    def candidateList(self, page):
        pageNum = int(page)
        querySet = Candidate.objects.filter(paidTime='', teacher__isnull=True)
        i = pageNum * 20
        canlist = []
        for item in querySet:
            i += 1
            if i >= (pageNum + 1) * 20:
                break
            can = {}
            can['id'] = item.id
            can['candidateNum'] = item.candidateNum
            can['name'] = item.name
            canlist.append(can)
        return canlist

    def get(self, request):
        if not request.user.is_authenticated():
            return self.logout(request)
        target = request.GET.get('target')
        if target:
            return JsonResponse(self.candidateList(target), safe=False)
        return render(request, 'ncrePay/index.html')

    def post(self, request):
        if 'logout' in request.POST:
            return self.logout(request)
