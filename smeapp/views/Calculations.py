from ..models import SME, CalculationScale, SizeValue, SectorThreshold
import logging

# Initialize a logger for debugging
logger = logging.getLogger(__name__)

def determine_size_of_employees(number_of_employees, sector):
    """Determine the size of employees based on the sector-specific thresholds."""
    thresholds = SectorThreshold.objects.filter(sector=sector).select_related('size')

    if not thresholds.exists():
        logger.error(f"No thresholds defined for sector: {sector}")
        raise ValueError(f"No thresholds defined for sector: {sector}")

    try:
        # Use ordered thresholds to determine the size
        for threshold in thresholds.order_by('max_employees'):
            if number_of_employees <= threshold.max_employees:
                return threshold.size  # Return the linked SizeValue object
        return SizeValue.objects.get(size='LARGE')  # Default to 'LARGE' if no match
    except SizeValue.DoesNotExist as e:
        logger.error(f"SizeValue not configured properly: {e}")
        raise ValueError(f"Thresholds not configured properly for sector: {sector}") from e


def determine_size_of_annual_revenue(annual_revenue, sector):
    """Determine the size of annual revenue based on the sector-specific thresholds."""
    thresholds = SectorThreshold.objects.filter(sector=sector).select_related('size')

    if not thresholds.exists():
        logger.error(f"No thresholds defined for sector: {sector}")
        raise ValueError(f"No thresholds defined for sector: {sector}")

    try:
        for threshold in thresholds.order_by('max_annual_revenue'):
            if annual_revenue <= threshold.max_annual_revenue:
                return threshold.size
        return SizeValue.objects.get(size='LARGE')
    except SizeValue.DoesNotExist as e:
        logger.error(f"SizeValue not configured properly: {e}")
        raise ValueError(f"Thresholds not configured properly for sector: {sector}") from e


def determine_size_of_asset_value(asset_value, sector):
    """Determine the size of asset value based on the sector-specific thresholds."""
    thresholds = SectorThreshold.objects.filter(sector=sector).select_related('size')

    if not thresholds.exists():
        logger.error(f"No thresholds defined for sector: {sector}")
        raise ValueError(f"No thresholds defined for sector: {sector}")

    try:
        for threshold in thresholds.order_by('max_asset_value'):
            if asset_value <= threshold.max_asset_value:
                return threshold.size
        return SizeValue.objects.get(size='LARGE')
    except SizeValue.DoesNotExist as e:
        logger.error(f"SizeValue not configured properly: {e}")
        raise ValueError(f"Thresholds not configured properly for sector: {sector}") from e


def calculate_rating(size_of_employees, size_of_annual_revenue, size_of_asset_value):
    """Calculate the rating based on the size of employees, annual revenue, and asset value."""
    try:
        rating = size_of_employees.value + size_of_annual_revenue.value + size_of_asset_value.value
        logger.info(f"Calculated rating: {rating}")
        return rating
    except Exception as e:
        logger.error(f"Error calculating rating: {e}")
        raise


def determine_business_size(rating):
    """Determine the size of the business based on the rating."""
    try:
        if rating < 4:
            return SizeValue.objects.get(size='MICRO')
        elif rating < 8:
            return SizeValue.objects.get(size='SMALL')
        elif rating < 10:
            return SizeValue.objects.get(size='MEDIUM')
        else:
            return SizeValue.objects.get(size='LARGE')
    except SizeValue.DoesNotExist as e:
        logger.error(f"Error determining business size: {e}")
        raise


def create_calculation_scale(sme, size_of_employees, size_of_annual_revenue, size_of_asset_value, rating, size_of_business):
    """Create a CalculationScale record."""
    try:
        scale = CalculationScale.objects.create(
            sme=sme,
            size_of_employees=size_of_employees,
            size_of_annual_revenue=size_of_annual_revenue,
            size_of_asset_value=size_of_asset_value,
            rating=rating,
            size_of_business=size_of_business
        )
        logger.info(f"CalculationScale created for SME: {sme}")
        return scale
    except Exception as e:
        logger.error(f"Error creating CalculationScale: {e}")
        raise

    

def update_sme_record_in_database(sme_id, company, contact_person, phone_number, email, address, sector,
                                  type_of_business, product_service,number_of_employees, asset_value, annual_revenue,
                                  export,comments,ownership, support_service, training_received, funding_received,
                                  source_of_funds,compliance, registration, tax, education):
    # Assuming you have a model for SME records and CalculationScale records
    sme = SME.objects.get(id=sme_id)
    sme.company = company
    sme.type_of_business = type_of_business
    sme.registration = registration
    sme.sector = sector
    sme.product_service = product_service
    sme.number_of_employees = number_of_employees
    sme.export = export
    sme.ownership = ownership
    sme.contact_person = contact_person
    sme.address = address
    sme.phone_number = phone_number
    sme.email = email
    sme.education = education
    sme.support_service = support_service
    sme.training_received = training_received
    sme.funding_received = funding_received
    sme.compliance = compliance
    sme.tax = tax
    sme.source_of_funds = source_of_funds
    sme.annual_revenue = annual_revenue
    sme.asset_value = asset_value
    sme.comments = comments
    sme.save()
    
    return sme

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

