from rest_framework.serializers import PrimaryKeyRelatedField, IntegerField, ValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from mongoengine.fields import StringField, ReferenceField, EmailField
from .models import User, Category, Product, Cart, Order, Coupon, CartItem, OrderItem
from bson import ObjectId
from mongoengine.errors import ValidationError
from rest_framework import serializers

class UserSerializer(DocumentSerializer):
    id = StringField(read_only=True)
    username = StringField()
    email = EmailField()
    password = StringField(write_only=True)

    class Meta:
        model = User  # Add the model attribute
        fields = ['id', 'username', 'email', 'password']  # Specify the fields to include
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CategorySerializer(DocumentSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(DocumentSerializer):
    category = ReferenceField(Category)
    
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(EmbeddedDocumentSerializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())  # Correct field type
    quantity = IntegerField()

    class Meta:
        model = CartItem  # Ensure this points to the correct model
        fields = '__all__'  # Include all fields or specify them explicitly

    def to_representation(self, instance):
        """Convert ObjectId fields to strings before sending JSON response."""
        data = super().to_representation(instance)

        # Convert ObjectId fields to string
        if isinstance(data.get('id'), ObjectId):
            data['id'] = str(data['id'])

        if isinstance(data.get('product'), ObjectId):
            data['product'] = str(data['product'])

        return data

class CartSerializer(DocumentSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())  # Correct field type
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart  # Add this line
        fields = '__all__'  # Include all fields

    def create(self, validated_data):
        user = validated_data.get('user')

        # Check if the user already has a cart
        cart = Cart.objects(user=user).first()
        if not cart:
            cart = Cart(user=user)  # Create a new Cart
        else:
            cart.items = []  # Reset items if cart already exists

        items_data = validated_data.pop('items', [])
        for item_data in items_data:
            cart_item = CartItem(**item_data)  # Create the CartItem (NO .save())
            cart.items.append(cart_item)  # Add it to cart.items (NO .save())

        cart.save()  # Save the entire Cart document (this saves the embedded items)

        return cart
    
    def to_representation(self, instance):
        """Convert ObjectId fields to strings before sending JSON response."""
        data = super().to_representation(instance)

        # Convert ObjectId to string
        if isinstance(data.get('id'), ObjectId):
            data['id'] = str(data['id'])

        if isinstance(data.get('user'), ObjectId):
            data['user'] = str(data['user'])

        return data

class OrderItemSerializer(serializers.Serializer):
    product = serializers.CharField()  # Expecting the product ID as a string
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_product(self, value):
        # Validate that the product ID exists
        try:
            product = Product.objects.get(id=ObjectId(value))  # Convert to ObjectId
        except Product.DoesNotExist:
            raise ValidationError(f"Product with id {value} does not exist.")
        return product

class OrderSerializer(serializers.Serializer):
    user = serializers.CharField()  # Adjust the field according to your User model type
    order_number = serializers.CharField(max_length=255)  # Ensure it's unique
    status = serializers.CharField(max_length=255)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = serializers.CharField(max_length=255)
    items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        user = validated_data.pop('user')
        items_data = validated_data.pop('items')

        # Create the Order instance
        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            product_ref = item_data.pop('product')  # Extract the product and remove it from item_data

            # Create OrderItem instances
            order_item = OrderItem(product=product_ref, **item_data)  # Pass product_ref separately
            order.items.append(order_item)

        order.save()  # Save the order and its items
        return order

class CouponSerializer(DocumentSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'