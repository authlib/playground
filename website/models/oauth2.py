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
