from django.shortcuts import render, redirect

from . import util
from django.http import Http404
from django import forms

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

    # Check if the user wants to edit the entry
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content,
                "edit_form": form,
            })

    # Render the entry page with content
    else:
        form = UpdateForm(initial={"content": entry_content})
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entry_content,
            "edit_form": form,
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