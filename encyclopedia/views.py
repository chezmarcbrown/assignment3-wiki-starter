from django.shortcuts import render
import markdown
import random

# Small change

from . import util

def convert_to_html(page_title):
    page = util.get_entry(page_title)
    markdowner = markdown.Markdown()
    if page == None:
        return None
    else:
        return markdowner.convert(page)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else :
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })    

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_new.html")
    
    if request.method == "POST":
        page = request.POST.get('page')
        info = request.POST.get('info')
        
        if util.get_entry(page):
            return render(request, "encyclopedia/error.html", 
                          {"message": "This entry already exists"})

        util.save_entry(page, info)
        converted_info = convert_to_html(page)
        return render(request, "encyclopedia/entry.html", 
                      {"page": page, "info": converted_info})

            
def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })