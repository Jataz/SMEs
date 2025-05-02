from rest_framework import serializers
from ..models import SME, CalculationScale, Province, District, SizeValue,UserProfile, Ward,Sector,SectorThreshold
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


phone_regex = RegexValidator(
    regex=r'^\d[\d\s.-]{9,14}$',
    message="Phone number must start with a digit and be 10 to 15 digits long, spaces, dashes, and periods allowed."
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']  # Adjust as needed


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'province_name']
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'district_name']

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['id','district','ward_name']
class SizeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeValue
        fields = ['id', 'size', 'value']

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name']

class SectorThresholdSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    class Meta:
        model = SectorThreshold
        fields = ['id', 'sector', 'size', 'value']

class CalculationScaleSerializer(serializers.ModelSerializer):
    size_of_employees = SizeValueSerializer()
    size_of_annual_revenue = SizeValueSerializer()
    size_of_asset_value = SizeValueSerializer()
    size_of_business = SizeValueSerializer()
    class Meta:
        model = CalculationScale
        fields = ('size_of_employees', 'size_of_annual_revenue', 'size_of_asset_value', 'rating', 'size_of_business')
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    ward = WardSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'province', 'district', 'ward', 'is_ward_level', 'is_district_level', 'is_province_level', 'is_national_level']
class SMESerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex], max_length=20)
    province = ProvinceSerializer()
    district = DistrictSerializer()
    ward = WardSerializer()
    sector = SectorSerializer()
    calculation_scale = CalculationScaleSerializer(many=True)
    user_profile = UserProfileSerializer(read_only=True) 

    class Meta:
        model = SME
        fields = ('id', 'sme_ref_number', 'company', 'type_of_business', 'registration', 'sector', 
             'product_service', 'number_of_employees', 'export', 'ownership', 'contact_person', 
             'address', 'phone_number', 'email', 'education', 'support_service', 'training_received', 
             'funding_received', 'compliance', 'tax', 'source_of_funds', 'annual_revenue', 
             'asset_value', 'comments', 'province', 'district', 'ward', 'calculation_scale', 
             'user_profile')
        
    def validate_phone_number(self, value):
        """
        Perform custom validations on the phone number.
        This method can be used for additional checks if needed.
        """
        # Example: Ensure the phone number does not contain invalid characters
        if not value[0].isdigit():
            raise serializers.ValidationError("Phone number must start with a digit.")
        return value