from django.contrib import admin
from .models import Listing, Profile, Request

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "city", "phone")
    search_fields = ("user__username", "user__email", "city")

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "donor", "category", "city", "quantity", "status", "created_at")
    list_filter = ("category", "status", "city")
    search_fields = ("title", "description", "donor__username")

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("listing", "requester", "status", "created_at")
    list_filter = ("status",)
