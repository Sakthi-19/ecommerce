from mongoengine import Document, fields, EmbeddedDocument
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

class User(Document):
    username = fields.StringField(required=True, unique=True)
    email = fields.EmailField()
    password = fields.StringField(required=True)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    date_joined = fields.DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'email'],
        'app_label': 'core'
    }

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    @property
    def is_authenticated(self):
        return self.is_active  # You can customize this based on your business logic

class Category(Document):
    name = fields.StringField(max_length=100, unique=True)
    description = fields.StringField(blank=True)
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'categories',
        'indexes': ['name'],
        'app_label': 'core'
    }

class Product(Document):
    category = fields.ReferenceField(Category)
    name = fields.StringField(max_length=255)
    description = fields.StringField()
    price = fields.FloatField()
    stock = fields.IntField(default=0)
    image = fields.StringField(blank=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'products',
        'indexes': ['name', 'category', 'price', 'is_active'],
        'app_label': 'core'
    }

class CartItem(EmbeddedDocument):
    product = fields.ReferenceField(Product)
    quantity = fields.IntField(default=1)
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
    
    @property
    def total_price(self):
        return float(self.product.price) * self.quantity

class Cart(Document):
    user = fields.ReferenceField(User, unique=True)
    items = fields.ListField(fields.EmbeddedDocumentField(CartItem))
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'carts',
        'app_label': 'core'
    }
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items)

class OrderItem(EmbeddedDocument):
    product = fields.ReferenceField(Product)  # Link to the Product model
    quantity = fields.IntField()
    price = fields.FloatField()

    @property
    def total_price(self):
        return self.price * self.quantity

class Order(Document):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    )
    
    user = fields.ReferenceField(User)
    order_number = fields.StringField(unique=True)
    status = fields.StringField(choices=STATUS_CHOICES, default='P')
    total_price = fields.FloatField()
    shipping_address = fields.StringField()
    items = fields.ListField(fields.EmbeddedDocumentField(OrderItem))
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'orders',
        'indexes': ['user', 'order_number', 'status', 'created_at'],
        'app_label': 'core'
    }

class Coupon(Document):
    code = fields.StringField(max_length=20, unique=True)
    discount_percent = fields.IntField()
    max_discount = fields.FloatField(null=True)
    min_order_value = fields.FloatField(null=True)
    valid_from = fields.DateTimeField()
    valid_to = fields.DateTimeField()
    is_active = fields.BooleanField(default=True)
    max_usage = fields.IntField(null=True)
    used_count = fields.IntField(default=0)
    
    meta = {
        'collection': 'coupons',
        'indexes': ['code', 'is_active', 'valid_from', 'valid_to'],
        'app_label': 'core'
    }