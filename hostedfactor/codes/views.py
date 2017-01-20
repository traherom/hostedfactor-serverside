from django.shortcuts import render
from django import urls
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models

class CodeList(LoginRequiredMixin, generic.ListView):
    """
    Show all codes for current client
    """
    model = models.Code
    ordering = 'name'


class CodeCreate(LoginRequiredMixin, generic.CreateView):
    """
    Create a new code in the DB
    """
    model = models.Code
    fields = [
        'name',
        'secret',
    ]
    success_url = urls.reverse_lazy('code-list')

    def form_valid(self, form):
        """
        The newly created code should be put in the current client
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class CodeEdit(LoginRequiredMixin, generic.UpdateView):
    """
    Edit name of code
    """
    model = models.Code
    pk_url_kwarg = 'code_pk'
    fields = [
        'name',
    ]
    success_url = urls.reverse_lazy('code-list')


class CodeDelete(LoginRequiredMixin, generic.DeleteView):
    """
    Remove code entirely from database
    """
    model = models.Code
    pk_url_kwarg = 'code_pk'
    success_url = urls.reverse_lazy('code-list')
