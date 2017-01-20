from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

import re

import pyotp

BASE32_RE = re.compile(r'[^A-Za-z2-7]')

class Code(models.Model):
    """
    A TOTP-based code.

    Stores secret information and can calculate current value
    """
    code_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, blank=False, help_text='User-friendly name for code')
    secret = models.CharField(max_length=255, blank=False)

    @property
    def current_value(self):
        """
        Calculates current value for this TOTP
        """
        if not hasattr(self, '_totp'):
            self._totp = pyotp.TOTP(self.secret)
        return self._totp.now()

    def clean(self):
        """
        Ensure secret is a valid value
        """
        self.secret = BASE32_RE.sub('', self.secret)
        if len(self.secret) != 32:
            raise ValidationError('Secret key must be 32 characters long and A-Z or 2-7 only (Base32)')

        super().clean()

    def __str__(self):
        return '{}: {}'.format(self.user, self.name)
