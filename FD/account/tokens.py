import jwt
import datetime
SECRET_JWT = "secretkey:(test)"

SECRET_PRE = "secretkey(test)"

def create_token(id):

    encoded = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300), 'id' : id}, SECRET_PRE, algorithm='HS256')
    return encoded

def validate_token(token):
    try:
        jwt.decode(token, SECRET_PRE, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    else:
        return True