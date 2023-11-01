from django.shortcuts import render, redirect
from django.contrib import messages
from . import util
import markdown2
import random
from .forms import newEntry, editEntry

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    entries = util.list_entries()
    isValid = False

    for e in entries:
        if entry_title.lower() == e.lower():
            entry_title = e
            isValid = True
    
    if isValid:
        entry_content = markdown2.markdown(util.get_entry(entry_title))
    else: entry_content = ""

    return render(request, "encyclopedia/entry.html", {
        "entries": entries,
        "entry_title": entry_title,
        "entry_content": entry_content
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", entry_title=random_entry)

def new_page(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = newEntry(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['title']
            entry_content = form.cleaned_data['content'].encode()

            name = entry_title.lower()
            for e in entries:
                if name == e.lower():
                    return render(request, "encyclopedia/new_page.html",{"form": form, "errormsg": "Name of new entry already taken. Choose another name"})
            
            util.save_entry(entry_title, entry_content)
            return redirect("index")
        else:
            return render(request, "encyclopedia/new_page.html",{"form": form})
    return render(request,"encyclopedia/new_page.html", {"form": newEntry()})

def edit_page(request, entry_title):
    old_content = util.get_entry(entry_title)

    if request.method == "POST":
        form = editEntry(request.POST, old_content=old_content)
        if form.is_valid():
            entry_content = form.cleaned_data['content'].encode()
            
            util.save_entry(entry_title, entry_content)
            return redirect("entry", entry_title=entry_title)
        else:
            return render(request, "encyclopedia/edit_page.html",{"form": form, "entry_title": entry_title})
    return render(request,"encyclopedia/edit_page.html", {
        "form": editEntry(old_content=old_content),
        "entry_title": entry_title
        })

def search(request):
    entries = util.list_entries()
    results = []

    if request.method == "GET":
        query = request.GET.get('q')
        for e in entries:
            if query.lower() == e.lower():
                return redirect('entry', entry_title=e)
            elif query.lower() in e.lower():
                results.append(e)

    return render(request, "encyclopedia/search.html", {
        "entries": entries,
        "results": results,
        "query": query
    })
