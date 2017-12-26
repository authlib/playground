import time
from sqlalchemy import Column
from sqlalchemy import (
    Integer, String, Text
)
from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)

from .base import Base


class OAuth2Client(Base, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(48), nullable=False)
    website = Column(Text)
    allowed_grants = Column(Text)

    def check_response_type(self, response_type):
        grant_maps = {'code': 'authorization_code', 'token': 'implicit'}
        grant_type = grant_maps.get(response_type)
        if not grant_type:
            return False
        return self.check_grant_type(grant_type)

    def check_grant_type(self, grant_type):
        return grant_type in self.allowed_grants.split()


class OAuth2AuthorizationCode(Base, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)


class OAuth2Token(Base, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    def is_refresh_token_expired(self):
        expired_at = self.created_at + self.expires_in * 2
        return expired_at < time.time()

    @classmethod
    def query_token(cls, access_token):
        return cls.query.filter_by(access_token=access_token).first()
