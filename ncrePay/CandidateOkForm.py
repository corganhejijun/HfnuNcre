# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Apply, Candidate


class CandidateOkForm(forms.Form):
    def post(self, request):
        return HttpResponseRedirect(reverse('apply'))

    def get(self, request):
        canId = request.GET.get('can')
        teaId = request.GET.get('tea')
        try:
            app = Apply.objects.get(candidate__id=canId, teacher__id=teaId)
        except:
            return HttpResponseRedirect(reverse('apply'))
        querySet = Candidate.objects.filter(candidateNum=app.candidate.candidateNum)
        return render(request, 'ncrePay/candidateOk.html',
            {'name': app.candidate.name,
            'id': app.candidate.candidateNum[-4:],
            'number': len(querySet) * 80,
            'alipay': app.teacher.alipayQr})
