from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Pet
# ModelForm: Form được tạo từ Model -> tạo ra những ô input y chang định nghĩa của model.
# Form: Dạng freestyle/custom form.
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet # Form này dành cho Model nào
        fields = '__all__' # ('name', 'age', 'type') # Chọn ô input cho cột trong table đc hiển thị
        widgets = { # Thêm các thuộc tính HTML vào các ô input của form
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'vacinated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dewormed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sterilized': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields.pop('id', None)
            # self.fields.pop('name', None)

    # Khi tạo server validate thì tạo ở phia forms.
    # Khi muốn validate cho 1 field thì tạo hàm có dạng clean_<tên field muốn validate>

    # Pet không được trùng tên, id
    def clean_id(self):
        print("Validate Id")
        # Thử lấy Pet với id người dùng gửi lên.
        # Nếu trả về 1 pet object thì id đã trùng, báo lỗi
        # Nếu không trả về thì id chưa trùng, trả lại id tiếp tục xử lý
        try:
            pet_id = self.cleaned_data['id']
            Pet.objects.get(id=pet_id)
            print("Đã trùng id, văng lỗi")
            raise ValidationError(f'Pet với id={pet_id} đã tồn tại. Vui lòng nhập id khác')
        except Pet.DoesNotExist:
            print("Pet với id chưa tồn tại")
            return self.cleaned_data['id']

    def clean_name(self):
        if self.instance.id and self.instance.name == self.cleaned_data['name']:
            # Dành cho trường hợp edit Pet nhưng không sữa `name`
            return self.cleaned_data['name']
        print("Validate Name")
        # Thử lấy Pet với name người dùng gửi lên.
        # Nếu trả về 1 pet object thì name đã trùng, báo lỗi
        # Nếu không trả về thì name chưa trùng, trả lại name tiếp tục xử lý
        try:
            pet_name = self.cleaned_data['name']
            Pet.objects.get(name=pet_name)
            print("Đã trùng name, văng lỗi")
            raise ValidationError(f'Pet với name={pet_name} đã tồn tại. Vui lòng nhập name khác')
        except Pet.DoesNotExist:
            print("Pet với name chưa tồn tại")
            return self.cleaned_data['name']
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
        max_length=20,
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