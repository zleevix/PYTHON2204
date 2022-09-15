from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.
# Bảng đơn
class Student(models.Model):
    # Tên table liên kết với class model: <tên app viết thường>_<tên class viết thường>
    # name, age, gender, email, phone
    # name, email, phone (lấy chữ 0 ở đầu sdt), gender: TEXT
    # age: INTEGER
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.BooleanField() # True: name, False là nữ
    email = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    address = models.TextField(default="Hồ Chí Minh") # textfield là không giới hạn về độ dài

    def __str__(self):
        return self.name

# Những lệnh kiểm tra với thay đổi của models.py
# 1. Kiễm tra xem mình có thay đổi gì hay không ? python manage.py makemigrations <tên app>
    # Không có tên app thì sẽ toàn bộ các app

# 2. Xem các thay đổi với dạng SQL command: python manage.py sqlmigrate <tên app> <số tạo ở command trên>

# 3. Apply các thay đổi xuống database: python manage.py migrate

# Quan hệ 1-1
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} is a Place"

    class Meta:
        db_table = "Place" # `db_table` định tên tùy chọn của table trong DB

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE, # `on_delete: CASCADE` khi mà mình xóa khóa chính của liên kết FK thì sẽ tự đông xóa hết theo FK 
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.place.name} the restaurant"

    class Meta:
        db_table = "Restaurant"

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        db_table = "Reporter"

class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['headline']
        db_table = "Article"

# class Publication(models.Model):
#     title = models.CharField(max_length=30)

#     class Meta:
#         ordering = ['title'] # Dùng để sắp xếp, tăng dần ['title'] / ['-title'] giảm dần
#         db_table = "Publication"

#     def __str__(self):
#         return self.title

# class Article(models.Model):
    # # Tên table tạo mới thì sẽ lấy <tên class chứa ManyToManyField>_<trường ManyToMany>
    # headline = models.CharField(max_length=100)
    # publications = models.ManyToManyField(Publication)

    # class Meta:
    #     ordering = ['headline']
    #     db_table = "Article"

    # def __str__(self):
    #     return self.headline

class Pet(models.Model):
    TYPE_CHOICES = (
        ('cat', 'Cat'),
        ('dog', 'Dog')
    )
    id = models.CharField('Mã Thú Cưng', max_length=10, primary_key=True)
    name = models.CharField('Tên Thú Cưng', max_length=30)
    age = models.IntegerField('Tuổi')
    type = models.CharField('Loại', max_length=3, choices=TYPE_CHOICES)
    weight = models.IntegerField('Cân Nặng')
    length = models.IntegerField('Chiều Dài')
    color = models.CharField('Màu Sắc', max_length=7) # #00FF1A
    vacinated = models.BooleanField()
    dewormed = models.BooleanField()
    sterilized = models.BooleanField()

    class Meta:
        db_table = "Pet"
        # ordering = ['-id']

