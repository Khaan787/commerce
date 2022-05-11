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
            listing_owner = User.objects.get(pk=request.user.id),
            Auction_closed = False
            

        )

        listing.save()
        listing.watchlist.add(request.user)
        listing.save()


        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")

@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)
    owner = listing.listing_owner
    
    
    return render(request, "auctions/listing.html", {
        "that_listing": listing,
        "user": request.user,
        "owner": owner,
        
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
            listing = Listing.objects.get(pk=listing_id),
            bid_placed_by = request.user
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
    starting_Bid = listing.Starting_Bid  
    Bids = Bid.objects.all()
    Bids_on_listing = listing.bids.all()    
    Bids_amounts =listing.bids.values_list('Bid_amount', flat=True)
    Bids_Placers = listing.bids.values_list('bid_placed_by', flat=True)
    owner = listing.listing_owner     

    Highest_bid = None
    winner_object = None
    winner = None
    
    print("listing:", listing)
    print("Bids:", Bids)
    print("Bids_on_listing:", Bids_on_listing)
    print("Bids_amounts: ", Bids_amounts)
    print("Bids_Placers:", Bids_Placers)
    print("owner:", owner)
    
    if request.method == "POST":
        listing.Auction_closed = True
        listing.save()

        # Find which Bid_amount is == to the Starting_Bid i.e which Bid_amount is the Highest Bid placed 
        # Find the corresponding bid_placed_by of that Bid_amount
        for i in Bids_amounts:
            if i == starting_Bid:
                Highest_bid = i
                print("Highest_bid:", Highest_bid)

                winner_query = Bid.objects.filter(Bid_amount=Highest_bid)
                winner_object = Bid.objects.get(Bid_amount=Highest_bid)
                winner = winner_object.bid_placed_by

                listing.listing_winner = winner
                listing.save()


                print("winner_query:", winner_query)
                print("winner_object:", winner_object)
                print("winner:", winner)
                
      
        # The index page of the Highest bidder should get a message of "You won the Bid" on That Listing
        return render(request, "auctions/close.html",{
            "listing": listing,
            "user" : request.user,
            "owner": owner,          
            "winner": listing.listing_winner
        })





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
