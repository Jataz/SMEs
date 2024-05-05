from rest_framework import serializers
from ..models import SME, Province, District, SizeValue
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

class SMESerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex], max_length=20)
    province = ProvinceSerializer()
    district = DistrictSerializer()
    size_of_business = SizeValueSerializer()

    class Meta:
        model = SME
        fields = '__all__'
        
    def validate_phone_number(self, value):
        """
        Perform custom validations on the phone number.
        This method can be used for additional checks if needed.
        """
        # Example: Ensure the phone number does not contain invalid characters
        if not value[0].isdigit():
            raise serializers.ValidationError("Phone number must start with a digit.")
        return value