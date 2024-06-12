
from ..models import SME, CalculationScale, SizeValue


def determine_size_of_employees(number_of_employees):
    """Determine the size of employees based on the number of employees."""
    if number_of_employees <= 5:
        return SizeValue.objects.get(size='MICRO')
    elif 5 <= number_of_employees <= 40:
        return SizeValue.objects.get(size='SMALL')
    elif 41 <= number_of_employees <= 75:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def determine_size_of_annual_revenue(annual_revenue):
    """Determine the size of annual revenue based on the annual revenue."""
    if annual_revenue <= 30000:
        return SizeValue.objects.get(size='MICRO')
    elif annual_revenue <= 500000:
        return SizeValue.objects.get(size='SMALL')
    elif annual_revenue <= 1000000:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def determine_size_of_asset_value(asset_value):
    """Determine the size of asset value based on the asset value."""
    if asset_value <= 10000:
        return SizeValue.objects.get(size='MICRO')
    elif asset_value <= 500000:
        return SizeValue.objects.get(size='SMALL')
    elif asset_value <= 1000000:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def calculate_rating(size_of_employees, size_of_annual_revenue, size_of_asset_value):
    """Calculate the rating based on the size of employees, annual revenue, and asset value."""
    return size_of_employees.value + size_of_annual_revenue.value + size_of_asset_value.value


def determine_business_size(rating):
    """Determine the size of the business based on the rating."""
    if rating < 4:
        return SizeValue.objects.get(size='MICRO')
    elif rating < 8:
        return SizeValue.objects.get(size='SMALL')
    elif rating < 10:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def create_calculation_scale(sme, size_of_employees, size_of_annual_revenue, size_of_asset_value,
                             rating, size_of_business):
    """Create a CalculationScale record."""
    CalculationScale.objects.create(
        sme=sme,
        size_of_employees=size_of_employees,
        size_of_annual_revenue=size_of_annual_revenue,
        size_of_asset_value=size_of_asset_value,
        rating=rating,
        size_of_business=size_of_business
    )
    

def update_sme_record_in_database(sme_id, company, contact_person, phone_number, email, address, sector,
                                  type_of_business, product_service,number_of_employees, asset_value, annual_revenue, age, sex,export,comments,disability):
    # Assuming you have a model for SME records and CalculationScale records
    sme = SME.objects.get(id=sme_id)
    sme.company = company
    sme.contact_person = contact_person
    sme.phone_number = phone_number
    sme.email = email
    sme.address = address
    sme.sector = sector
    sme.type_of_business = type_of_business
    sme.product_service = product_service
    #sme.province_id = province_id
    #sme.district_id = district_id
    #sme.ward_id = ward_id
    sme.number_of_employees = number_of_employees
    sme.asset_value = asset_value
    sme.annual_revenue = annual_revenue
    sme.age = age
    sme.sex = sex
    sme.export = export
    sme.comments = comments
    sme.disability = disability
    sme.save()


def update_calculation_scale(sme_id, size_of_employees, size_of_annual_revenue, size_of_asset_value,
                             rating, size_of_business):
    # Assuming you have a model for CalculationScale records
    calculation_scale = CalculationScale.objects.get(sme=sme_id)
    calculation_scale.size_of_employees = size_of_employees
    calculation_scale.size_of_annual_revenue = size_of_annual_revenue
    calculation_scale.size_of_asset_value = size_of_asset_value
    calculation_scale.rating = rating
    calculation_scale.size_of_business = size_of_business
    calculation_scale.save()

