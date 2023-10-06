from django.shortcuts import render, redirect
from markdown2 import markdown
from .util import get_entry, save_entry
import random

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
    
def new_entry(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        if get_entry(title):
            context = {
                'error': 'An entry with this title already exists. Please choose a different title.',
                'title': title,
                'content': content
            }
            return render(request, 'encyclopedia/new_entry.html', context)

        save_entry(title, content)
        
        return redirect('entry', title=title)

    return render(request, 'encyclopedia/new_entry.html')

def random_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)

