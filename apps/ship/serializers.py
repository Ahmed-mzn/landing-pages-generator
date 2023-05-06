from rest_framework import serializers
from .models import Channel, ChannelField, ConstantChannel, ConstantChannelField, Order, OrderItem, Coupon, Warehouse

from apps.main.models import Lead, Product, App, Affiliate
from apps.main.serializers import LeadSerializer, ProductSerializer


class ChannelFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelField
        fields = ('id', 'key', 'value', 'created_at', 'updated_at')


class ChannelSerializer(serializers.ModelSerializer):
    fields = ChannelFieldSerializer(many=True)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'type', 'is_active', 'created_at', 'fields', 'updated_at')

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            exist = Channel.objects.filter(app__user=self.context['request'].user, type=attrs['type']).exists()
            if exist:
                raise serializers.ValidationError(detail="Channel already exist")
        return attrs

    def create(self, validated_data):
        app = self.context['request'].user.apps.first()
        fields = validated_data.pop('fields')

        channel = Channel.objects.create(**validated_data, app=app)
        for field in fields:
            ChannelField.objects.create(channel=channel, **field)

        return channel

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PATCH':
            return super().update(instance, validated_data)
        fields = validated_data.pop('fields')

        # update fields only
        for field in fields:
            try:
                field_obj = instance.fields.get(key=field['key'])
                field_obj.value = field['value']
                field_obj.save()
            except:
                print('error when update field : ' + field['key'])
        return instance


class ConstantChannelFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstantChannelField
        fields = ('id', 'key', 'value', 'created_at', 'updated_at')


class ConstantChannelSerializer(serializers.ModelSerializer):
    constant_fields = ConstantChannelFieldSerializer(many=True)

    class Meta:
        model = ConstantChannel
        fields = ('id', 'name', 'type', 'image_url', 'constant_fields', 'created_at', 'updated_at')


class ChannelViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'type')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'amount', 'created_at', 'updated_at')
        extra_kwargs = {
            'amount': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    lead = LeadSerializer(many=False)
    items = OrderItemSerializer(many=True, read_only=True)
    input_items = serializers.ListField(write_only=True)
    shipping_company = ChannelViewSerializer(many=False, required=False)

    class Meta:
        model = Order
        fields = ('id', 'lead', 'template', 'items', 'coupon', 'is_paid', 'shipping_company', 'status', 'input_items',
                  'shipping_company', 'shipping_tracking_id', 'shipping_awb', 'amount', 'created_at', 'updated_at')
        extra_kwargs = {
            'is_paid': {'read_only': True},
            'shipping_company': {'read_only': True},
            'shipping_tracking_id': {'read_only': True},
            'shipping_awb': {'read_only': True},
            'amount': {'read_only': True},
        }

    def validate_input_items(self, value):
        for item in value:
            try:
                Product.objects.get(pk=item["id"])
            except:
                raise serializers.ValidationError(detail="Item not found")
        return value

    def create(self, validated_data):
        print(validated_data)
        input_lead = validated_data.pop("lead")
        items = validated_data.pop("input_items")
        template = validated_data.pop("template")
        print(items)
        try:
            lead = Lead.objects.all().get(phone_number=input_lead.get('phone_number'),
                                          name=input_lead.get('name'), address=input_lead.get('address'),
                                          city=input_lead.get('city'))
        except:
            lead = Lead.objects.create(name=input_lead.get('name'), phone_number=input_lead.get('phone_number'),
                                       city=input_lead.get('city'), address=input_lead.get('address'))

        ship = Channel.objects.filter(app=template.app).first()
        order = Order.objects.create(lead=lead, template=template, shipping_company=ship, amount=0)

        total_amount = 0

        for item in items:
            product = Product.objects.get(pk=item["id"])
            if product.price_after_discount:
                amount = product.price_after_discount * int(item["quantity"])
            else:
                amount = product.price * int(item["quantity"])
            total_amount += amount
            OrderItem.objects.create(product=product, order=order, quantity=item["quantity"], amount=amount)

        order.amount = total_amount
        order.save()

        return order


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'code', 'type', 'percentage', 'amount', 'active', 'num_available', 'num_used',
                  'created_at', 'updated_at')

    def create(self, validated_data):
        app = App.objects.filter(user=self.context['request'].user).first()

        coupon = Coupon.objects.create(app=app, **validated_data)

        return coupon


class AffiliateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliate
        fields = ('id', 'affiliate_identifier', 'affiliate_secret', 'email', 'phone_number', 'full_name',
                  'created_at', 'updated_at')
        extra_kwargs = {
            'affiliate_identifier': {'read_only': True},
            'affiliate_secret': {'read_only': True},
        }

    def create(self, validated_data):
        app = App.objects.filter(user=self.context['request'].user).first()

        affiliate = Affiliate.objects.create(app=app, **validated_data)

        return affiliate


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('id', 'title', 'city', 'email', 'name', 'phone_number', 'address','is_current',
                  'created_at', 'updated_at')

    def create(self, validated_data):
        app = App.objects.filter(user=self.context['request'].user).first()

        count_warehouses = Warehouse.objects.filter(app=app).count()

        warehouse = Warehouse.objects.create(app=app, **validated_data)

        if count_warehouses == 0:
            warehouse.is_current = True
            warehouse.save()

        return warehouse