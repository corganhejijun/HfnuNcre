# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from SendMail import sendMail

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
        canList['photo'] = 'http://jdjks.hfnu.edu.cn/wp/340051/' + item.photoName + ".jpg"
        querySet = Candidate.objects.filter(candidateId=item.candidateId)
        canList['testName'] = u'报考科目：'
        for item in querySet:
            canList['testName'] += ' ' + item.testName
        canList['testCnt'] = len(querySet)
        return canList

    def renderList(self, request):
        username = request.user.get_username()
        querySet = Apply.objects.filter(teacher__username=username).exclude(status='success')
        return render(request, 'ncrePay/myList.html', {'username': username, 'list': querySet})

    def get(self, request):
        if not request.user.is_authenticated():
            return self.logout(request)
        target = request.GET.get('target')
        if target:
            # target = accept'xxxx'
            return JsonResponse(self.getCandidate(int(target[6:])), safe=False)
        return self.renderList(request)

    def post(self, request):
        acceptId = -1
        for n, v in request.POST.iteritems():
            if n.startswith('accept'):
                acceptId = int(n[6:])
        if acceptId == -1:
            return HttpResponseRedirect(reverse('index'))
        try:
            app = Apply.objects.get(candidate__id=acceptId)
        except:
            return HttpResponseRedirect(reverse('index'))
        title = app.candidate.candidateNum[-4:] + app.candidate.name + u" 计算机等级考试报名"
        if 'infoOk' in request.POST:
            text = u'报名信息审核通过，查看支付方式请点击下方网址：\n'\
                + u'http://jdjks.hfnu.edu.cn/ncre/candidateOk/?can=' + str(app.candidate.id) + u'&tea=' + str(app.teacher.id)
            sendMail(app.email, title, text)
            app.status = 'success'
            app.save()
        else:
            text = ""
            if 'photoError' in request.POST:
                text += u'照片不合格，请使用正规证件照\n'
            if 'noTel' in request.POST:
                text += u'未输入联系方式\n'
            if 'otherError' in request.POST:
                text += request.POST['otherError'] + '\n'
            if len(text) > 1:
                text = u'报名信息审核不合格，存在以下问题：\n' + text + u'请修改后重新提交审核'
                sendMail(app.email, title, text)
                app.status = 'reject'
                app.save()
        return self.renderList(request)

    def getSuccessList(self, request):
        username = request.user.get_username()
        querySet = Apply.objects.filter(teacher__username=username, status='success')
        return render(request, 'ncrePay/myList.html', {'username': username, 'list': querySet, 'success': True})

    def postSuccessList(self, request):
        acceptId = -1
        for n, v in request.POST.iteritems():
            if n.startswith('accept'):
                acceptId = int(n[6:])
        if acceptId == -1:
            return HttpResponseRedirect(reverse('index'))
        try:
            app = Apply.objects.get(candidate__id=acceptId)
        except:
            return HttpResponseRedirect(reverse('index'))
        title = app.candidate.candidateNum[-4:] + app.candidate.name + u" 计算机等级考试报名"
        text = u'缴费成功，报名结束，请登录系统查看缴费状态，如果仍显示“未支付”，请回复此邮件。否则请勿回复此封系统自动发送的邮件。'
        sendMail(app.email, title, text)
        app.status = 'paid'
        app.save()
        self.getSuccessList(request)
