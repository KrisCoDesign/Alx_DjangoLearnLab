# from django.shortcuts import render
# from .models import CustomUser
# from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse


@permission_required('bookshelf.can_view', raise_exception=True)
def can_view(request):
    return HttpResponse("Book viewing")

@permission_required('bookshelf.can_create', raise_exception=True)
def can_create(request):
    return HttpResponse("Book Published")

@permission_required('bookshelf.can_edit', raise_exception=True)
def can_edit(request):
    return HttpResponse("Book edited")

@permission_required('bookshelf.can_delete', raise_exception=True)
def can_delete(request):
    return HttpResponse("Book deleted")

