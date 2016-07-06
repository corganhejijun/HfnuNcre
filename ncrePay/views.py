from .LoginForm import LoginForm
from .CandidateForm import CandidateForm


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
