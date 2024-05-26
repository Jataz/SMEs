from .frontend import index,sme_list,size_of_business_data,sex_data
from .users import user_logout_view,UserLoginView
from .smes import SMEListView,ProvinceAPIView,DistrictAPIView,WardAPIView,\
    sme_create_record,get_districts,get_wards,SmeDetail,SMEUpdateView,update_sme_record