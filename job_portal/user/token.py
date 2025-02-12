from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def __init__(self, expiration_time=10*60):
        self.expiration_time = expiration_time
        super(CustomPasswordResetTokenGenerator, self).__init__()

    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp) + str(user.is_active))

    def check_token(self, user, token):
        if not (user and token):
            return False
        # Parse the token to get the timestamp
        try:
            ts_b36, _ = token.split("-")
            ts = int(ts_b36, 36)
        except ValueError:
            return False

        # Check if the token is expired
        if (datetime.now() - datetime(2001, 1, 1)).total_seconds() - ts > self.expiration_time:
            return False

        return super(CustomPasswordResetTokenGenerator, self).check_token(user, token)

custom_token_generator = CustomPasswordResetTokenGenerator(expiration_time=10*60)
