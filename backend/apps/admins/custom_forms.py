from django import forms
from django.contrib.auth.forms import AuthenticationForm

from apps.admins.models import AdminSecretKey


class SecretKeyAdminAuthenticationForm(AuthenticationForm):
    secret_key = forms.CharField(
        label="비밀키",
        widget=forms.PasswordInput,
        help_text="관리자용 비밀키를 입력하세요.",
    )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        input_key = self.cleaned_data.get("secret_key")
        secret_key_obj = AdminSecretKey.objects.order_by('-id').first()
        if not secret_key_obj or input_key != secret_key_obj.key:
            raise forms.ValidationError("비밀키가 일치하지 않습니다.", code="invalid_secret_key")
