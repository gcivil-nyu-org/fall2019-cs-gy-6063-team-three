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
        ",graduation_rate"
    )
    LOCAL_PROGRAM_FIELD_LIST = (
        "dbn, code1, code2, code3, code4, code5, code6, code7, code8, code9, code10,"
        "seats9ge1, seats9ge2, seats9ge3, seats9ge4, seats9ge5, seats9ge6, seats9ge7, "
        "seats9ge8, seats9ge9,seats9ge10,program1, program2,program3, program4, "
        "program5, program6, program7, program8, program9,program10, prgdesc1, "
        "prgdesc2, prgdesc3, prgdesc4, prgdesc5, prgdesc6,prgdesc7, prgdesc8, "
        "prgdesc9, prgdesc10, offer_rate1, offer_rate2, offer_rate3, offer_rate4, "
        "offer_rate5, offer_rate6,offer_rate7, offer_rate8, offer_rate9, offer_rate10 "
    )
