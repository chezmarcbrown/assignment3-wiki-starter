from django.shortcuts import render
import markdown

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
    
def newpage(request):
    response = {
    "GET": render(request, "encyclopedia/create_new.html"),
    }.get(request.method)
    return response

def random(request):
    response = {
    "GET": render(request, "encyclopedia/random_page.html"),
    }.get(request.method)
    return response

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })

def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_new.html")
    else:
        page = request.POST['page']
        info = request.POST['info']
        existingPage = util.get_entry(page)
        if existingPage != None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists"
            })
        else:
            util.save_entry(page, info)
            converted_info = convert_to_html(page)
            return render(request, "encyclopedia/entry.html", {
                "page": page,
                "info": converted_info
            })
