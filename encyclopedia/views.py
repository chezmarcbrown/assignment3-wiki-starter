from django.shortcuts import render, redirect

from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.convert_to_html(title)
    print("In entry " + title)
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
    search = request.GET['q'].strip()
    title = f"Search Results: \"{search}\""
    
    entries = util.list_entries()
    search_results = []
    for entry in entries:
        if search.lower() in entry.lower():
            search_results.append(entry)

    # with a POST, you need to redirect to another page, not render a page. 
    # you'll see the misbehavior when you hit the browser refresh
    # after the search is performed. Alternatively, use a GET 
    # method on form in search.html (as I've done) and render the page
    return render(request, "encyclopedia/search.html", {
        "title": title,
        "entries": search_results
    })
    
def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })


def add(request):
    # better to test for POST, and then default to the GET action
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        contents = util.get_entry(title)

        if contents is not None:
            return render(request, "encyclopedia/add.html", {
                "error_message": f"Page \"{title}\" already exists."
            })
        else:
            util.save_entry(title, content)
            return redirect('entry', title=title)
    return render(request, "encyclopedia/add.html")
   
def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    print("In rand " + random_entry)
    return redirect(entry, random_entry)