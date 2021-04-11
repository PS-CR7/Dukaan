# Python imports
from typing import Dict, Any
# django/rest_framwork imports
from model_utils import Choices
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
# app level imports
import uuid
from .managers import UserManager
from django.contrib.postgres.fields import JSONField

class Account(AbstractBaseUser):
    """
    User model represents the user data in the database.
    """

    mobile = models.BigIntegerField(
        unique=True,
        null=True,)
    is_staff = models.BooleanField(
        default=False,
    )
    password = models.CharField(max_length=256, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    objects = UserManager()

    USERNAME_FIELD = "mobile"

    class Meta:
        db_table = "account"

    def __str__(self):
        return str(self.mobile)

    def modify(self, payload: Dict[str, Any]):
        """
        This will update license object
        """
        for key, value in payload.items():
            setattr(self, key, value)
        self.save()

class Store(models.Model):
    customer= models.ForeignKey('Account', on_delete=models.CASCADE)
    store_name = models.CharField(max_length=64, blank=False)
    address = models.CharField(max_length=64, blank= False)
    store_link = models.CharField(max_length=128, blank= False, default=uuid.uuid4)

class Product(models.Model):
    store= models.ForeignKey('Store',on_delete=models.CASCADE)
    product_name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=64, blank= False)
    mrp = models.CharField(max_length=64, blank=False)
    sale_price = models.CharField(max_length=64, blank= False)
    image = models.TextField(blank=True)
    category = models.CharField(max_length=64, blank= False)

class Customer(models.Model):
    mobile = models.BigIntegerField(
        unique=True, null=False,)
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=64, blank=False)

class Order(models.Model):
    buyer= models.ForeignKey('Customer',on_delete=models.CASCADE)
    order_item = JSONField()

class Cart(models.Model):
    session = models.CharField(max_length=64, blank=False)
    items = JSONField()





