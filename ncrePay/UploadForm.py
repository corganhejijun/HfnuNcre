# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth

from os import path, remove
import csv

from .models import Apply, Candidate


class UploadForm(forms.Form):
    uploadFile = forms.FileField()

    def refreshData(self, requestFile):
        if path.exists('D:/git/HfnuNcre/candidate.csv'):
            remove('D:/git/HfnuNcre/candidate.csv')
        with open('D:/git/HfnuNcre/candidate.csv', 'wb+') as destination:
            for chunk in requestFile.chunks():
                destination.write(chunk)
        Candidate.objects.filter().delete()
        csvFile = file('D:/git/HfnuNcre/candidate.csv', 'rb')
        csvReader = csv.reader(csvFile)
        for line in csvReader:
            if csvReader.line_num == 1:
                continue
            lst = Candidate.objects.filter(candidateNum=line[2], testCode=line[16])
            if lst:
                continue
            can = Candidate()
            can.candidateNum = line[2]
            can.testNum = line[3]
            can.name = line[4]
            can.candidateId = line[8]
            can.paidTime = line[15]
            can.testCode = line[16]
            can.testName = line[17]
            can.photoName = line[18]
            can.mail = line[21]
            can.phone = line[22]
            can.testRoom = line[25]
            can.testAddr = line[26]
            can.testNum = line[28]
            can.testBeginTime = line[32]
            can.testEndTime = line[33]
            if len(can.paidTime) == 0:
                querySet = Apply.objects.filter(candidateNum=can.candidateNum)
                if len(querySet) == 1:
                    app = querySet[0]
                    if len(can.mail) > 0 and len(app.email) == 0:
                        app.email = can.mail
                    app.name = can.name
                    app.save()
                elif len(querySet) > 1:
                    for i in range(len(querySet)):
                        if i == 0:
                            continue
                        querySet[i].delete()
                else:
                    # len == 0
                    app = Apply()
                    app.candidateNum = can.candidateNum
                    app.status = 'apply'
                    app.email = can.mail
                    app.save()
            can.save()
        csvFile.close()

    def logout(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))

    def get(self, request):
        if not request.user.is_authenticated():
            return self.logout(request)
        return render(request, 'ncrePay/upload.html', {'form': self})

    def post(self, request):
        if not request.user.is_authenticated():
            return self.logout(request)
        if self.is_valid():
            self.refreshData(request.FILES['uploadFile'])
            return HttpResponseRedirect(reverse('index'))
        else:
            print self.errors
            return render(request, 'ncrePay/upload.html', {'form': self})
