from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.uername.lowercase()}"


class Listing(models.Model):
    # Use models.CASCADE (no quotes)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return f"\"{self.owner}\" listed {self.name.Capitalize()}. Description: {self.description}"


class Bid(models.Model):  # Renamed to singular
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    # Added max_digits (e.g., 10 digits total, 2 decimal places allows up to 99,999,999.99)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):  # Renamed to singular
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")  # Fixed related_name
    content = models.TextField()
