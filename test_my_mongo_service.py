def test_validate_input_post():

    from my_mongo_service import validate_input_post

    input1 = {"user_email": "user1@email.com",
              "user_age": 20,
              "heart_rate": 77}
    user_email1, user_age1, heart_rate1 = validate_input_post(input1)

    assert(user_email1 == "user1@email.com")
    assert(user_age1 == 20)
    assert(heart_rate1 == 77)

    input2 = {"email": "user2@email.com",
              "age": 21,
              "heart_rate": 1000}
    user_email2, user_age2, heart_rate2 = validate_input_post(input2)

    assert(user_email2 is None)
    assert(user_age2 is None)
    assert(heart_rate2 is None)

def test_validate_interval_average():

    from datetime import datetime
    from my_mongo_service import validate_input_interval_average

    input1 = {"user_email": "user1@email.com",
              "heart_rate_average_since": "2018-01-01 07:07:07.000007"}
    user_email1, time_since1, time_formatted1 = validate_input_interval_average(input1)

    assert(user_email1 == "user1@email.com")
    assert(time_since1 == "2018-01-01 07:07:07.000007")
    assert(time_formatted1 == datetime.strptime(time_since1, "%Y-%m-%d %H:%M:%S.%f"))

    input2 = {"email": "user2@email.com",
              "average_since": "2018-01-01 07:07:07.000007"}
    user_email2, time_since2, time_formatted2 = validate_input_interval_average(input2)

    assert(user_email2 is None)
    assert(time_since2 is None)
    assert(time_formatted2 is None)

    input3 = {"user_email": "user3@email.com",
              "heart_rate_average_since": "18-31-01 07:07:07.000007"}
    user_email3, time_since3, time_formatted3 = validate_input_interval_average(input3)

    assert(user_email3 is None)
    assert(time_since3 is None)
    assert(time_formatted3 is None)

def test_check_tachycardia():

    from my_mongo_service import check_tachycardia

    t1 = check_tachycardia(1, 150)
    t2 = check_tachycardia(2, 152)
    assert(t1 == False)
    assert(t2 == True)

    t3 = check_tachycardia(3, 136)
    t4 = check_tachycardia(4, 138)
    assert(t3 == False)
    assert(t4 == True)

    t5 = check_tachycardia(5, 133)
    t6 = check_tachycardia(7, 135)
    assert(t5 == False)
    assert(t6 == True)

    t7 = check_tachycardia(9, 130)
    t8 = check_tachycardia(11, 132)
    assert(t7 == False)
    assert(t8 == True)

    t9 = check_tachycardia(13, 118)
    t10 = check_tachycardia(15, 120)
    assert(t9 == False)
    assert(t10 == True)

    t11 = check_tachycardia(25, 0)
    t12 = check_tachycardia(70, 1000)
    assert(t11 == False)
    assert(t12 == True)
