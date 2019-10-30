class UserType:
    STUDENT = "ut_student"
    ADMIN_STAFF = "ut_admin_staff"
    TEACHER = "ut_teacher"


class ApiInfo:
    API_DOMAIN = "data.cityofnewyork.us"
    API_RESOURCE = "uq7m-95z8"
    APP_TOKEN = "NAGEBEKXZypPeTj4F7DXuGRh1"
    LOCAL_FIELD_LIST = (
        "dbn, school_name,boro,overview_paragraph,neighborhood,location,"
        "phone_number,school_email,website,total_students,start_time,end_time"
        ",graduation_rate "
    )
