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
from .models import CarModel
from .credentials import credentials_dictionary

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
        context["dealerships"] = dealerships
        # Return a list of all dealerships in the context variable
        return render(request,"djangoapp/index.html", context=context)
    
def get_dealerships_by_state(request,state="Texas"):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_state(url,state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    
def get_dealerships_by_id(id=1):
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/dealership-package/get-dealership"
        # Get dealer from the URL
        dealerships = get_dealers_by_id(url,id)
        # Concat all dealer's short name
        dealer_name = ''
        if dealerships:
            dealer_name = ''.join(dealerships[0].full_name)
        # Return a list of dealer short name
        return dealer_name
    


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/02ddb919-0a17-4fb5-a9db-36ebc037a2e9/dealership-package/get-review"
        # Get reviews from the URL
        reviews = get_dealer_by_id_from_cf(url,dealer_id)
        context["reviews"]=reviews
        dealer =get_dealerships_by_id(dealer_id)
        context["dealer"]=dealer
        context["dealer_id"]=dealer_id
        return render(request,"djangoapp/dealer_details.html",context=context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    json_result={}
    if request.method =="POST":
        if request.user.is_authenticated:
            url = credentials_dictionary["add_review"]["url"]
            api_key = credentials_dictionary["add_review"]["api_key"]

            review={}
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
        
            review["name"]=request.user.username
            
            if "content" in request.POST:
                review["review"]= request.POST['content']

            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"]=="on":
                    review["purchase"] =  True
                else:
                    review["purchase"] =  False

            if "purchasedate" in request.POST :
                review["purchase_date"]= request.POST["purchasedate"]
            if "car" in request.POST :
                car = CarModel.objects.get(id=int(request.POST['car'])) 
                review["car_make"]= car.car_make.name
                review["car_model"]= car.name
                review["car_year"]= int(car.year.strftime("%Y"))

        
            json_payload={}
            json_payload["review"]=review
            json_result = post_request(url, api_key,json_payload)
            return redirect("djangoapp:dealer_details",dealer_id)
    if request.method =="GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context={}
        context["dealer_id"] = dealer_id
        dealer =get_dealerships_by_id(dealer_id)
        context["dealer"] = dealer
        context["cars"] = cars
        return render(request,"djangoapp/add_review.html",context=context)

            

