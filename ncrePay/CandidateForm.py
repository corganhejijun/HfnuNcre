# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from SendMail import sendMail

from .models import Apply, Teacher, Candidate


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
        querySet = Apply.objects.filter(teacher__isnull=True)
        i = pageNum * 20
        canlist = []
        for item in querySet:
            if '@' not in item.email:
                continue
            i += 1
            if i > 100:
                break
            can = {}
            can['id'] = item.candidateNum
            can['candidateNum'] = item.candidateNum
            can['name'] = item.name
            can['email'] = item.email
            canlist.append(can)
        return canlist

    def get(self, request):
        if not request.user.is_authenticated():
            return self.logout(request)
        target = request.GET.get('target')
        if target:
            return JsonResponse(self.candidateList(target), safe=False)
        return render(request, 'ncrePay/index.html', {'username': request.user.get_username()})

    def post(self, request):
        if 'logout' in request.POST:
            return self.logout(request)
        if not request.user.is_authenticated():
            return self.logout(request)
        acceptId = ""
        for n, v in request.POST.iteritems():
            if n.startswith('accept'):
                acceptId = n[6:]
        if len(acceptId) == 0:
            return HttpResponseRedirect(reverse('index'))
        applyItem = Apply.objects.filter(candidateNum=acceptId)
        teacherName = request.user.get_username()
        try:
            teacher = Teacher.objects.get(username=teacherName)
        except Exception, e:
            print str(e)
            return self.logout(request)
        for item in applyItem:
            item.teacher = teacher
            item.status = "teacher"
            title = item.candidateNum[-4:] + item.name + u" 计算机等级考试报名"
            text = u"你的报名信息正由 " + teacher.name + u" 老师审核中，报名人数较多请耐心等待\n本邮件由系统自动发送，请勿回复"
            sendMail(item.email, title, text)
            item.save()
        return HttpResponseRedirect(reverse('index'))
