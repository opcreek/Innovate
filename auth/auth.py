import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-fsnd-15.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'innovateProject'
INT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE5ZjFlMzZiNjliYzBjMTJlM2JhMTkiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODkxNTIyNDYsImV4cCI6MTU4OTIzODY0NiwiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.01Pfq9KENRpMCmOzJ8YhOI0PBJVf3imDhk3lHeo2PqlN7ZjLPX_B0oDHHjPv89bwrYKXRcCjJDAt6ljHr4vlb9JB6-f8RyMVz-7VqMv101IXXuy8WZJie7eAqw42Ev7gkbpm4aQ2GtDgnL1Kn0dm5mOt0_2DTFZIRobB7edZmQZnI1PU3nLH0_0Rs6Rjrb9DM_4d96LkVFlAmg4Emft7rNgG59B9H7g-OcVsE76FCXBDMAaNTSQTIMXZvmaXXE0NEVdc6rRQsxoQ1foX0vcwEXJ-XjUcrAgjmHIXgMhbcdRJXpHTzCe22l5WgJcezsTCV6QGH_3izDrAFbfD2KFuxw'
EMP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFhMDczNzFjYzFhYzBjMTQ3NDcwNzUiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODkxNTI0MTMsImV4cCI6MTU4OTIzODgxMywiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwcm9qZWN0LWRldGFpbCIsInBhdGNoOnByb2plY3QiLCJwb3N0OnByb2plY3QiXX0.ygh54YtbLGMeCD8oYY0e9iO6QeR4kTIxFi32TvPWnucfeNuVJu7qZAwbFCPb9Aqlv2PN5FJR_N4xGe5Iq_lLiLSrTLgwVypMURo_DX4vPhGQnsb3S0tT91H97DnDAtudRj_oBAJxzara6BmrHvAQr9s86VPQV0N8Caz9ltfuOhAT4cIFgDYf6eotkky4yttCG2F1LlKRILVFd2ji_-nktj233SXC_udI4c3ClNR79u2CMGa3ZjvRm2UL7wghtjnFFm-vcShEVoGY0aVhMGVyFbV31OEEiYykC-SLY6fz4AOedWtemRl0LXXTdILlwwXxaG21L6HBEh7Wxbfs2selXQ'
SUP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlRUW1kakVaa29kWjhRVV9zSnN2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1mc25kLTE1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFhMDg5YjFjYzFhYzBjMTQ3NDc0NTQiLCJhdWQiOiJpbm5vdmF0ZVByb2plY3QiLCJpYXQiOjE1ODkxNTI1ODAsImV4cCI6MTU4OTIzODk4MCwiYXpwIjoiNlZ4QUNHc2FsMVFMcEFtaFY2aHdZRmtqZWo4MVVRVjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwcm9qZWN0IiwiZGVsZXRlOnRlYW0tbWVtYmVyIiwiZ2V0OnByb2plY3QtZGV0YWlsIiwiZ2V0OnRlYW0tbWVtYmVycyIsInBhdGNoOnByb2plY3QiLCJwYXRjaDp0ZWFtLW1lbWJlciIsInBvc3Q6cHJvamVjdCJdfQ.J0znV2R-tY3-mT92YrFaO2ZAbk12IZ7zTiHoVZm_3xDgWJthNMJvdDUWwqzjz8ME2pokKRkpCfNdMdG9LmdIkxJcYlFt1L4mr5F74xkEK8xG1rChF4NEKUOeIXgRLOm8aspDbny2T2JUtL7oAJBVRRLE7OryZ9XPTnkqKz--MgidRCY0E_19ISrzJe964yrA3laYTmA_tp7b0FhyCICgj4oD_Z5xlEr-GJ7cNHNmLvnhoim_qHyVrvdxMLGQsX9tIx9sSz-y9jZOp_OREsXftW6t4lta3h3yjyA0gpLRRFexDPRYBrVnMI24jLHLO12-ul0cIEd58iegRmFCRmXJfQ'


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
