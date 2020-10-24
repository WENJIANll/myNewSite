from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名', 
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名或已绑定的邮箱'}))
    password = forms.CharField(label='密码', 
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        # 判断账号密码对不对
        user = auth.authenticate(username=username_or_email, password=password)

        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
                else:
                    raise forms.ValidationError('用户名或密码不正确')
                    
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名', 
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'}
                            )
                        )
    email = forms.EmailField(label='邮箱', 
                             widget=forms.EmailInput(
                             attrs={'class':'form-control', 'placeholder':'请输入邮箱'}
                            )
                        )
    password = forms.CharField(label='密码', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}
                            )
                        )
    password_again = forms.CharField(label='再输入一次密码', 
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'}
                                )
                            )
    vertifycode = forms.CharField(label='验证码',
                                  required=False,
                                  widget=forms.TextInput(
                                  attrs={'class':'form-control','placeholder':'此处填写邮箱收到的验证码，点击发送验证码到邮箱'}
                            )
                        )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        code = self.request.session.get('register_code', '')
        vertifycode = self.cleaned_data.get('vertifycode', '')
        if not (code != '' and code == vertifycode):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

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

    def clean_verification_code(self):
        vertifycode = self.cleaned_data.get('vertifycode', '').strip()
        if vertifycode == '':
            raise forms.ValidationError('验证码不能为空')
        return vertifycode

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

class Change_passwordForm(forms.Form):
    old_password = forms.CharField(label='旧密码', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入旧密码'}
                            )
                        )
    new_password = forms.CharField(label='新密码', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入新密码'}
                            )
                        )
    new_password_again = forms.CharField(label='新密码', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再输入新密码'}
                            )
                        )

    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(Change_passwordForm,self).__init__(*args,**kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password','')
        new_password_again = self.cleaned_data.get('new_password_again','')
        if new_password != new_password_again:
            raise forms.ValidationError('两次输入密码不同，平复下心情再试一次')
        return self.cleaned_data

    def clean_old_password(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        old_password = self.cleaned_data.get('old_password','')
        user = self.cleaned_data.get('user','')
        if not user.check_password(old_password):
            raise forms.ValidationError('输入旧密码错误，冷静想一下旧密码')
        else:
            return old_password

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'请输入绑定过的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )
    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('forgot_password_code', '1')
        print(code)
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code
    