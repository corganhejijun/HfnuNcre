from .LoginForm import LoginForm
from .CandidateForm import CandidateForm
from .ApplyForm import ApplyForm
from .MyListForm import MyListForm


def login(request):
    if request.method == 'GET':
        form = LoginForm(request.GET)
        return form.get(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        return form.post(request)


def index(request):
    if request.method == 'GET':
        form = CandidateForm(request.GET)
        return form.get(request)
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        return form.post(request)


def apply(request):
    if request.method == 'GET':
        form = ApplyForm(request.GET)
        return form.get(request)
    if request.method == 'POST':
        form = ApplyForm(request.POST)
        return form.post(request)


def myList(request):
    if request.method == 'GET':
        form = MyListForm(request.GET)
        return form.get(request)
    if request.method == 'POST':
        form = MyListForm(request.POST)
        return form.post(request)
