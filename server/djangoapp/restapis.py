import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if api_key:
            # Basic authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs,
                                        auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs) 
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, api_key=None,json_payload={}, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        if api_key:
            #generate IAM token from api key
            token_url='https://iam.cloud.ibm.com/identity/token'
            token_response = requests.post(token_url,headers={'Content-Type': 'application/x-www-form-urlencoded'},data='grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey='+api_key)
            json_token_data = json.loads(token_response.text)
            iam_token = json_token_data["access_token"]
            #authentication with IAM token
            response = requests.post(url, headers={'Content-Type': 'application/json',"Authorization": "Bearer "+iam_token}, params=kwargs,json=json_payload,
                                        )
        else:
            # no authentication GET
            response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs,json=json_payload) 
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

def get_dealers_by_state(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


def get_dealers_by_id(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,id=id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the reviews list
        reviews = json_result
        # For each review_item object
        for review_item in reviews:

            dealership=review_item["dealership"]
            name=review_item["name"]
            purchase=review_item["purchase"]
            review=review_item["review"]
            purchase_date=review_item["purchase_date"] if "purchase_date" in review_item else "" 
            car_make=review_item["car_make"] if "car_make" in review_item else ""
            car_model=review_item["car_model"] if "car_model" in review_item else ""
            car_year=review_item["car_year"] if "car_year" in review_item else 0
            id=review_item["id"] if "id" in review_item else review_item["_id"]
            # Create a DealerReview 
            review_obj = DealerReview(dealership=dealership , name=name, purchase=purchase, review=review, purchase_date=purchase_date, car_make=car_make, car_model=car_model, car_year=car_year, id=id)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/939f5955-4e1f-428d-b7ee-214ea1ee3ef8/v1/analyze"
    api_key = "mEBhFsTKwnGJ9tUJAU5d444HdbVzxp4Cm3LLyl7OFxt5"
    
    params = dict()
    params["text"] = review
    params["version"] = "2022-04-07"
    params["features"] = {"sentiment": True}
    params["return_analyzed_text"] = False
    json_result = get_request(url, api_key, **params)
    sentiment_label = ""
    if "sentiment" in json_result:
        sentiment_label = json_result["sentiment"]["document"]["label"]
    return sentiment_label
    



