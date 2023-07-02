from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
#from .models import CarDealer
from .restapis import get_dealers_from_cf, get_dealers_by_state,get_dealers_by_id, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.



def about(request):
    return render(request,"djangoapp/about.html")



# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,"djangoapp/contact_us.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context ={}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)
    
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")




# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request,"djangoapp/registration.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False

    try:
        User.objects.get(username=username)
        user_exist = True
    except:
        logger.error("New user")
    if not user_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                        password=password)
        login(request, user)
        return redirect("djangoapp:index")
    else:
        context['message'] = "User already exists."
        return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    
def get_dealerships_by_state(request,state="Texas"):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_state(url,state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    
def get_dealerships_by_id(request,id=1):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_id(url,id)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/dealership-package/get-review"
        # Get reviews from the URL
        reviews = get_dealer_by_id_from_cf(url,dealer_id)
        reviews = ' '.join([review.review+":"+review.sentiment+"<br>" for review in reviews])
        return HttpResponse(reviews)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    json_result={}
    if request.method =="POST":
        #if request.user.is_authenticated:
        url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/actions/dealership-package/post-review"
        api_key="_GuQrqFdEw6XzhL7xiLHa5yycwSy6evIf6xijUeaiGwz"
        review={}
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = "This is a great car dealer"
        json_payload={}
        json_payload["review"]=review
        json_result = post_request(url, api_key,json_payload)
    return HttpResponse(json_result)

            

