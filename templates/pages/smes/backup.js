$.ajax({
    url: '/api/v1/provinces/',
    dataType: 'json',
    success: function(provinceData) {
        var provinceDropdown = modal.find('#province-dropdown');
        provinceDropdown.empty(); // Clear existing options
        $.each(provinceData.provinces, function(index, province) {
            provinceDropdown.append('<option value="' + province.id + '">' + province.province_name + '</option>');
        });

        // Select the province in the dropdown
        provinceDropdown.val(data.province.id);

        // Trigger change event manually to populate district and ward dropdowns
        provinceDropdown.change();
    },
    error: function(error) {
        console.error('Error fetching provinces:', error);
    }
});

// Handle change event for provinces dropdown
modal.find('#province-dropdown').change(function() {
    var selectedProvinceId = $(this).val();
    var districtDropdown = modal.find('#district-dropdown');
    var wardDropdown = modal.find('#ward-dropdown');

    // Clear existing options
    districtDropdown.empty();
    wardDropdown.empty();
    wardDropdown.append('<option value="" selected disabled>Select Ward</option>');

    if (selectedProvinceId) {
        // Fetch districts for the selected province
        $.ajax({
            url: `/api/v1/districts/?province_id=${selectedProvinceId}`,
            dataType: 'json',
            success: function(districtData) {
                // Append districts to the dropdown
                districtDropdown.append('<option value="" selected disabled>Select District</option>');
                $.each(districtData.districts, function(index, district) {
                    districtDropdown.append(`<option value="${district.id}">${district.district_name}</option>`);
                });

                // Select the district in the dropdown
                districtDropdown.val(data.district.id);

                // Trigger change event manually to populate ward dropdown
                districtDropdown.change();
            },
            error: function(error) {
                console.error('Error fetching districts:', error);
            }
        });
    }
});

// Populate ward dropdown based on selected district
modal.find('#district-dropdown').change(function() {
    var selectedDistrictId = $(this).val();
    var wardDropdown = modal.find('#ward-dropdown');

    // Clear existing options
    wardDropdown.empty();
    wardDropdown.append('<option value="" selected disabled>Select Ward</option>');

    if (selectedDistrictId) {
        // Fetch wards for the selected district
        $.ajax({
            url: `/api/v1/wards/?district_id=${selectedDistrictId}`,
            dataType: 'json',
            success: function(wardData) {
                // Append wards to the dropdown
                $.each(wardData.wards, function(index, ward) {
                    wardDropdown.append(`<option value="${ward.id}">${ward.ward_name}</option>`);
                });

                // Select the ward in the dropdown
                wardDropdown.val(data.ward.id);
            },
            error: function(error) {
                console.error('Error fetching wards:', error);
            }
        });
    }
});