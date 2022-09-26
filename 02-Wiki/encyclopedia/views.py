from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django import forms
import random
import markdown2
from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="", widget=forms.Textarea)


class EditPageForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)


def index(request):
    if request.GET != {}:
        return HttpResponseRedirect("/wiki/search/?q=" + request.GET['q'])
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def entry(request, title):

    if request.GET != {}:
        return HttpResponseRedirect("/wiki/search/?q=" + request.GET['q'])
    else:
        if title in util.list_entries():
            textHtml = markdown2.markdown(util.get_entry(title))

            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "text": textHtml
            })
        else:
            return HttpResponseNotFound('<h1 style=\'text-align: center;font-size: 5rem;\' >Page not found</h1>')


def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid() and (request.POST["title"] not in util.list_entries()):
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect("/wiki/" + title)
        elif request.POST["title"] in util.list_entries():
            return HttpResponseNotFound(
                "<h1 style=\'text-align: center;font-size: 5rem;\'>The encyclopedia entry already exists</h1>")
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })

    elif request.GET != {}:
        return HttpResponseRedirect("/wiki/search/?q=" + request.GET['q'])

    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewPageForm().as_p()
        })


def editpage(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect("/wiki/" + title)

    elif request.GET != {}:
        return HttpResponseRedirect("/wiki/search/?q=" + request.GET['q'])

    else:
        text = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "text": text,
            "form": EditPageForm({"content": text}).as_p()
        })


def randompage(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect("/wiki/" + title)


def search(request):
    if request.GET != {}:

        posibbleResults = []

        for entry in util.list_entries():
            if request.GET['q'] == entry:
                return HttpResponseRedirect("/wiki/" + request.GET['q'])
            elif request.GET['q'] in entry:
                posibbleResults.append(entry)

        return render(request, "encyclopedia/search.html", {
            'query': request.GET['q'],
            "entries": posibbleResults
        })

    else:
        return render(request, "encyclopedia/search.html", {})


