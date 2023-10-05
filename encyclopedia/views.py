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