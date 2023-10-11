from django.shortcuts import render, redirect
from markdown2 import markdown

from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title.strip())

    if not content:
        content = "## Error 404 : Page not Found."

    content = markdown(content)

    return render(
        request, "encyclopedia/entry.html", {
            "title" : title,
            "content" : content
        }
     )

def search(request):
    if request.method == "POST":
        item = request.POST['q'].strip()

        pages = util.list_entries()
        if item in pages:
            return redirect("entry", title=item)
        
        return render(
            request, "encyclopedia/search.html", {
                "title": item,
                # Thanks to GeeksForGeeks for this one liner substring list search
                # https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/
                "content" : [i for i in pages if item.lower() in i.lower()]
            }
        )

def random(request):
    return redirect("entry", choice(util.list_entries()))

def edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': util.get_entry(title)
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        util.save_entry(title, content)

        content = markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "message": f"Could not create the page \"{title}\" as it already exists."
            })
        else:
            util.save_entry(title, content)
            return redirect("entry", title=title)
    
