from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return "Make Name:"+self.name+","+\
                "Make Description:"+self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealer_id = models.IntegerField()
    CAR_TYPE_CHOICES = [
        ("Sedan","Sedan"), 
        ("SUV","SUV"),
        ("WAGON","WAGON"),
    ]
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    year = models.DateField()
    def __str__(self):
        return  "Make Name:"+self.car_make.name+","+\
                "Model Name:"+self.name+","+\
                "type:"+self.car_type+","+\
                "year:"+str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
