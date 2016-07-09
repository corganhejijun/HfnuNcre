# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from .models import Teacher, Apply


class LaomoForm(forms.Form):
    def rendrePage(self, request):
        teacherSet = []
        applySet = []
        for item in Teacher.objects.filter():
            teacherSet.append(item.name)
            applySet.append(len(Apply.objects.filter(teacher__id=item.id)))
        return render(request, 'ncrePay/laomo.html', {'teaList': teacherSet, 'appList': applySet})

    def get(self, request):
        return self.rendrePage(request)

    def post(self, request):
        return self.rendrePage(request)
