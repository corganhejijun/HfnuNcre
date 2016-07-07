from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # only if you need to support Python 2
class Teacher(models.Model):
    username = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    alipayQr = models.CharField(max_length=64)

    def __str__(self):
        return self.name


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


class Apply(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    # apply teacher reject success
    status = models.CharField(max_length=24, default="apply")
    email = models.CharField(max_length=128)
