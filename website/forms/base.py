from flask_wtf import FlaskForm
from flask_wtf._compat import string_types
from wtforms.widgets import HiddenInput


class BaseForm(FlaskForm):
    def hidden_fields(self):
        for field in self._fields:
            if isinstance(field, string_types):
                field = getattr(self, field, None)
            if field and isinstance(field.widget, HiddenInput):
                yield field

    def visible_fields(self):
        for field in self._fields:
            if isinstance(field, string_types):
                field = getattr(self, field, None)

            if field and not isinstance(field.widget, HiddenInput):
                yield field

