from django.shortcuts import render, redirect
import markdown2
from . import util
from django.http import Http404
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class UpdateForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 80}))

def entry(request, title):
    
    entry_content = util.get_entry(title)
    
    if entry_content is None:
        raise Http404("Entry not found")

    return render(request, 'encyclopedia/entry.html', {
        "title": title,
        "content": markdown2.markdown(entry_content)
    })
    
def search(request):
    query = request.GET.get("q")
    
    if query:
        # Check if the query matches the name of an encyclopedia entry
        entry_content = util.get_entry(query)
        if entry_content is not None:
            return redirect('entry', title=query)
        
        # If the query does not match an entry, find entries with the query as a substring
        results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results,
        })
    else:
        return redirect('index')

def edit(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(f"wiki/{ title }")
    else:
        title = request.GET.get('title')
        content = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'content': content
        })

def create(request):
    pass

def random(request):
    pass

