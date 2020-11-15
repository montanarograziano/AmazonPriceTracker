

class Product:
    def __init__(self, name, price, prev_price, link, discount):
        self.name = name
        self.price = price
        self.prev_price = prev_price
        self.link = link
        self.discount = discount
    
    def __lt__(self, other):
        return self.discount < other.discount
    
    def serialize(self):
        return {
            "name" : self.name,
            "price" : self.price,
            "prev_price" : self.prev_price,
            "link" : self.link,
            "discount" : self.discount
        }
    
    def from_json(self, json_):
        self.name = json_["name"]
        self.price = json_["price"]
        self.prev_price = json_["prev_price"]
        self.link = json_["link"]
        self.discount = json_["discount"]