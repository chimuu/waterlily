import uuid

from rest_framework import serializers

from order.models.order import Order
from waterlily.settings import ORDER_IMAGE_BASE_URL
from waterlily.settings import ORDER_IMAGE_LOCATION
from base64 import b64decode


class MeasurementDetailsSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True)
    display = serializers.CharField(allow_blank=True)


class BillDetailsSerializer(serializers.Serializer):
    type = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()


class MeasurementsSerializer(serializers.Serializer):
    measurement_type = serializers.CharField()
    details = serializers.ListField(child=MeasurementDetailsSerializer())
    note = serializers.CharField(allow_blank=True)


class BillSerializer(serializers.Serializer):
    details = serializers.ListField(child=BillDetailsSerializer())
    total_price = serializers.FloatField()
    note = serializers.CharField(allow_blank=True)


class BaseOrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_mobile = serializers.IntegerField()
    customer_address = serializers.CharField(allow_blank=True)
    measurements = serializers.ListField(child=MeasurementsSerializer())
    bill = BillSerializer()
    delivery_date = serializers.DateTimeField()

    def create(self, validated_data):
        last_order = Order.objects.filter(user=self.context['request'].user).order_by('id').last()
        if last_order:
            serial_no = last_order.serial_no + 1
        else:
            serial_no = 1
        order = Order(user=self.context['request'].user, serial_no=serial_no, **validated_data)
        order.save()
        return order

    def update(self, instance, validated_data):
        instance.customer_name = validated_data['customer_name']
        instance.customer_mobile = validated_data['customer_mobile']
        instance.customer_address = validated_data['customer_address']
        instance.measurements = validated_data['measurements']
        instance.bill = validated_data['bill']
        instance.delivery_date = validated_data['delivery_date']
        instance.save()
        return instance


class PostOrderSerializer(BaseOrderSerializer):
    pass


class PutOrderSerializer(BaseOrderSerializer):
    id = serializers.IntegerField()


class GetOrderSerializer(BaseOrderSerializer):
    id = serializers.IntegerField()
    serial_no = serializers.IntegerField()
    image_url = serializers.URLField()


class SearchOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    serial_no = serializers.IntegerField()
    customer_name = serializers.CharField()
    customer_mobile = serializers.IntegerField()


class ImageUploadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField(max_length=50)
    file_data = serializers.CharField()

    def create(self, validated_data):
        if validated_data['type'] == 'order':
            order = Order.objects.get(id=validated_data['id'])
            filename = "%d_%s.%s" % (order.id, uuid.uuid4(), "jpeg")
            image_url = ORDER_IMAGE_BASE_URL + filename
            imag_path = ORDER_IMAGE_LOCATION + filename
            order.image_url = image_url
            order.save()
            try:
                image_data = b64decode(validated_data['file_data'].split('base64,', 1)[1])
            except IndexError:
                image_data = b64decode(validated_data['file_data'])
            with open(imag_path, 'wb') as f:
                f.write(image_data)
            return image_url
