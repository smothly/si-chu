from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from allauth.account.forms import SignupForm as BaseSignupForm
from allauth.account.forms import LoginForm as BaseLoginForm
from allauth.account.forms import AddEmailForm

from .models import majors, grades

User = get_user_model()


class SignupForm(BaseSignupForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    grade = forms.ChoiceField(choices=grades)
    major = forms.ChoiceField(choices=majors)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = "성"
        self.fields['first_name'].label = "이름"
        self.fields['username'].label = "아이디"
        self.fields['email'].label = "이메일"
        self.fields['password1'].label = "비밀번호"
        self.fields['password2'].label = "비밀번호 (확인)"
        self.fields['grade'].label = "학년"
        self.fields['major'].label = "전공"

        self.fields['last_name'].widget.attrs.update({"class": "input", "autofocus": True, "placeholder": "성"})
        self.fields['first_name'].widget.attrs.update({"class": "input", "placeholder": "이름"})
        self.fields['username'].widget.attrs.update({"class": "input", "autofocus": False})
        self.fields['email'].widget.attrs.update({"class": "input", "placeholder": "이메일@kookmin.ac.kr"})
        self.fields['password1'].widget.attrs.update({"class": "input"})
        self.fields['password2'].widget.attrs.update({"class": "input"})

    def clean_email(self):
        value = super(SignupForm, self).clean_email()
        if value.split("@")[-1] not in settings.ALLOWED_EMAIL_HOSTS:
            self.add_error(
                'email', "{} 메일만 사용가능합니다.".format(', '.join(settings.ALLOWED_EMAIL_HOSTS))
            )
        return value

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.grade = request.POST.get('grade')
        user.major = request.POST.get('major')
        user.save()
        return user


class LoginForm(BaseLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = "아이디"
        self.fields['password'].label = "비밀번호"

        self.fields['login'].widget.attrs.update({"class": "input", "autofocus": True, "placeholder": "아이디"})
        self.fields['password'].widget.attrs.update({"class": "input", "placeholder": "비밀번호"})


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    grade = forms.ChoiceField(choices=grades)
    major = forms.ChoiceField(choices=majors)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'grade', 'major']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = "성"
        self.fields['first_name'].label = "이름"
        self.fields['grade'].label = "학년"
        self.fields['major'].label = "전공"

        self.fields['last_name'].required = False
        self.fields['first_name'].required = False
        self.fields['grade'].required = False
        self.fields['major'].required = False

        self.fields['last_name'].widget.attrs.update({"class": "input", "autofocus": True, "placeholder": "성"})
        self.fields['first_name'].widget.attrs.update({"class": "input", "placeholder": "이름"})


class EmailUpdateForm(AddEmailForm):

    def __init__(self, *args, **kwargs):
        super(EmailUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({"class": "input"})

    def clean_email(self):
        value = super(EmailUpdateForm, self).clean_email()
        if value.split("@")[-1] not in settings.ALLOWED_EMAIL_HOSTS:
            self.add_error(
                'email', "{} 메일만 사용가능합니다.".format(', '.join(settings.ALLOWED_EMAIL_HOSTS))
            )
        return value
