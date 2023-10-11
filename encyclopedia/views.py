from django.shortcuts import render
import markdown

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
    
def newpage(request):
    response = {
    "GET": render(request, "encyclopedia/create_new.html"),
    }.get(request.method)
    return response