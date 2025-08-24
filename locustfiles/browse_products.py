from random import randint
from locust import HttpUser, TaskSet, task, between


class WebstiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        # generate a collection_id randomly
        collection_id = randint(2, 6)
        # define a request
        self.client.get(
            f"/store/products/?collection_id={collection_id}",
            name="/store/products/",
        )

    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(
            f"/store/products/{product_id}",
            name="/store/products/:id",
        )

    @task(1)
    def add_to_cart(self):
        # override on_start method to create a cart and get it's id
        cart_id = self.cart_id
        product_id = randint(1, 10)
        self.client.post(
            f"/store/carts/{cart_id}/items/",
            name="/store/carts/items",
            json={
                "product_id": product_id,
                "quantity": 1,
            },
        )

    def on_start(self):
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
