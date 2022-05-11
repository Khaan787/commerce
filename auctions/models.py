from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    Title = models.CharField(max_length=64)
    Description = models.TextField(max_length=500)
    Category = models.CharField(max_length=16)
    Starting_Bid = models.IntegerField()
    Image = models.ImageField()
    Auction_closed = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, blank= True, related_name="watcher")
    listing_owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner",null=True)
    listing_winner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="winner", null=True)

    #def bid(self):
        #return self.Starting_Bid


class Bid(models.Model):
    Bid_amount = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_placed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_placer", null=True)

