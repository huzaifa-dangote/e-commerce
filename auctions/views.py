from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from datetime import datetime, timedelta
from django.db.models import Max
import pytz

from .models import User, Bid, Comment, Listing
from .forms import BidForm, ListingForm, CommentForm

class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class ListingDetailView(LoginRequiredMixin, DetailView):
    model = Listing

def index(request):
    listings = Listing.objects.exclude(is_inactive=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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
            messages.error(request, "Invalid username and/or password")
            return HttpResponseRedirect(reverse("login"))
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
            messages.error(request, "Passwords must match")
            return HttpResponseRedirect(reverse("register"))

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken")
            return HttpResponseRedirect(reverse("register"))
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_page(request, listing_id):
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing = Listing.objects.get(id=listing_id)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            listing.comment.add(comment)
            messages.success(request, "Comment added successfully")
            return HttpResponseRedirect(reverse("listing-page", args=(listing.id,)))
        
        else:
            messages.success(request, "Invalid entry")
            return HttpResponseRedirect(reverse("listing-page", args=(listing.id,)))

    listing = Listing.objects.get(id=listing_id)
    user = request.user
    highest_bid = listing.bid.all().aggregate(Max("bid")).get("bid__max")
    comments = listing.comment.all()
    
    if user.is_authenticated:
        watchlist = user.watchlist_listings.all()
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "watchlist": watchlist,
            "highest_bid": highest_bid,
            "comments": comments,
            "form": CommentForm 
        })
    
    else:
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "highest_bid": highest_bid,
            "comments": comments,
            "form": CommentForm
        })

@login_required
def watchlist(request, user_id):
    user = User.objects.get(id=user_id)
    watchlist = user.watchlist_listings.all()
    return render(request, "auctions/watchlist_page.html", {
        "watchlist": watchlist    
    })

@login_required
def add_to_watchlist(request, listing_id):
    
    if request.method == 'POST':
        
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        listing.watchlist.add(user)
        messages.success(request, "Item added to your watchlist")
        return HttpResponseRedirect(reverse("listing-page", args=(listing.id,)))
    
@login_required
def remove_from_watchlist(request, listing_id):
    
    if request.method == "POST":
        
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        listing.watchlist.remove(user)
        messages.success(request, "Item removed from your watchlist")
        return HttpResponseRedirect(reverse("listing-page", args=(listing.id,)))
   
@login_required
def bidding(request, listing_id):
    
    if request.method == "POST":
        form = BidForm(request.POST)
        listing = Listing.objects.get(id=listing_id)
        max_bid = listing.bid.all().aggregate(Max("bid")).get("bid__max")
        
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            
            if listing.bid.exists():
                if bid.bid > max_bid:
                    bid.save()
                    listing.bid.add(bid)
                    messages.success(request, "Your bid was successful")
                    return HttpResponseRedirect(reverse("index"))
                else:
                    messages.error(request, "Your bid must be greater than the latest bid")
                    return HttpResponseRedirect(reverse("bidding", args=(listing.id,)))
                
            else:
                if bid.bid >= listing.starting_bid:
                    bid.save()
                    listing.bid.add(bid)
                    messages.success(request, "Your bid was successful")
                    return HttpResponseRedirect(reverse("index"))
                else:
                    messages.error(request, "Your bid must be at least as large as the starting bid")
                    return HttpResponseRedirect(reverse("bidding", args=(listing.id,)))
            
        else:
            return render(request, "auctions/bidding_page.html", {
                "form": form    
            })
        
    return render(request, "auctions/bidding_page.html", {
        "form": BidForm()
    })

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bid_value = listing.bid.all().aggregate(Max("bid")).get("bid__max")
    user = listing.bid.get(bid=bid_value).user
    user.listings_won.add(listing)
    listing.is_inactive = True
    listing.save()
    messages.success(request, f"{listing.title} listing is closed and {user} is the winner")
    return HttpResponseRedirect(reverse("index"))

def categories(request):
    return render(request, "auctions/categories.html", {
        "listingform": ListingForm()
    })

def category(request, category_name):
    from .models import LISTING_CATEGORIES
    category = Listing.objects.filter(category=category_name).exclude(is_inactive=True)
    category_name = LISTING_CATEGORIES[category_name]
    return render(request, "auctions/category_page.html", {
        "category": category,
        "category_name": category_name
    })