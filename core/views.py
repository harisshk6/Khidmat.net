from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ListingForm, ProfileForm, RegisterForm, RequestForm
from .models import Listing, Profile, Request

def home(request):
    listings = Listing.objects.filter(status="available")[:6]
    return render(request, "home.html", {"listings": listings})

def listings(request):
    qs = Listing.objects.filter(status="available")
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    city = request.GET.get("city", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if city:
        qs = qs.filter(city__icontains=city)
    return render(request, "listings.html", {"listings": qs, "q": q, "category": category, "city": city})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "listing_detail.html", {"listing": listing})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Welcome to Khidmat.net!")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

@login_required
def dashboard(request):
    my_listings = request.user.listings.all()
    incoming = Request.objects.filter(listing__donor=request.user).select_related("listing", "requester")
    outgoing = request.user.requests.select_related("listing")
    return render(request, "dashboard.html", {
        "my_listings": my_listings,
        "incoming": incoming,
        "outgoing": outgoing,
    })

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profile.html", {"form": form})

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.save()
            messages.success(request, "Your donation has been posted.")
            return redirect("listing_detail", pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, "listing_form.html", {"form": form})

@login_required
def request_item(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.donor == request.user:
        messages.error(request, "You cannot request your own donation.")
        return redirect("listing_detail", pk=pk)
    if listing.status != "available":
        messages.error(request, "This donation is no longer available.")
        return redirect("listing_detail", pk=pk)

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.listing = listing
            obj.requester = request.user
            try:
                obj.save()
                messages.success(request, "Request sent to the donor.")
            except Exception:
                messages.error(request, "You have already requested this donation.")
            return redirect("listing_detail", pk=pk)
    else:
        form = RequestForm()
    return render(request, "request_form.html", {"form": form, "listing": listing})

@login_required
def update_request(request, pk, action):
    req = get_object_or_404(Request, pk=pk)
    if req.listing.donor != request.user:
        messages.error(request, "You are not allowed to change this request.")
        return redirect("dashboard")

    if action == "accept" and req.status == "pending":
        req.status = "accepted"
        req.listing.status = "reserved"
        req.listing.save(update_fields=["status"])
        req.save(update_fields=["status"])
        messages.success(request, "Request accepted. The donation is now reserved.")
    elif action == "reject" and req.status == "pending":
        req.status = "rejected"
        req.save(update_fields=["status"])
        messages.info(request, "Request rejected.")
    elif action == "complete" and req.status == "accepted":
        req.status = "completed"
        req.listing.status = "completed"
        req.save(update_fields=["status"])
        req.listing.save(update_fields=["status"])
        messages.success(request, "Donation marked as completed.")
    return redirect("dashboard")
