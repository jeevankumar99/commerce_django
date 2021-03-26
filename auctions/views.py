from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
from .models import *
from django.contrib.auth.decorators import login_required


# ModelForms

class createForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'eg: Microsoft Xbox One X 1TB (2019)'}),
            'description': forms.Textarea(attrs={'placeholder': 'eg: 6 months old, with controller'}),
            'image_url': forms.TextInput(attrs={'placeholder': 'eg: https://www.xbox.com/en=IN/consoles/xbox-one.png'}),
            'opening_bid': forms.NumberInput(attrs={'placeholder': 'eg: $200'}),
        }
        exclude = 'user', 'current_bid', 'closed',

class bidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = 'user', 'product',

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = 'user', 'product',


# Views

@login_required(login_url="/login")
def bid(request):
    bid_form = bidForm(request.POST)
    temp_product = Product.objects.get(id=request.session['product_id'])
    temp_bid = bid_form.save(commit=False)

    # to keep bids above current and opening bid
    if temp_bid.bid < temp_product.opening_bid or temp_bid.bid < temp_product.current_bid:
        request.session['invalid_bid'] = True
        return HttpResponseRedirect(f"listings/{request.session['product_id']}")

    # saving the new bid and updating the Product model
    temp_bid.user = User.objects.get(username=request.user)
    temp_product.current_bid = temp_bid.bid
    temp_product.save()
    temp_bid.product = temp_product
    temp_bid.save()
    return HttpResponseRedirect(f"listings/{request.session['product_id']}")


def categories(request):
    available_categories = Product.objects.values_list('category')

    # converts all available categories to a list, ignores duplicates
    available_categories = [i[0] for i in available_categories]
    return render(request, "auctions/categories.html", {
        'categories': set(available_categories),
        'title': "Categories",
    })


@login_required(login_url="/login")
def close_listing(request):
    if request.method == 'GET':
        product = Product.objects.get(id=request.session['product_id'])
        
        # if listing is closed without bid made
        bid_list = Bid.objects.filter(product=product).order_by('-bid')
        if len(bid_list) > 0:
            bid_user = bid_list[0].user
        else:
            bid_user = False
        return render(request, "auctions/close_listing.html", {
            'product': product,
            'listing_description': markdown2.markdown(product.description),
            'bid_user': bid_user,
        })
    else:
        # remove the listing from database after closing
        product = Product.objects.get(id=request.session['product_id'])
        user = User.objects.get(username=request.user)
        winning_user = Bid.objects.filter(product=product).order_by('-bid')
        if len(winning_user) > 0:
            winning_user = winning_user[0].user
        else:
            winning_user = None
        print ("line 94", user, product, winning_user)
        ClosedProduct.objects.create(user=user, product=product, winning_user=winning_user) 
        product.closed = True
        product.save()
        request.session['closed'] = True
        return HttpResponseRedirect("/")

        
@login_required(login_url="/login")
def comment(request):
    
    # saves new comments in database and links it with the product
    comment_form = commentForm(request.POST)    
    temp_comment = comment_form.save(commit=False)
    temp_comment.user = User.objects.get(username=request.user)
    temp_comment.product = Product.objects.get(id=request.session['product_id'])
    temp_comment.save()
    return HttpResponseRedirect(f"listings/{request.session['product_id']}")


@login_required(login_url="/login")
def create_listings(request):
    if request.method == "POST":
        create_form = createForm(request.POST)
        if create_form.is_valid():
            temp_form = create_form.save(commit=False)
            temp_form.user = User.objects.get(username=request.user)
            temp_form.description = markdown2.markdown(temp_form.description)
            
            # check if image_url or/and category is left empty
            if len(temp_form.image_url) < 1:
                temp_form.image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"
            if len(temp_form.category) < 1:
                temp_form.category = "Others"
            
            temp_form.save()
            return HttpResponseRedirect(f"/listings/{temp_form.id}")
    else:
        create_form = createForm()
        return render(request, "auctions/create.html", {
            'create_form': create_form
        })


def display_listing(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.closed:
        return render(request, "auctions/listing_closed.html")
    
    request.session['product_id'] = product_id
    bid_form = bidForm()
    comment_form = commentForm()  

    # for placeholder in bid field to show greater than current_bid or opening_bid
    if product.current_bid == 0:
        bid_form.fields['bid'].widget.attrs['placeholder'] = f"Higher than ${product.opening_bid}.00"
    else:
        bid_form.fields['bid'].widget.attrs['placeholder'] = f"Higher than ${product.current_bid}.00"
  
    # to handle the error if no bid is placed yet while accessing bid-user
    bid_user = Bid.objects.filter(product=product).order_by('-bid')
    if len(bid_user) > 0:
        bid_user = bid_user[0].user
    else:
        bid_user = False
    
    # to handle the error when no comments are made while diplaying the comments
    try:
        comments = Comment.objects.filter(product=Product.objects.get(id=product_id))
    except Comment.DoesNotExist:
        comments = "No Comments!"
    request.session['product_id'] = product_id
    
    # to handle the error when watchlist is empty while trying to access it
    try:
        watch_list = Watchlist.objects.get(
            user=User.objects.get(username=request.user),
            product=product)
        watchlist = True
    except User.DoesNotExist:
        watchlist = False
    except Watchlist.DoesNotExist:
        watchlist = False
    
    # to check if the invalid <div> has to be displayed
    try:
        invalid_bid = request.session['invalid_bid']
        request.session['invalid_bid'] = False
    except KeyError:
        invalid_bid = False
    
    # to check whether to display the close_auction button on listing
    try:
        if product.user == User.objects.get(username=request.user):
            close_listing = True
        else: 
            close_listing = False
    except User.DoesNotExist:
        close_listing = False

    # to check if bids are yet to be placed
    try: 
        bid_history = Bid.objects.filter(product=product)
    except:
        bid_history = None

    return render(request, "auctions/listing.html", {
                'product': product,
                'bid_history': bid_history,
                'close_listing': close_listing,
                'listing_description': markdown2.markdown(product.description),
                'watchlist': watchlist,
                'comments': comments,
                'invalid_bid': invalid_bid,
                'bid_user': bid_user,
                'bid_form': bid_form,
                'comment_form': comment_form
            })


def filter_categories(request, cat):
    
    # display products of selected category
    products = Product.objects.filter(category=cat)
    return render(request, "auctions/categories.html", {
        'products': products,
        'title': cat
    })


def index(request):
    
    # to check if the listing closed <div> has to be displayed
    try:
        closed = request.session['closed']
        request.session['closed'] = False
    except KeyError:
        closed = False

    return render(request, "auctions/index.html", {
        'closed': closed,
        'listings': Product.objects.all(),
        'index_page': True,
        'heading': "Active Listing"
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


@login_required(login_url="/login")
def my_watchlist(request):
    products = Watchlist.objects.filter(user=User.objects.get(username=request.user))
    products = [i.product for i in products]
    return render(request, "auctions/categories.html", {
        'products': products,
        'title': "My Watchlist",
    })


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

@login_required(login_url="/login")
def watchlist(request):
    
    # to handle error while removing from watchlist
    try:
        watch_list = Watchlist.objects.get(
            user=request.user,
            product= Product.objects.get(id=request.session['product_id']) 
            )
    except Watchlist.DoesNotExist:
        watch_list = Watchlist()
        watch_list.user = User.objects.get(username=request.user)
        watch_list.product = Product.objects.get(id=request.session['product_id'])
        watch_list.save()
        return HttpResponseRedirect(f"listings/{request.session['product_id']}")
    
    watch_list.delete()
    return HttpResponseRedirect(f"listings/{request.session['product_id']}")

@login_required(login_url="/login")
def my_winnings(request):
   
    # display products of selected category
    products = ClosedProduct.objects.filter(winning_user=request.user)
    products = [i.product for i in products]
    return render(request, "auctions/index.html", {
        'listings': products,
        'title': "My Winnings",
        'heading': "My Winnings",
        'index_page': False
    })
