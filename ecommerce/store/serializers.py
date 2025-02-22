from rest_framework import serializers
from .models import Order, OrderItem, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'total_price', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, total_price=0)  

        total_price = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if product.stock_quantity < quantity:
                raise serializers.ValidationError(f"Product {product.name} is out of stock.")

            product.stock_quantity -= quantity
            product.save()

            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            total_price += product.price * quantity

        order.total_price = total_price
        order.save()
        return order
