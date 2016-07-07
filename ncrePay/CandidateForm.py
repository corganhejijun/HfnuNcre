# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

from .models import Apply, Teacher


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
            i += 1
            can = {}
            can['id'] = item.candidate.id
            can['candidateNum'] = item.candidate.candidateNum[-4:]
            can['name'] = item.candidate.name
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
        acceptId = -1
        for n, v in request.POST.iteritems():
            if n.startswith('accept'):
                acceptId = int(n[6:])
        if acceptId == -1:
            return HttpResponseRedirect(reverse('index'))
        applyItem = Apply.objects.filter(candidate__id=acceptId)
        teacherName = request.user.get_username()
        try:
            teacher = Teacher.objects.get(username=teacherName)
        except:
            return self.logout(request)
        for item in applyItem:
            item.teacher = teacher
            item.status = "teacher"
            title = item.candidate.candidateNum[-4:] + item.candidate.name
            text = u"你的报名信息正由" + teacher.name + u"老师审核中，报名人数较多请耐心等待\n本邮件由系统自动发送，请勿回复"
            self.sendMail(item.email, title, text)
            item.save()
        return HttpResponseRedirect(reverse('index'))

    def sendMail(self, dest, title, text):
        mailInfo = {
            "from": "JijunHe@qq.com",
            "to": dest,
            "hostname": "smtp.qq.com",
            "username": "JijunHe@qq.com",
            "password": "sjycupiwuhoyecgc",
            "mailsubject": title,
            "mailtext": text,
            "mailencoding": "utf-8"
        }
        try:
            smtp = SMTP_SSL(mailInfo["hostname"])
            smtp.set_debuglevel(1)
            smtp.ehlo(mailInfo["hostname"])
            smtp.login(mailInfo["username"], mailInfo["password"])

            print 'OK5'
            msg = MIMEText(mailInfo["mailtext"], 'plain', mailInfo['mailencoding'])
            print 'OK4'
            msg["Subject"] = Header(mailInfo["mailsubject"], mailInfo["mailencoding"])
            print 'OK3'
            msg["from"] = mailInfo["from"]
            print 'OK2'
            msg["to"] = mailInfo["to"]
            print 'OK1'
            smtp.sendmail(mailInfo["from"], mailInfo["to"], msg.as_string())
            smtp.quit()
        except Exception, e:
            print str(e)
