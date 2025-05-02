document.addEventListener('DOMContentLoaded', function() {
    const provinceSelect = document.getElementById('id_province');
    const districtSelect = document.getElementById('id_district');
    const wardSelect = document.getElementById('id_ward');

    provinceSelect.addEventListener('change', function() {
        const provinceId = provinceSelect.value;
        districtSelect.innerHTML = '<option value="">Select a district</option>';
        wardSelect.innerHTML = '<option value="">Select a ward</option>';
        
        if (provinceId) {
            fetch(`/api/v1/admin/get_districts/${provinceId}/`)
                .then(response => response.json())
                .then(data => {
                    data.districts.forEach(district => {
                        const option = new Option(district.district_name, district.id);
                        districtSelect.add(option);
                    });
                })
                .catch(error => console.error('Error fetching districts:', error));
        }
    });

    districtSelect.addEventListener('change', function() {
        const districtId = districtSelect.value;
        wardSelect.innerHTML = '<option value="">Select a ward</option>';
        
        if (districtId) {
            fetch(`/api/v1/admin/get_wards/${districtId}/`)
                .then(response => response.json())
                .then(data => {
                    data.wards.forEach(ward => {
                        const option = new Option(ward.ward_name, ward.id);
                        wardSelect.add(option);
                    });
                })
                .catch(error => console.error('Error fetching wards:', error));
        }
    });
});
