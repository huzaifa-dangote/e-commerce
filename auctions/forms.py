from django import forms
from django.forms import ModelForm
from .models import User, Bid, Comment, Listing

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid",]
        
        widgets = {
            "bid": forms.NumberInput(attrs={"class": "w3-input w3-border"})    
        }
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment",]
        
        widgets = {
            "comment": forms.Textarea(attrs={"class": "w3-input w3-border", "placeholder": "Type a comment", "rows": "5"})    
        }
        
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "starting_bid", "description", "image_url", "category"]
        
        widgets = {
            "title": forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "starting_bid": forms.NumberInput(attrs={"class": "w3-input w3-border"}),
            "description": forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "image_url": forms.URLInput(attrs={"class": "w3-input w3-border"}),
            "category": forms.Select(attrs={"class": "w3-input w3-border"})
        }