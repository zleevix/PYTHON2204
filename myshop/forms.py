from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Form đăng ký RegistrationFrom
# Bắt buộc người dùng phải điền: 
    #username: username không trùng
    #password: 
    #first_name
    #last_name
    #email: email cũng không được

class RegistrationForm(forms.Form):
    username = forms.CharField(
        label="Tên Đăng Nhập",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mật Khẩu",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Nhập Lại Mật Khẩu",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="Tên",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Họ",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    # Kiễm tra username/email không trùng. password và confirm_password phải giống nhau
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise ValidationError(f'Tên đăng nhập đã trùng')
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise ValidationError(f'Email đã trùng')
        except User.DoesNotExist:
            return email

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError("Mật khẩu và nhập lại không giống nhau")
        return self.cleaned_data['confirm_password']

    def save(self):
        User.objects.create_user( # create_user là lưu vào CSDL có hash password. create lưu dạng raw data
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Tên Đăng Nhập",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mật Khẩu",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # # hàm này dùng để kiểm tra thông tin người dùng gửi lên
    # # Láy username, password check thông tin
    # def clean_password(self):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #     try:
    #         # Thử get User từ username và password
    #         # Nếu trả về thì thông tin hợp lệ.