import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-fsnd-15.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'innovateProject'
INT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE5ZjFlMzZiNjliYzBjMTJlM2JhMTkiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODg5NzcxNTcsImV4cCI6MTU4OTA2MzU1NywiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.Y7j3_h_hDaBhJZqXTuPpBZppCK0cs6kNG6H1h9qMXbmdXhH-tUPoTUOqkQPOpT2NMgd-XuNkHae2x1boo3dJoK6WSV-ZwX_R4tFhay50bhAjbJ4VrloJOMVvJZYgNfqJuYDjRVt1tmGxiNGXvq8mFro7arWyNHpa3NttnCMBxgGmd6kdhKolZUB7SzGCZr9lxO_dietIcLqTJz6KTfy0WbT1gm5Z6SrcrjJSjwWfkqMldS60n73EIuqSaW090t3XUxjLZtvOkIU8HN1Exstl0fgVFuo-1VRjQp3bPMyPisZIra_r373wmbsl0o_SSkOyo1keWfMJ8A8ohFjArnckcw'
EMP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFhMDczNzFjYzFhYzBjMTQ3NDcwNzUiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODg4OTE2NTQsImV4cCI6MTU4ODk3ODA1NCwiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwcm9qZWN0LWRldGFpbCIsInBhdGNoOnByb2plY3QiLCJwb3N0OnByb2plY3QiXX0.BsAg_NH_LBVN8JyyvLboU7BU1UK5luc6M3S5-a7MuGAKwQqoI8uAWefT4nbsQ0zqZVWNQuDvllus13nXsVr5cKwc_yg16Dqt6o5hoSAT8EaovX4Eqa_m5asAssQ2_xUK6HJWJm1gBVJRrNsgg0MDB_XOgXVptXwvoSU9xpiSTM9RHtjkRM8TZGE9Ph9FGEV1WhLjLReU_BfzPurgbFdeqhWyVQxFHmzVjyusy1vLH8bfUtsP5FJ1KNhxfWmZIQQAmVEByb1GjTd4vzvq3V9QfXHRK8eEz8_c8tbZXWl67SP6HVv1fLZsQMY33Wr9taL8g8pxfTKyZzP_0cahgzlQqg'
SUP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFhMDg5YjFjYzFhYzBjMTQ3NDc0NTQiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODg5NzcyNTcsImV4cCI6MTU4OTA2MzY1NywiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwcm9qZWN0IiwiZGVsZXRlOnRlYW0tbWVtYmVyIiwiZ2V0OnByb2plY3QtZGV0YWlsIiwiZ2V0OnRlYW0tbWVtYmVycyIsInBhdGNoOnByb2plY3QiLCJwYXRjaDp0ZWFtLW1lbWJlciIsInBvc3Q6cHJvamVjdCJdfQ.rcKIyUC2DR-57-4fviNV90JUChIOHb7Ad-u2CxnweGd52nhjGhjAtObGQWFPuywgOM8SHPw8ebxz5ILFIvCVXRz_C3XpcWK38ofTSutIQlJGQtMjuj9Gc8CHcy5_3jlt9eFNh-6tRgzVecsVjsWwkYSFMhnV2HY5BwiKNosP1z8Cql5ozp6QO5H4v3InXEIN9W_9mO3hmYahVSCIAD4T-Hzcbt5TUjhtYqBKs380bG5dwNpoh61pBmPEx8OJqk2_LaH7cgAmE8KspEgT_0y9ZrpJrO07lAyeXunaNiBSJ0lS6EUca3zBZG2dijmPq6m-6VstlC-wmc96rQND-KaOfQ'


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

# retrieve header from request
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

# implement check permission method


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permission not included in JWT'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'
        }, 403)
        # abort(403)
    return True


# verify decode JWT token
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please check the audience \
                and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)

# requires authorization decorator


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
