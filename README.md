# FD_django

## API

### regist_user
회원가입
#### request
```http
POST /account/regist_user
```
| Name | Description |
| ---- | ----------- |
| `id` | id |
| `passwd` | 비밀번호 |
| `gender` | 성별 |
| `age` | 나이 |
| `height` | 키 |
| `weight` | 체중 |
| `reg_datetime` | 가입 날짜 |
| `gcode` | 목표코드 |
| `calorie` | 목표 칼로리 |
| `carbohydrate` | 목표 탄수화물 |
| `protein` | 목표 단백질 |
| `fat` | 목표 지방 |
| `sugar` | 목표 당 |
| `salt` | 목표 나트륨 |
| `saturated_fat` | 목표 포화지방 |
| `intf_type` | 간헐적단식 타입 |
#### response
| HTTP Status Code | Description |
| ---- | ----------- |
| `201` | 성공 |
| `400` | 실패 |

***
### app_login
로그인
#### request
```http
POST /account/app_login
```

| Name | Description |
| ---- | ----------- |
| `id` | user0001 |
| `passwd` | pwd0000 |

#### response
`
{'status_code' : 1, 'token' : '---token---', 'msg' : ["로그인 성공", "ID가 없습니다", "비밀번호가 틀렸습니다"] }
`

***
### profile_meal
해당 사용자가 올린 식단 이미지 리스트
#### request
```http
POST /account/profile_meal
```
| Name | Description |
| ---- | ----------- |
| `token` | JWT |
| `id` | 사용자 아이디(ex. user0001) |

#### response
`{'status_code': 1, 'img': 이미지 리스트}`

***
### community_meal
특정 목표코드를 가진 사용자가 올린 식단 이미지 리스트
#### request
```http
POST /account/community_meal
```
| Name | Description |
| ---- | ----------- |
| `token` | JWT |
| `gcode` | 목표코드(ex. 1231) |

#### response
`{'status_code': 1, 'img': 이미지 리스트}`

***
### detect
이미지명을 보내면, 해당 식단 이미지에 포함된 음식 정보(class, 좌표(x1,y1,x2,y2))를 반환
#### request
```http
POST /account/detect
```
| Name | Description |
| ---- | ----------- |
| `token` | JWT |
| `img_name` | 이미지 파일명(ex. user0001_0000001.jpg) |

#### response
`{'status_code': 1, 'result': array(class, 좌표)}`

***
### user_date_info
유저 아이디와 날짜를 보내면, 해당 날짜의 유저 식단 정보(칼로리/탄단지/사진명) & 유저의 목표 칼로리 탄단지 정보 반환
#### request
```http
POST /account/user_date_info
```
| Name | Description |
| ---- | ----------- |
| `id` | user id |
| `date` | 날짜(yyyy-mm-dd) |

#### response
```
{
    "infoList": [
        {
            "calories_total": 450.0,
            "carbo_total": 30.0,
            "fat_total": 10.0,
            "protein_total": 20.0,
            "image_name": "user0001_0000001.jpg"
        },
        ...
    ],
    "infoNum": (# of info),
    "user_calorie": 0.0,
    "user_carbo": -1.0,
    "user_fat": -1.0,
    "user_protein": -1.0
}

```