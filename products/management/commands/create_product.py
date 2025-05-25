from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Product
from products.choices import Currency
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker()
        currency_data = [
            Currency.GEL,
            Currency.USD,
            Currency.EURO
        ]
        products_to_create = []
        
        for _ in range(1000):
            name = faker.name()
            description = faker.text()
            price = round(random.uniform(1, 1000), 2)
            currency = random.choice(currency_data)
            quantity = random.randint(1, 100)
            
            product = Product(
                name = name,
                description = description,
                price = price,
                currency = currency,
                quantity = quantity
            )
            products_to_create.append(product)
            
        Product.objects.bulk_create(products_to_create, batch_size=100)
        print(f'Created {len(products_to_create)} products')