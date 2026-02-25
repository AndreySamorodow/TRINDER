from src.config import settings

import urllib.parse
import secrets

def generate_google_oauth_redirect_uri():
    random_state = secrets.token_urlsafe(16)
    #Запись в бд или редис
    
    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": "http://localhost:5500/auth/google",
        "response_type": "code",
        "scope": " ".join([
            "openid",
            "profile",
            "email"
        ]),
        "access_type": "offline",
        "state": random_state
    }

    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

    return f"{base_url}?{query_string}"