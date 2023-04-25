import csv


class Product:
    def __init__(self, product_id, product_name, product_price):
        self._product_id = product_id
        self._product_name = product_name
        self._product_price = product_price
        self._quantity = 0
        self.purchase_history = []
        self.order_history = []

    def add_purchase_history(self, quantity, price):
        self.purchase_history.append((quantity, price))
        self.quantity += quantity

    def add_order_history(self, quantity, price):
        self.order_history.append((quantity, price))
        self.quantity -= quantity

    @property
    def product_id(self):
        return self._product_id

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        self._product_name = value

    @property
    def product_price(self):
        return self._product_price

    @product_price.setter
    def product_price(self, value):
        self._product_price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    def avg_price(self):
        if not self.purchase_history:
            return 0

        total_quantity = sum(q for q, _ in self.purchase_history)
        total_price = sum(quantity * price for quantity,
                          price in self.purchase_history)

        return total_price / total_quantity

    def avg_order_price(self):
        if not self.order_history:
            return 0
        total_quantity = sum(q for q, _ in self.order_history)
        total_price = sum(quantity * price for quantity,
                          price in self.order_history)
        return total_price / total_quantity

    def num_of_orders(self):
        return sum(q for q, _ in self.order_history)


class Ecommerce:
    def __init__(self):
        self.products = {}
        self.commands = {
            "save_product": self.save_product,
            "purchase_product": self.purchase_product,
            "order_product": self.order_product,
            "get_quantity_of_product": self.get_quantity_of_product,
            "get_average_price": self.get_average_price,
            "get_product_profit": self.get_product_profit,
            "get_fewest_product": self.get_fewest_product,
            "get_most_popular_product": self.get_most_popular_product,
            "get_orders_report": self.get_orders_report,
            "export_orders_report": self.export_orders_report
        }

    def save_product(self, product_id, product_name, product_price):
        if product_id not in self.products:
            self.products[product_id] = Product(
                product_id, product_name, product_price)
        else:
            self.products[product_id].product_name = product_name
            self.products[product_id].product_price = product_price
        # აქ ვუშვებ რომ თუ უკვე არსებობს პროდუქტი, თავიდან შენახვის შემთხვევაში
        # ფასი და სახელი ეცვლება შესაბამისად.

    def purchase_product(self, product_id, quantity, product_price):
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found in products..")
            return

        product = self.products.get(product_id)
        product.add_purchase_history(quantity, product_price)

    def order_product(self, product_id, quantity):
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found in products..")
            return

        product = self.products.get(product_id)
        if product.quantity < quantity:
            print(f"Can't buy that much {product_id}.")
            return
        product.add_order_history(quantity, product.product_price)

    def get_quantity_of_product(self, product_id):
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found in products..")
            return

        product = self.products.get(product_id)
        print(product.quantity)
        return

    def get_average_price(self, product_id):
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found in products..")
            return

        product = self.products.get(product_id)
        average_price = product.avg_price()
        print(f"{average_price:.2f}")
        return

    def get_product_profit(self, product_id):
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found in products..")
            return

        product = self.products.get(product_id)
        avg_purchase = product.avg_price()
        avg_order = product.avg_order_price()
        price_diff = avg_order - avg_purchase

        profit = sum(price_diff * quantity for quantity,
                     _ in product.order_history)
        print(f"{profit:.2f}")

    def get_fewest_product(self):
        if not self.products:
            print("No products")
            return
        fewest = min(self.products.values(), key=lambda p: p.quantity)
        print(f"{fewest.product_name}")

    def get_most_popular_product(self):
        if not self.products:
            print("No products")
            return

        popular = max(self.products.values(), key=lambda p: p.num_of_orders())
        print(f"{popular.product_name}")

    def get_orders_report(self):
        orders = []
        for product in self.products.values():
            for quantity, price in product.order_history:
                cogs = product.avg_price() * quantity
                sell_price = price * quantity
                one_product = {
                    "Product ID": product.product_id,
                    "Product Name": product.product_name,
                    "COGS": cogs,
                    "Quantity": quantity,
                    "Price": price,
                    "Sell Price": sell_price,
                }
                orders.append(one_product)
        for o in orders:
            print(o)
        return orders

    def export_orders_report(self, path):
        orders = self.get_orders_report()

        with open(path, 'w', newline='', encoding='utf-8') as file_csv:
            fields = [
                "Product ID",
                "Product Name",
                "COGS",
                "Quantity",
                "Price",
                "Sell Price"
            ]
            writer = csv.DictWriter(file_csv, fields)

            writer.writeheader()
            for o in orders:
                writer.writerow(o)

    def run(self):
        converter = {
            "save_product": (str, str, float),
            "purchase_product": (str, int, float),
            "order_product": (str, int),
            "get_quantity_of_product": (str,),
            "get_average_price": (str,),
            "get_product_profit": (str,),
            "get_fewest_product": (),
            "get_most_popular_product": (),
            "get_orders_report": (),
            "export_orders_report": (str,)
        }

        while True:
            command = input("Enter command: ").split()
            cmd, *args = command
            if cmd == "exit":
                break
            elif cmd in self.commands:
                converted_args = [conv(arg)
                                  for conv, arg in zip(converter[cmd], args)]
                self.commands[cmd](*converted_args)
            else:
                print(f"Invalid command: {cmd}")


if __name__ == "__main__":
    app = Ecommerce()
    app.run()
