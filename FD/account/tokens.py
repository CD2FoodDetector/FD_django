import jwt
import datetime

SECRET_PRE = "secretkey(test)"

def create_token(id):

    encoded = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), 'id' : id}, SECRET_PRE, algorithm='HS256')
    return encoded

def create_refresh(id):
    encoded = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7), 'id': id}, SECRET_PRE,
                         algorithm='HS256')
    return encoded

def check_refresh(token, id):
    try:
        jwt.decode(token, SECRET_PRE, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return "expiredSignature"
    except jwt.InvalidTokenError:
        return "invalid"
    else:
        return create_token(id)

def validate_token(token):
    try:
        jwt.decode(token, SECRET_PRE, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return "expiredSignature"
    except jwt.InvalidTokenError:
        return "invalid"
    else:
        return True