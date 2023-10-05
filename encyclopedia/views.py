from django.shortcuts import render

from . import util

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
            "content": content
        })
    
def search(request):
    if request.method == 'POST':
        search = request.POST['q'].strip()
        content = util.convert_to_html(search)
        title = f"Search Results: \"{search}\""

        if content == None:
            content = f"No results found for {search}."
        else:
            entries = util.list_entries()
            search_results = []
            for entry in entries:
                if search.lower() in entry.lower():
                    search_results.append(entry)
            content = search_results

        return render(request, "encyclopedia/search.html", {
            "title": title,
            "content": content
        })