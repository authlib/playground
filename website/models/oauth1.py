from sqlalchemy import Column
from sqlalchemy import (
    Integer, String, Text
)
from authlib.flask.oauth1.sqla import (
    OAuth1ClientMixin,
    OAuth1TokenCredentialMixin,
)

from .base import Base


class OAuth1Client(Base, OAuth1ClientMixin):
    __tablename__ = 'oauth1_client'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(48), nullable=False)
    website = Column(Text)


class OAuth1Token(Base, OAuth1TokenCredentialMixin):
    __tablename__ = 'oauth1_token'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    def set_user_id(self, user_id):
        self.user_id = user_id
