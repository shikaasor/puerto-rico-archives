from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import file
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


def home(request):
    context = {
        'files': file.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=file.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'files':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


class fileListView(ListView):
    model = file
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'files'
    ordering = ['-dateuploaded']
    paginate_by = 2


class UserfileListView(ListView):
    model = file
    template_name = 'blog/file_repo.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'files'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return file.objects.filter(author=user).order_by('-dateuploaded')


class fileDetailView(DetailView):
    model = file
    template_name = 'blog/file_detail.html'


class fileCreateView(LoginRequiredMixin, CreateView):
    model = file
    template_name = 'blog/file_form.html'
    fields = ['title', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class fileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = file
    template_name = 'blog/file_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.author:
            return True
        return False


class fileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = file
    success_url = '/'
    template_name = 'blog/file_confirm_delete.html'

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
