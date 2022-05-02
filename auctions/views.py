from ast import And
import this
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Listing,User,Bid


def index(request):    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
    })
    
@login_required
def create(request):
    if request.method == "POST":
        listing = Listing(
            Title = request.POST["title"],
            Description = request.POST["description"],
            Category = request.POST["category"],
            Starting_Bid = request.POST["starting_bid"],
            Image = request.POST["image"],
            watchlist = User.objects.get(pk=request.user.id),
            listing_owner = User.objects.get(pk=request.user.id)
            

        )

        listing.save()
        listing.watchlist.add(request.user)


        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")

@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id),
    owner = listing.listing_owner

    print(listing)
    print(user)
    print(owner)

    return render(request, "auctions/listing.html", {
        "that_listing": listing,
        "user": user,
        "owner": owner
    })


@login_required
def my_watchlist(request):
    user = User.objects.get(pk=request.user.id)

    return render(request, "auctions/my_watchlist.html",{
        "watchlist": user.watcher.all()
    })

@login_required
def add_listing(request, that_listing):
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=that_listing)

    listing.watchlist.add(user)

    return HttpResponseRedirect(reverse("my_watchlist"))


@login_required
def remove_listing(request,listing_id):
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=listing_id)

    listing.watchlist.remove(user)

    return HttpResponseRedirect(reverse("my_watchlist"))


@login_required
def bid_placed(request,listing_id):
    if request.method == "POST":
        
        recent_bid = Bid(
            Bid_amount = request.POST["bid_amount"],
            listing = Listing.objects.get(pk=listing_id)
        )

        listing = Listing.objects.get(pk=listing_id)
        starting_Bid = listing.Starting_Bid        
        recent_bid_int = int(recent_bid.Bid_amount)
   

        if recent_bid_int > starting_Bid:

            listing.Starting_Bid =  recent_bid_int

            listing.save()
            recent_bid.save()
            
            return HttpResponse("Bid SUCCESSFULLY Placed")

        else:
            return HttpResponse("Bid CANNOT be placed")        
   

        #last_highest_bid = Bids.objects.get(pk=Listing)
        #all_bids_placed = Bids.objects.values_list('Placed_Bids', flat=True)


#close_auction view:
# When the user clicks the button i.e. closes the listing, changing the value of Auction_close from False to True
# if the auction is not closed already
# it should remove the listing from the site
# and the user who made the last highest bid will be the winner

@login_required
def close_auction(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        listing.Auction_closed = True
        # Disable the Bids on the Listing And display an Error message such as "The auction is Closed"








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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
