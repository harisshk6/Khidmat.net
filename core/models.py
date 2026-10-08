from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    ROLE_CHOICES = [
        ("donor", "Donor"),
        ("requester", "Requester"),
        ("both", "Both"),
        ("volunteer", "Volunteer"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="both")
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("clothing", "Clothing"),
        ("medicine", "Medicine"),
        ("school", "School Supplies"),
        ("hygiene", "Hygiene"),
        ("household", "Household"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("completed", "Completed"),
    ]
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    city = models.CharField(max_length=100)
    pickup_details = models.CharField(max_length=255, blank=True)

    image = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    pickup_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    pickup_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Request(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    ]
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="requests")
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["listing", "requester"], name="one_request_per_user_listing")
        ]

    def __str__(self):
        return f"{self.requester.username} -> {self.listing.title}"
