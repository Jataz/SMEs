from rest_framework import serializers
from ..models import SME

class SMESerializer(serializers.ModelSerializer):
    class Meta:
        model = SME
        fields = (
            'company', 'province', 'district', 'contact_person',
            'phone_number', 'address', 'sector', 'type_of_business',
            'product_service', 'annual_revenue', 'number_of_employees',
            'asset_value', 'size_of_busines'
        )
