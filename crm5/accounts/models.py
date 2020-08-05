from django.db import models

# 后台的table在这儿连
class Location(models.Model): #parent model
    cityName =models.CharField(max_length=50)
    zipCode =models.IntegerField(max_length=50)
    def __str__(self):
        return self.cityName


class Seller(models.Model):
    username =models.CharField(max_length=50)
    password =models.CharField(max_length=50)
    filt_c = models.FloatField(null = True)
    email = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.username

# class Category(models.Model):
#     name =models.CharField(max_length=50)

class Product(models.Model): #child model
    location = models.ForeignKey(Location, null = True, on_delete=models.SET_NULL)
    CATEGORY = (
			('Lifestyle', 'Lifestyle'),
			('Kitchen', 'Kitchen'),
            ('Fashion','Fashion'),
            ('Beauty','Beauty'),
            ('Study','Study'),
			)
    productName =models.CharField(max_length=500)
    price = models.FloatField(null = True)
    depreciation = models.FloatField(null = True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY) #category只能选
    seller = models.ForeignKey(Seller, null = True, on_delete=models.SET_NULL)
    filt_p = models.FloatField(null = True)


    def __str__(self):
        return self.productName
