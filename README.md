#FD_django
================
## API
### regist_user
POST http://127.0.0.1:8000/account/regist_user

example in body :

{
    "id": "testuser",
    "passwd": "testuser",
    "gender": 1,
    "age": 1,
    "height": 1,
    "weight": 1,
    "reg_datetime": "2021-01-01 04:20:11",
    "gcode": 0,
    "calorie": 1,
    "carbohydrate": 0,
    "protein": 0,
    "fat": 0,
    "sugar": 0,
    "salt": 0,
    "saturated_fat": 0,
    "intf_type": 0
}

### app_login

POST http://127.0.0.1:8000/account/app_login

example in body : 

{
    "id" : "testuser",
    "passwd" : "testuser",
...
}
