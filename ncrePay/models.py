from __future__ import unicode_literals

from django.db import models


class Teacher(models.Model):
    username = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    alipayQr = models.CharField(max_length=64)


class Candidate(models.Model):
    candidateNum = models.CharField(max_length=14)
    testNum = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    candidateId = models.CharField(max_length=18)
    paidTime = models.CharField(max_length=20)
    testCode = models.CharField(max_length=2)
    testName = models.CharField(max_length=64)
    photoName = models.CharField(max_length=20)
    mail = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    testRoom = models.CharField(max_length=4)
    testAddr = models.CharField(max_length=64)
    testNum = models.CharField(max_length=4)
    testBeginTime = models.CharField(max_length=20)
    testEndTime = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
