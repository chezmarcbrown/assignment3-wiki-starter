from django.shortcuts import render, redirect
from django import forms
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

        util.save_entry(title, content)
        
        return redirect('entry', title=title)

    return render(request, 'encyclopedia/new_entry.html')

def edit_entry(request, title):
    if request.method == 'POST':
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry', title=title)
    else:
        content = util.get_entry(title)
        context = {
            'title': title,
            'content': content
        }
        return render(request, 'encyclopedia/edit_entry.html', context)
    
class CreateForm(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={"style": "width: 300px;", "class": "form-control"}
        ),
    )
    content = forms.CharField(
        label="Content (Markdown)",
        widget=forms.Textarea(
            attrs={"style": "width: 600px;", "class": "form-control"}
        ),
    )

def new_entry_form(request):
    if request.method == "POST":
        new_entry = CreateForm(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data['title']
            content = new_entry.cleaned_data['content']
            # Search for duplicate
            if get_entry(title) is None:
                util.save_entry(title, content)
                return redirect("entry", title=title)
            else:
                return render(request, "encyclopedia/new_entry_form.html",
                    { "error": "An entry with this title already exists. Please choose a different title.",
                        "form": new_entry},
                )
    else:
        new_entry = CreateForm()
    return render(request, "encyclopedia/new_entry_form.html", {"form": new_entry})

def random_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)

