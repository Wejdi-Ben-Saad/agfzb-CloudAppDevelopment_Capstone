"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator


# from cloudant.client import Cloudant
# from cloudant.error import CloudantException

from requests import ConnectionError, RequestException


def main(param):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    
    try:
        authenticator = IAMAuthenticator(param["IAM_API_KEY"])

        service = CloudantV1(authenticator=authenticator)

        service.set_service_url(param["COUCH_URL"])
    except ApiException as cloudant_exception:
        print("unable to connect")
        return {"body":{"error": str(cloudant_exception)}}
    except (RequestException, ConnectionError, ConnectionResetError) as err:
        print("connection error")
        return {"body":{"error": str(err)}}
    selector={}
    if "dealerId" in param :
        selector["id"] = int(param["dealerId"])
    review_list = service.post_find("reviews",selector).get_result()["docs"]
    for review in review_list:
        if "_id" in review:
            del review["_id"]
        if "_rev" in review:
            del review["_rev"]
    return {"body": review_list}

def post_review(param):
    try:
        authenticator = IAMAuthenticator(param["IAM_API_KEY"])

        service = CloudantV1(authenticator=authenticator)

        service.set_service_url(param["COUCH_URL"])
    except ApiException as cloudant_exception:
        print("unable to connect")
        return {"body":{"error": str(cloudant_exception)}}
    except (RequestException, ConnectionError, ConnectionResetError) as err:
        print("connection error")
        return {"body":{"error": str(err)}}

    if param:
        name=""
        dealership= -1
        review= ""
        purchase= False
        another= ""
        purchase_date= ""
        car_make= ""
        car_model= ""
        car_year=0
        if ("review" in param) and(type(param["review"]) is dict):
            if "name" in param["review"]:
                name= param["review"]["name"]
            if "dealership" in param["review"]:
                dealership= param["review"]["dealership"]
            if "review" in param["review"]:
                review= param["review"]["review"]
            if "purchase" in param["review"]:
                purchase= param["review"]["purchase"]
            if "another" in param["review"]:
                another= param["review"]["another"]
            if "purchase_date" in param["review"]:
                purchase_date= param["review"]["purchase_date"]
            if "car_make" in param["review"]:
                car_make= param["review"]["car_make"]
            if "car_model" in param["review"]:
                car_model= param["review"]["car_model"]
            if "car_year" in param["review"]:
                car_year= param["review"]["car_year"]
            review_document= Document( 
                    name= name,
                    dealership= dealership,
                    review= review,
                    purchase= purchase,
                    another= another,
                    purchase_date= purchase_date,
                    car_make= car_make,
                    car_model= car_model,
                    car_year= car_year
            )
            response = service.post_document(db='reviews',document=review_document).get_result()
            return {"body": response}
        
    return {"body":{"error": 500}}




