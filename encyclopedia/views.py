from django.shortcuts import render, redirect
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown(content)
        return render(request, "encyclopedia/entry.html", {
            'title': title, 'content': html_content
        })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    if query in entries:
        return redirect('entry', title=query)
    else:
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, 'encyclopedia/search.html', {'results': results})