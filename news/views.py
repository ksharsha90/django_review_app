from django.shortcuts import render
from django.http import HttpResponse
from .models import News


def news(request):
    newss = News.objects.all().order_by("-date")
    context = {
        "newss": newss
    }
    return render(request, "news.html", context=context)
