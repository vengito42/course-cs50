from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required

from .models import *


class NewProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class WatchlistForm(forms.Form):
    id_product = forms.IntegerField(label="", widget=forms.HiddenInput())


#       --------------------------
#         Pagina de INICIO
#       -------------------------


def index(request):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []

    query = request.GET.get('q') if request.GET.get('q') else ''

    context = {'products': Product.objects.filter(category__name__icontains=query, active=True),
               'num_watchlist': len(request.session["watchlist"]),
               'categories': Category.objects.all()}
    return render(request, "auctions/index.html", context)


#       --------------------------
#         Logica de USUARIOS
#       -------------------------


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {"message": "Invalid username and/or password.",
                       'num_watchlist': len(request.session["watchlist"])}
            return render(request, "auctions/login.html", context)
    else:
        context = {'num_watchlist': len(request.session["watchlist"])}
        return render(request, "auctions/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            context = {"message": "Passwords must match.",
                       'num_watchlist': len(request.session["watchlist"])}
            return render(request, "auctions/register.html", context)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            context = {"message": "Username already taken."}
            return render(request, "auctions/register.html", context)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {'num_watchlist': len(request.session["watchlist"])}
        return render(request, "auctions/register.html", context)


#       --------------------------
#         Logica de PRODUCTOS
#       -------------------------


def product_view(request, product_id):

    product = Product.objects.get(pk=product_id)
    comments = Comment.objects.filter(product=product_id)
    form = WatchlistForm({"id_product": product.pk})

    last_bid = Bid.objects.filter(product=product_id).first()
    if last_bid is None:
        last_bid = product.price
    else:
        last_bid = last_bid.price

    context = {
        'product': product,
        'comments': comments,
        'formWatchlist': form,
        'num_watchlist': len(request.session["watchlist"]),
        'message': None,
        'last_bid': last_bid}

    if product.active:

        if request.method == 'POST':
            #       -----------
            #       NEW COMMENT
            if 'comment' in request.POST:
                comment = Comment(product=product,
                                  user=request.user,
                                  content=request.POST.get('comment'))
                comment.save()

                context['message'] = 'Comment Successfull'

            elif 'active' in request.POST:
                product.winner_id = Bid.objects.filter(product=product_id).first().user.pk
                product.active = request.POST.get('active')
                product.save()
                return HttpResponseRedirect(reverse("index"))

            #       ----------------
            #       ADD TO WATCHLIST
            else:
                form = WatchlistForm(request.POST)
                if form.is_valid():
                    id = form.cleaned_data["id_product"]
                    if id not in request.session["watchlist"]:
                        request.session["watchlist"] += [id]
                        context['num_watchlist'] = len(request.session["watchlist"])
        return render(request, "auctions/product.html", context)

    else:
        return render(request, "auctions/product-finish.html", context)


def new_bid(request,product_id):
    product = Product.objects.get(id=product_id)
    last_bid = Bid.objects.filter(product=product_id).first()
    if not last_bid:
        last_bid = product.price
    else:
        last_bid = last_bid.price

    context = {'obj': product,
               'num_watchlist': len(request.session["watchlist"]),
               'last_bid': last_bid,
               'message': None}

    if request.method == 'POST':
        final_bid = Bid(price=request.session['new_bid'],
                        user=request.user,
                        product=product)
        final_bid.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        new_bid = float(request.GET.get('new_bid'))
        context['new_bid'] = new_bid

        if new_bid > product.price and new_bid > last_bid:
            request.session['new_bid'] = new_bid

        else:
            context['message'] = 'Your bid not is valid. Must be greater than price or than last bid.'
        return render(request, "auctions/new-bid.html", context)


@login_required(login_url='/login')
def new_product(request):

    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {"form": form}
            return render(request, "auctions/newproduct.html", context)

    context = {'form': NewProductForm().as_p(),
               'num_watchlist': len(request.session["watchlist"])}
    return render(request, "auctions/newproduct.html", context)


#       --------------------------
#         Logica de la WATCHLIST
#       --------------------------


@login_required(login_url='/login')
def watchlist(request):
    products = []
    for id_product in request.session["watchlist"]:
        products.append(Product.objects.get(pk=id_product))

    context = {'products': products,
               'form': WatchlistForm(),
               'num_watchlist': len(request.session["watchlist"])}
    return render(request, "auctions/watchlist.html", context)


@login_required()
def delete(request, product_id):
    if request.method == 'POST':
        for id in request.session["watchlist"]:
            if id == product_id:
                request.session.modified = True
                request.session["watchlist"].remove(id)
        return HttpResponseRedirect('watchlist')
    else:
        product = Product.objects.get(id=product_id)
        context = {'obj': product,
                   'num_watchlist': len(request.session["watchlist"])}
        return render(request, "auctions/delete.html", context)
