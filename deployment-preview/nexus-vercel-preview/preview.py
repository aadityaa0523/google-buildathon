"""Protected, disposable preview. Never use for durable marketplace data."""
import base64
import hmac
import hashlib
import os
import secrets

from starlette.responses import JSONResponse, Response

# This snapshot intentionally makes no paid model calls.
os.environ.pop('GEMINI_API_KEY', None)
# Privileged API routes receive a fresh private key, never shipped to the UI.
os.environ['NEXUS_OPERATOR_KEY'] = secrets.token_urlsafe(32)

from app.main import app

from preview_config import PASSWORD_SHA256
COOKIE_ACCESS = secrets.token_urlsafe(32)


@app.middleware('http')
async def protect_preview(request, call_next):
    password = os.environ.get('NEXUS_PREVIEW_PASSWORD', '')
    if not password and not PASSWORD_SHA256:
        return JSONResponse({'detail': 'Preview password has not been configured.'}, status_code=503)
    auth = request.headers.get('authorization', '')
    authenticated = False
    if auth.startswith('Basic '):
        try:
            username, supplied_password = base64.b64decode(auth[6:], validate=True).decode().split(':', 1)
            actual_hash = hashlib.sha256(supplied_password.encode()).hexdigest()
            expected_hash = hashlib.sha256(password.encode()).hexdigest() if len(password) >= 20 else PASSWORD_SHA256
            authenticated = username == 'nexus' and bool(expected_hash) and hmac.compare_digest(actual_hash, expected_hash)
        except (ValueError, UnicodeError):
            pass
    supplied = request.cookies.get('nexus_preview_access', '')
    cookie = COOKIE_ACCESS
    if not (authenticated or hmac.compare_digest(supplied, cookie)):
        return Response('Private Nexus demo: sign in with the preview credentials.', status_code=401,
                        headers={'WWW-Authenticate': 'Basic realm="Nexus preview", charset="UTF-8"', 'Cache-Control': 'no-store'})
    # Browser API calls use Bearer authentication; the access cookie preserves
    # preview authentication without interfering with the agent token header.
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Nexus-Preview'] = 'disposable-test-credits'
    response.set_cookie('nexus_preview_access', cookie, secure=True, httponly=True, samesite='strict', max_age=3600)
    return response
