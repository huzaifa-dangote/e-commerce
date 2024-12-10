from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.db.models import Max

LISTING_CATEGORIES = {
    "FASHION": "Fashion",
    "ELECTRONICS": "Electronics",
    "TOYS": "Toys",
    "HOME": "Home",
    "FOOD": "Food",
    "BEVERAGES": "Beverages",
    "BEAUTY": "Beauty and Personal Products",
}

class User(AbstractUser):
    def __str__(self):
        return f"{self.username} ({self.email})"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"${self.bid} bid, made by {self.user}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    
    def __str__(self):
        return f"Comment by {self.user}"

class Listing(models.Model):
    title = models.CharField(max_length=20)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=200, null=True, default=None, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_listings")
    bid = models.ManyToManyField(Bid, blank=True, related_name="bid_listing", null=True, default=None)
    comment = models.ManyToManyField(Comment, related_name="comment_listing", blank=True, null=True, default=None)
    category = models.CharField(max_length=11, choices=LISTING_CATEGORIES, null=True, default=None)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_won", blank=True, null=True, default=None)
    is_inactive = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Title: {self.title}; Starting bid: ${self.starting_bid}; Category:{self.category}"
    
    def get_absolute_url(self):
        return reverse("listing-detail", kwargs={"pk": self.pk})
    
    def highest_bid(self):
        return self.bid.all().aggregate(Max("bid")).get("bid__max")