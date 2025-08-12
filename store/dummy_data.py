from store.models import Product, Collection
from decimal import Decimal
import random

# Get all collections from the database
collections = Collection.objects.all()

# Ensure there are collections to assign products to
if not collections:
    print("No collections found. Please create collections first.")
else:
    for i in range(1, 21):
        # Select a random collection to assign to the product
        random_collection = random.choice(collections)

        # Create the product instance
        Product.objects.create(
            title=f'Product {i}',
            slug=f'product-{i}',
            unit_price=Decimal(random.randint(10, 100)),
            inventory=random.randint(10, 50),
            collection=random_collection
        )

    print('20 products created and assigned to collections.')