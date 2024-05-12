from rest_framework import serializers
from ..models import SME, CalculationScale, Province, District, SizeValue
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\d[\d\s.-]{9,14}$',
    message="Phone number must start with a digit and be 10 to 15 digits long, spaces, dashes, and periods allowed."
)

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'district_name']

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'province_name']

class SizeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeValue
        fields = ['id', 'size', 'value']

class CalculationScaleSerializer(serializers.ModelSerializer):
    size_of_employees = SizeValueSerializer()
    size_of_annual_revenue = SizeValueSerializer()
    size_of_asset_value = SizeValueSerializer()
    size_of_business = SizeValueSerializer()
    class Meta:
        model = CalculationScale
        fields = ('size_of_employees', 'size_of_annual_revenue', 'size_of_asset_value', 'rating', 'size_of_business')

class SMESerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex], max_length=20)
    province = ProvinceSerializer()
    district = DistrictSerializer()
    calculation_scale = CalculationScaleSerializer(many=True)

    class Meta:
        model = SME
        fields = ('company', 'contact_person', 'phone_number', 'email', 'address', 'sector', 'type_of_business', 
                  'product_service', 'province', 'district', 'number_of_employees', 
                  'asset_value', 'annual_revenue', 'calculation_scale')
        
    def validate_phone_number(self, value):
        """
        Perform custom validations on the phone number.
        This method can be used for additional checks if needed.
        """
        # Example: Ensure the phone number does not contain invalid characters
        if not value[0].isdigit():
            raise serializers.ValidationError("Phone number must start with a digit.")
        return value