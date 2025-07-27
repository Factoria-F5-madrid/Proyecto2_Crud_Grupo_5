# compra/serializers.py
from rest_framework import serializers
from django.db import transaction # Importamos transaction para asegurar la integridad de los datos
from .models import Order, OrderItem
from cliente.models import Customer
from prenda.models import Product

# Serializador para Product (uso general y anidado si es necesario)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description'] # O los campos que desees mostrar del Product

# Serializador para OrderItem (uso individual en endpoint, ej: /api/order-items/)
class OrderItemSerializer(serializers.ModelSerializer):
    # Para la entrada (POST/PUT/PATCH), acepta solo el ID del producto.
    # write_only=True significa que este campo solo se usa para la entrada de datos,
    # no se incluirá en la respuesta serializada.
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    
    # Para la salida (GET), muestra los detalles completos del producto.
    # read_only=True significa que este campo solo se usa para la salida de datos,
    # no se espera en la entrada. 'source='product'' indica que toma los datos
    # del campo 'product' del modelo subyacente.
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        # Incluimos 'product' para la entrada y 'product_details' para la salida.
        # Es crucial que 'product' esté aquí para que 'write_only=True' funcione.
        # 'product_details' es un campo de solo lectura que se genera a partir de 'product'.
        fields = ['id', 'order', 'product', 'quantity', 'product_details']
        read_only_fields = ('id', 'product_details',)


# Serializador para OrderItem cuando está ANIDADO dentro de Order
# Esta clase es la que se usa dentro de OrderSerializer para la representación anidada.
class NestedOrderItemSerializer(serializers.ModelSerializer):
    """
    Serializador para OrderItem cuando se usa de forma anidada dentro de OrderSerializer.
    """
    # === CORRECCIÓN CLAVE AQUÍ ===
    # Para la entrada (POST/PUT/PATCH), acepta solo el ID del producto.
    # NO es write_only=True porque el OrderSerializer necesita leer este campo para crear el OrderItem.
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    # product_name se muestra para legibilidad en la respuesta (solo lectura).
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        # No incluimos 'order' aquí porque se infiere de la relación con el Order padre.
        # Incluimos 'price' para que se pueda establecer el precio unitario
        fields = ['id', 'product', 'product_name', 'quantity', 'price']
        read_only_fields = ('id', 'product_name',) # 'id' es autogenerado, 'product_name' es solo para lectura


# Serializador principal para Order (con anidación writable)
class OrderSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Order, con soporte para OrderItems anidados (lectura/escritura).
    """
    # 'items' usa el NestedOrderItemSerializer y NO es read_only, permitiendo escritura anidada.
    items = NestedOrderItemSerializer(many=True)

    # customer_name se muestra para legibilidad en la respuesta, pero es read_only.
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        # Incluye 'items', 'customer_name' y 'total_amount' en los campos que se serializarán.
        fields = ['id', 'customer', 'customer_name', 'order_date', 'total_amount', 'status', 'items']
        read_only_fields = ('id', 'order_date', 'customer_name', 'total_amount',)

    # --- Método CREATE personalizado para manejar la creación de OrderItems anidados ---
    def create(self, validated_data):
        order_items_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item_data in order_items_data:
                # El campo 'product' en item_data ya es una instancia de Product
                # porque PrimaryKeyRelatedField en NestedOrderItemSerializer
                # ya lo ha validado y convertido.
                # No necesitas la validación Product.objects.filter(...).exists() aquí.
                OrderItem.objects.create(order=order, **item_data)
        return order

    # --- Método UPDATE personalizado para manejar la actualización de OrderItems anidados ---
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('items', None)

        with transaction.atomic():
            instance.customer = validated_data.get('customer', instance.customer)
            instance.save()

            if order_items_data is not None:
                instance.items.all().delete() # Borra todos los OrderItems asociados a esta Order.

                for item_data in order_items_data:
                    # Similar al create, 'product' en item_data ya es una instancia de Product.
                    OrderItem.objects.create(order=instance, **item_data)
        return instance
