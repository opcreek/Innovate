import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-fsnd-15.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'innovateProject'
INT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE5ZjFlMzZiNjliYzBjMTJlM2JhMTkiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODkxMTE1NzMsImV4cCI6MTU4OTE5Nzk3MywiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.Dx8Yfq7HtYhfqiEKmQnTdjRuwmJQUx6HZX9FBcaA5oEl5W2S4SIcsTo7o0fvDunTgW-ToghmSUUEon4U0lcJM1JsRBA300Frh_5tg16zr4Nine_rb7bHkX6wO9jeuVIeY9f8Nb5wjQZf2ETMbabBV8MB10U-UK8EXv8k4sKYP0kA_PnHZp8CsgiGiUlZK05ptcDW2JidcQzbAFPKBQVKbDSkkIiG4iBAOBq-RUoMhMneXfVRbtu2iwe8zQGl-OKeJ_DtwGH8CyU1qTmCc8gFrTUz3RCPHVccjfV7m3FzRbFA64sGFcBZ_mUMaEh7n9UlSqE-EgbXLE4Dc2gXeozzRA'
EMP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFhMDczNzFjYzFhYzBjMTQ3NDcwNzUiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODg4OTE2NTQsImV4cCI6MTU4ODk3ODA1NCwiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwcm9qZWN0LWRldGFpbCIsInBhdGNoOnByb2plY3QiLCJwb3N0OnByb2plY3QiXX0.BsAg_NH_LBVN8JyyvLboU7BU1UK5luc6M3S5-a7MuGAKwQqoI8uAWefT4nbsQ0zqZVWNQuDvllus13nXsVr5cKwc_yg16Dqt6o5hoSAT8EaovX4Eqa_m5asAssQ2_xUK6HJWJm1gBVJRrNsgg0MDB_XOgXVptXwvoSU9xpiSTM9RHtjkRM8TZGE9Ph9FGEV1WhLjLReU_BfzPurgbFdeqhWyVQxFHmzVjyusy1vLH8bfUtsP5FJ1KNhxfWmZIQQAmVEByb1GjTd4vzvq3V9QfXHRK8eEz8_c8tbZXWl67SP6HVv1fLZsQMY33Wr9taL8g8pxfTKyZzP_0cahgzlQqg'
SUP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFhMDg5YjFjYzFhYzBjMTQ3NDc0NTQiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODkwODEwNTcsImV4cCI6MTU4OTE2NzQ1NywiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwcm9qZWN0IiwiZGVsZXRlOnRlYW0tbWVtYmVyIiwiZ2V0OnByb2plY3QtZGV0YWlsIiwiZ2V0OnRlYW0tbWVtYmVycyIsInBhdGNoOnByb2plY3QiLCJwYXRjaDp0ZWFtLW1lbWJlciIsInBvc3Q6cHJvamVjdCJdfQ.3guYoRjyjRVgn4tlzafS8vZvIgZ1WLdY_8pq5E0A30C6CXRV26y8blWUpEdXZM71KxDUK97bQcu9B_cV5-e6E3IgFK-RpB2pb-vj69KjYdGUFVU39hipbZiuriD3f3iTXxyEQEbRrGnGO56jo5fq5pNWO3x3hJx_am0qrP8HomF6QFXtXXV77C5lIQnPFkbjyAa9_OFfGjXLik-6GPaUAjDbitxx_eR7hTplDmXDPEDohuSt157Rd2R5zHF5sr0cec9K_GsU4kS027qApt_gWBuqwguev2ZWZZQP2Jz5u1-WloAntDQt-Tc7rY68CdlDg5PAP0fklLQPLAwU_wlplw'


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
