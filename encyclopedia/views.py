from django.shortcuts import render

from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.convert_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "content": "Page does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    
def search(request):
    if request.method == 'POST':
        search = request.POST['q'].strip()
        title = f"Search Results: \"{search}\""
        
        entries = util.list_entries()
        search_results = []
        for entry in entries:
            if search.lower() in entry.lower():
                search_results.append(entry)
        content = search_results

        if search_results.count == 0:
            content = f"No results found for {search}"

        return render(request, "encyclopedia/search.html", {
            "title": title,
            "content": content
        })
    
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        
        content = util.convert_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/add.html")
    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        isExists = util.get_entry(title)

        if isExists is not None:
            return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "content": f"Page \"{title}\" already exists."
        })
        else:
            util.save_entry(title, content)
            content = util.convert_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
        
def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    content = util.convert_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
            "title": random_entry,
            "content": content
        })