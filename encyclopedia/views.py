from django.shortcuts import render, redirect
from django import forms
from random import randint
from . import util
import markdown2


# Form for creating/editing
class CreateForm(forms.Form):
    title = forms.CharField(
        label="Entry Title",
        widget=forms.TextInput(
            attrs={"style": "width: 300px;", "class": "form-control"}
        ),
    )
    content = forms.CharField(
        label="Contents",
        widget=forms.Textarea(
            attrs={"style": "width: 600px;", "class": "form-control"}
        ),
    )


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def create(request):
    if request.method == "POST":
        new_entry = CreateForm(request.POST)
        title = request.POST["title"]
        content = request.POST["content"]
        # Search for duplicate
        if find_entry(title) is None:
            util.save_entry(title, content)
            return redirect("entry", title=title)
        else:
            return render(
                request,
                "encyclopedia/create.html",
                {
                    "errormessage": "An existing entry already exists.",
                    "form": CreateForm(),
                },
            )
    else:
        return render(
            request,
            "encyclopedia/create.html",
            {"errormessage": False, "form": CreateForm()},
        )


def edit(request, title):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        f = CreateForm({"title": title, "content": util.get_entry(title)})
        return render(
            request,
            "encyclopedia/edit.html",
            {"title": title, "form": f},
        )


def random_page(request):
    entries = util.list_entries()
    rand = randint(0, len(entries) - 1)
    random_entry = entries[rand]
    return render(
        request,
        "encyclopedia/entry.html",
        {
            "entry_title": random_entry,
            "content": markdown2.markdown(util.get_entry(random_entry)),
        },
    )


def entry(request, title):
    entry = find_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html")
    else:
        content = markdown2.markdown(util.get_entry(entry))

        return render(
            request,
            "encyclopedia/entry.html",
            {"entry_title": entry, "content": content},
        )


def search(request):
    title = request.GET.get("q")
    entry = find_entry(title)
    if entry is None:
        poss_result = [i for i in util.list_entries() if title.lower() in i.lower()]
        if poss_result:
            return render(request, "encyclopedia/search.html", {"result": poss_result})
        else:
            return render(request, "encyclopedia/error.html")
    else:
        return redirect("entry", title=title)


def find_entry(title):
    entries = util.list_entries()
    for entry in entries:
        if entry.casefold() == title.casefold():
            return entry
    return None
