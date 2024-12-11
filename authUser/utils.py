from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailConfirmation(PasswordResetTokenGenerator):
    def make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


confirmation_token = EmailConfirmation()
