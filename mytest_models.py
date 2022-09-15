import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
django.setup()
os.getcwd()
'/Users/lehungvi/Library/CloudStorage/OneDrive-Personal/PythonWork/T3H/PYTHON2204/django-web/myweb'
# from myapp.models import Student
# # CURD: Create, Update, Read, Delete
# # C: Create bằng lệnh
# # student1 = Student(name="Ronaldo", age=37, gender=True, email="ronaldo@gmail.com", phone="012456789", address="Anh")
# # student1.save()
# # # Lưu ý: khi tạo object từ class như trên, thì phải cần thêm 1 lệnh nữa để thêm record vào table obj.save()
# # student2 = Student.objects.create(name="Messi", age=35, gender=True, email="messi@gmail.com", phone="01234", address="Pháp")
# # #Dùng qua tên class.objects.create thì khôgn cần .save()

# # R: Read
# Student.objects.all() # tương đương với SELECT * FROM Sudent;
# # LƯU Ý: `objects` phải có `s`
# students = Student.objects.all()
# for student in students:
#     print(student.name)
# # Lưu ý: tên biến nên có liên quan với tên class :)) tên class viết dạng số nhiều.
# # Lấy số nhiều, tên biến tiếng anh dạng số nhiều. Khi dùng vòng lặp qua thì sẽ số ít.
# # Các bạn sẽ biến chính xác tên class

# # Read detail 1 Student
# # SELECT * FROM Student WHERE id = 1;
# student = Student.objects.get(id = 1)
# # student.__dict__
# # {'_state': <django.db.models.base.ModelState object at 0x7f914f5620a0>, 'id': 1, 'name': 'Ronaldo', 'age': 37, 'gender': True, 'email': 'ronaldo@gmail.com', 'phone': '012456789', 'address': 'Anh'}
# student = Student.objects.get(id = 1) # .get là phải trả về duy nhất 1 object
# student
# # <Student: Student object (1)>
# student = Student.objects.filter(id = 1)
# student
# # <QuerySet [<Student: Student object (1)>]>
# student = Student.objects.filter(id = 1) # .filter thì trả về 1 danh sách.
# student = Student.objects.filter(name__startswith = "M") # Bắt đầu là chữ M = startswith
# student
# # <QuerySet [<Student: Student object (2)>, <Student: Student object (3)>]>
# for student in students:
#     print(student.name)

# # Ronaldo
# # Messi
# students = Student.objects.filter(name__startswith = "M") # Bắt đầu là chữ M = startswith 
# for student in students:
#     print(student.name)

# # Messi
# # Mbape
# students = Student.objects.filter(name__endswith = "M") # Bắt đầu là chữ M = startswith
# students
# # <QuerySet []>
# students = Student.objects.filter(name__contains = "M") # Bắt đầu là chữ M = startswith
# students
# # <QuerySet [<Student: Student object (2)>, <Student: Student object (3)>]>


# # Student.objects.get(pk=1)
# # <Student: Student object (1)>
# # student.__dict__
# # {'_state': <django.db.models.base.ModelState object at 0x7f914f562190>, 'id': 3, 'name': 'Mbape', 'age': 21, 'gender': True, 'email': 'mbape@gmail.com', 'phone': '01234', 'address': 'Pháp'}
# ronaldo = Student.objects.get(name = "Ronaldo")
# ronaldo.name = "Cristiano Ronaldo"
# ronaldo.email = "cristianoronaldo@gmail.com"
# ronaldo.save()

# Student.objects.get(pk=3).delete()
# # (1, {'myapp.Student': 1})

# from myapp.models import Place, Restaurant
# Place.objects.create(name="Quận 12", address="Quận 12")
# # <Place: Quận 12 is a Place>
# Place.objects.create(name="Quận 1", address="Quận 1")
# # <Place: Quận 1 is a Place>
# Place.objects.create(name="Quận 2", address="Quận 2")
# # <Place: Quận 2 is a Place>
# Place.objects.create(name="Quận 3", address="Quận 3")
# # <Place: Quận 3 is a Place>
# Place.objects.create(name="Quận 4", address="Quận 4")
# # <Place: Quận 4 is a Place>
# Place.objects.create(name="Quận 5", address="Quận 5")
# # <Place: Quận 5 is a Place>
# restaurant1=Restaurant(place_id=1, serves_hot_dogs=True, serves_pizza=True)
# restaurant1.save()
# restaurant1=Restaurant(place_id=1, serves_hot_dogs=True, serves_pizza=True)
# restaurant1.save()
# restaurant1=Restaurant(place_id=1, serves_hot_dogs=False, serves_pizza=True)
# restaurant1.save()
# # tên chính xác cột trong table
# place2 = Place.objects.get(pk=2)
# place2
# # <Place: Quận 1 is a Place>
# restaurant1=Restaurant(place_id=place2.id, serves_hot_dogs=False, serves_pizza=True)
# restaurant1.save()
# restaurant = Restaurant(place=place2, serves_hot_dogs=True, serves_pizza=True)
# restaurant.save()
# place3 = Place.objects.get(pk=3)
# restaurant = Restaurant(place=place3, serves_hot_dogs=True, serves_pizza=True)
# restaurant.save()
# Restaurant.objects.create(place=place3, serves_hot_dogs=True, serves_pizza=True)

# place = Place.objects.get(pk=1)
# place.name
# 'Quận 12'
# place.address
# 'Quận 12'
# restautant = Restaurant.objects.get(pk=1)
# restaurant
# # <Restaurant: Quận 2 the restaurant>
# restautant = Restaurant.objects.get(place_id=1)
# restaurant
# # <Restaurant: Quận 2 the restaurant>
# Restaurant.objects.get(place_id=1)
# # <Restaurant: Quận 12 the restaurant>
# Restaurant.objects.get(place_id=4)


# Restaurant.objects.get(place_id=3)
# # <Restaurant: Quận 2 the restaurant>
# place
# # <Place: Quận 12 is a Place>
# restaurant
# # <Restaurant: Quận 2 the restaurant>
# restaurant.place
# # <Place: Quận 2 is a Place>
# place
# # <Place: Quận 12 is a Place>
# place.restaurant
# # <Restaurant: Quận 12 the restaurant>

# #Trong quan hệ 1-1
# # Class A 1-1 class B
# # Thì class giữ OneToOneField thì muốn truy qua class còn thì dùng tên thuộc tính trong giữ OneToOneField
# # Ngược lại thì class kia dùng .<tên class viết thường>

from myapp.models import Reporter, Article
reporter1 = Reporter.objects.create(first_name="Ronaldo",last_name="Cristiano", email="ronaldo@gmail.com")
reporter2 = Reporter.objects.create(first_name="Messi",last_name="Leoniel", email="messi@gmail.com")
# reporter1
# <Reporter: Ronaldo Cristiano>
from django.utils.timezone import now
ar1 = Article(headline="Headline1", pub_date=now(), reporter=reporter1)
ar1.save()

ar2 = Article.objects.create(headline="Headline2", pub_date=now(), reporter=reporter1)
reporter1
# <Reporter: Ronaldo Cristiano>
reporter1.article_set.create(headline="Headline3", pub_date=now())
# <Article: Headline3>
# reporter1.article_set.all() tương đương với Article.objects.filter(reporter=reprorter1)  #  = SELECT * FROM Article WHERE Report.id = Article
reporter1.article_set.all()
# # # <QuerySet [<Article: Headline1>, <Article: Headline2>, <Article: Headline3>]>
Article.objects.filter(reporter=reporter1)
# # <QuerySet [<Article: Headline1>, <Article: Headline2>, <Article: Headline3>]>

# Note 1 - n
# class A 1-n class B
# từ class A truy cập tất các dòng liên kết <tên biến class A>.<tên class B viết thương>_set 

# từ class B, truy cập ngược liên kết với class A <tên biến class B>.<tên class A viết thường>

# from myapp.models import Publication, Article
# p1 = Publication(title="title1")
# p1.save()
# p2 = Publication.objects.create(title="title2")
# Publication.objects.all()
# # <QuerySet [<Publication: title1>, <Publication: title2>]>
# p3 = Publication.objects.create(title="title3")
# Publication.objects.all()
# # <QuerySet [<Publication: title1>, <Publication: title2>, <Publication: title3>]>
# a1 = Article.objects.create(headline="headlien1")
# a2 = Article.objects.create(headline="headlien2")
# Article.objects.all()
# # <QuerySet [<Article: headlien1>, <Article: headlien2>]>
# a1.publications
# # <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x7f8dfa558fa0>
# a1.publications.add(p1,p2)
# p1.article_set.add(a2,a1)
# a1.publications.add(p1,p2,p3)



# p1.article_set.all()
# # <QuerySet [<Article: headlien1>, <Article: headlien2>]>
# a1.publications.all()
# # <QuerySet [<Publication: title1>, <Publication: title2>, <Publication: title3>]>
