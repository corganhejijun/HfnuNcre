# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render

from .models import Candidate, Apply


class ApplyForm(forms.Form):
    name = forms.CharField(
        label=u'姓名',
    )
    personId = forms.CharField(
        label=u'身份证号码'
    )

    def get(self, request):
        return render(request, 'ncrePay/apply.html')

    def post(self, request):
        name = request.POST['name']
        personId = request.POST['id']
        if not name or not personId:
            return render(request, 'ncrePay/apply.html', {'errorMsg': u'请输入姓名及身份证号码'})
        querySet = Candidate.objects.filter(candidateId=personId, name=name)
        if not querySet:
            return render(request, 'ncrePay/apply.html', {'errorMsg': u'未查到报名信息，今天报名的考生请耐心等待信息更新，明天再查询'})
        paidCnt = 0
        for item in querySet:
            if len(item.paidTime) > 0:
                paidCnt += 1
        length = len(querySet)
        if paidCnt != 0:
            if paidCnt != length:
                return render(request, 'ncrePay/apply.html', {'errorMsg': u'你的支付信息异常，请邮件联系管理员：hfnuncre@foxmail.com'})
            if paidCnt == length:
                return render(request, 'ncrePay/apply.html', {'successMsg': u'你已缴费成功, 请登录系统查看缴费状态'})
        appQuery = Apply.objects.filter(candidateNum=querySet[0].candidateNum)
        if 'payFee' in request.POST:
            if appQuery:
                app = appQuery[0]
                app.email = request.POST['email']
                if app.status == 'reject':
                    app.status = 'teacher'
                app.save()
                return render(request, 'ncrePay/apply.html', {'successMsg': u'你已提交过申请，如果邮件地址有误，请重新查询并修改，我们将重新受理你修改后的信息'})
            app = Apply()
            app.candidateNum = querySet[0].candidateNum
            app.email = request.POST['email']
            app.name = querySet[0].name
            app.save()
            return render(request, 'ncrePay/apply.html', {'successMsg': u'缴费申请已受理，我们将在三个工作日内处理'})
        msg = ""
        email = ""
        if appQuery:
            app = appQuery[0]
            if '@' not in app.email:
                msg += u"请填写正确的邮箱，否则无法接收我们的消息 "
            if app.status == 'reject':
                msg += u'你的上一次审核未通过，请根据系统邮件修改后再提交审核'
            email = app.email
        return render(request, 'ncrePay/apply.html', {
            'name': name, 'id': personId, 'list': querySet, 'len': length,
            'pay': 80 * length, 'errorMsg': msg, 'email': email
        })
