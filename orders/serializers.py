from rest_framework import serializers
from .models import Order, OrderItem
from store.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'address1', 'address2', 'city', 'phone', 'post_code', 'created', 'updated', 'total_paid', 'order_key', 'billing_status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.user = validated_data.get('user', instance.user)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.city = validated_data.get('city', instance.city)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.post_code = validated_data.get('post_code', instance.post_code)
        instance.total_paid = validated_data.get('total_paid', instance.total_paid)
        instance.order_key = validated_data.get('order_key', instance.order_key)
        instance.billing_status = validated_data.get('billing_status', instance.billing_status)
        instance.save()

        # Update order items
        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                item = OrderItem.objects.get(id=item_id, order=instance)
                item.product = item_data.get('product', item.product)
                item.price = item_data.get('price', item.price)
                item.quantity = item_data.get('quantity', item.quantity)
                item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
    
class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']

class CreateOrderSerializer(serializers.Serializer):
    order_key = serializers.CharField(max_length=255)
    full_name = serializers.CharField(max_length=255)
    address1 = serializers.CharField(max_length=255)
    address2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            order_item_data = CreateOrderItemSerializer(data=item_data)
            order_item_data.is_valid(raise_exception=True)
            order_item = order_item_data.create(order_item_data.validated_data)
            order_item.order = order
            order_item.save()

        return order