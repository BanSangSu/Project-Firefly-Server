from authlib.integrations.starlette_client import OAuth
from core.config import settings

oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='apple',
    client_id=settings.APPLE_CLIENT_ID,
    client_secret=settings.APPLE_CLIENT_ID, # Placeholder, will be generated
    server_metadata_url='https://appleid.apple.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'name email', 'response_mode': 'form_post'},
    jwk_uri=f'https://appleid.apple.com/auth/keys', # Public key URL
    client_secret_generator=lambda metadata: {
        "client_id": metadata["client_id"],
        "team_id": settings.APPLE_TEAM_ID,
        "key_id": settings.APPLE_KEY_ID,
        "private_key": settings.APPLE_PRIVATE_KEY
    }
)
