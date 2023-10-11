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

