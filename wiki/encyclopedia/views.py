from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from . import util
from markdown2 import markdown

import random
import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "pageTitle": "Encyclopedia",
        "message": "All Pages",
        "entries": util.list_entries()
    })


def title(request, title):
    content = util.get_entry(title)
    if content is not None:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "message": None,
            "content": markdown(content)
        })

    return render(request, "encyclopedia/title.html", {
        "title": title,
        "message": "The requested page is not available",
        "content": None
    })


def newPage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        forEdit = request.POST.get("forEdit")

        if forEdit or util.get_entry(title) is None:
            util.save_entry(title, content)
            return redirect("title", title=title)
        else:
            return render(request, "encyclopedia/newPage.html", {
                "message": "This title already exists. Please change it.",
                "title": title,
                "content": content,
            })

    return render(request, "encyclopedia/newPage.html")


def randomPage(request):
    entries = util.list_entries()

    if not entries:
        return redirect("index")

    num = random.randrange(0, len(entries))
    title = entries[num]

    return redirect("title", title=title)


def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    if query in entries:
        return redirect('title', title=query)
    else:
        matches = [entry for entry in entries if query.lower()
                   in entry.lower()]
        return render(request, "encyclopedia/index.html", {
            "pageTitle": "Search Results",
            "entries": matches,
            "message": "Search results for \'" + query + "\'",
        })


def delete(request, title):
    util.delete_entry(title)
    return redirect("index")


def editPage(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/newPage.html", {
        "title": title,
        "content": entry,
        "forEdit": True,
    })
