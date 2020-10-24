from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', 
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码', 
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名', 
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'}))
    email = forms.EmailField(label='邮箱', 
                             widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='再输入一次密码', 
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

class ChangeNicknameform(forms.Form):
    new_nickname = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'})
    )

    # 通过类的初始化来为实例添加属性
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameform, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data


    def clean_nickname(self):
        new_nickname = self.cleaned_data.get('new_nickname','').strip()
        if new_nickname == '':
            raise ValidationError("新昵称不可为空")
        return new_nickname

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control','placeholder':'请输入邮箱地址'}
            )
    )

    vertifycode = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'此处填写收到的验证码，点击发送验证码到邮箱'}
            )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bindemailcode', '')
        vertifycode = self.cleaned_data.get('vertifycode', '')
        if not (code != '' and code == vertifycode):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        # 这里为什么要return回去呀
        return email

    def clean_verification_code(self):
        vertifycode = self.cleaned_data.get('vertifycode', '').strip()
        if vertifycode == '':
            raise forms.ValidationError('验证码不能为空')
        return vertifycode