from django.db.backends.signals import connection_created
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.dispatch import receiver

from .models import Product, Category
from django.db.models import Model
import csv
        
def read_products(file:str) -> list[Product]:
    __products__ = []
    with open(file, mode='r', newline='') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Read the header row (if present)
        header = next(csv_reader)
        
        # Iterate over the rows in the CSV file
        for row in csv_reader:
            title = row[header.index("title")]
            description = row[header.index("description")]
            category = row[header.index("category")]
            price = row[header.index("price")]
            stock = row[header.index("stock")]
            __product__ = Product.objects.create(title=title, description=description, 
                                                price=price, stock=stock)
            __product__.category.set([Category.objects.get(title=category)])
            __products__.append(__product__)
        
    return __products__

def read_categories(file:str) -> list[Category]:
    __categories__ = []
    with open(file, mode='r', newline='') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Read the header row (if present)
        header = next(csv_reader)
        
        # Iterate over the rows in the CSV file
        for row in csv_reader:
            title = row[header.index("title")]
            description = row[header.index("description")]
            __category__ = Category.objects.create(title=title, description=description)
            __categories__.append(__category__)
        
    return __categories__

def save_models(list:list[Model]) -> None:
    for mdl in list:
        mdl.save()

@receiver(connection_created, sender=DatabaseWrapper)
def initial_connection_to_db(sender, **kwargs):
    if Category.objects.count() == 0:
        save_models(read_categories('store/dummy_categories.csv'))
    if Product.objects.count() == 0:
        save_models(read_products('store/dummy_products.csv'))