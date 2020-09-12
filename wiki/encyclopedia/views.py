from django.shortcuts import render

from markdown2 import markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
        "message": "\"" + title + "\" does not currently have an entry in the encyclopedia."
        })
    return render(request, "encyclopedia/entry.html", {
    "title": title,
    "content": markdown(content)
    })

def search(request):
    search_request = request.GET.get("q")
    content = util.get_entry(search_request)
    if not content:
        result = []
        for title in util.list_entries():
            if search_request.casefold() in title.casefold():
                result.append(title)
        return render(request, "encyclopedia/search.html", {
            "result": result
        })
    return render(request, "encyclopedia/entry.html", {
    "title": search_request,
    "content": markdown(content)
    })

def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        for entry in util.list_entries():
            if title.casefold() == entry.casefold():
                return render(request, "encyclopedia/new_entry.html", {
                "message": "Page with the same title already exists!",
                "title": title,
                "content": content
                })
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "message": "New encyclopedia page added successfully!"
        })
    return render(request, "encyclopedia/new_entry.html")

def edit_entry(request, title):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content),
        "message": "\"" + title + "\" has been updated successfully!"
        })
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_entry.html", {
    "title": title,
    "content": content
    })

def random_entry(request):
    title = choice(util.list_entries())
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
    "title": title,
    "content": markdown(content)
    })
