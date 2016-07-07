# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from .models import Apply, Candidate


class MyListForm(forms.Form):
    def logout(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))

    def getCandidate(self, target):
        querySet = Candidate.objects.filter(id=target)
        item = querySet[0]
        canList = {}
        canList['name'] = item.name
        canList['candidateNum'] = item.candidateNum
        canList['phone'] = item.phone
        canList['id'] = item.candidateId
        canList['photo'] = 'http://jdjks.hftc.edu.cn/wp/340051/' + item.photoName + ".jpg"
        querySet = Candidate.objects.filter(candidateId=item.candidateId)
        canList['testName'] = u'报考科目：'
        for item in querySet:
            canList['testName'] += ' ' + item.testName
        canList['testCnt'] = len(querySet)
        return canList

    def get(self, request):
        if not request.user.is_authenticated():
            return self.logout(request)
        target = request.GET.get('target')
        if target:
            return JsonResponse(self.getCandidate(int(target)), safe=False)
        username = request.user.get_username()
        querySet = Apply.objects.filter(teacher__username=username)
        return render(request, 'ncrePay/myList.html', {'username': username, 'list': querySet})

    def post(self, request):
        acceptId = -1
        for n, v in request.POST.iteritems():
            if n.startswith('accept'):
                acceptId = int(n[6:])
        if acceptId == -1:
            return HttpResponseRedirect(reverse('index'))
        querySet = Candidate.objects.filter(id=acceptId)
        return render(request, 'ncrePay/myList.html', {''})
