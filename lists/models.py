from django.db import models
#from django.test import TestCase

# Create your models here
class List(models.Model):
    pass

class Item(models.Model):
    '''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
