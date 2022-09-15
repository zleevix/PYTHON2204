from django.shortcuts import render
# from myapp.models import Pet # xài lại model của myapp
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# TẠO REST API

# Xài API

# Đầu tiên phải là URL
#               là method: POST, GET, UPDATE, DELETE, PATCH, OPTIONS
# Ý nghĩa ccuar các method: từ client gửi lên server
# POST: Dùng trong trường hợp tạo mới 1 object
# GET: Dùng để đọc hết/chi tiết của objects/object
# PUT: Dùng để chỉnh sửa 1 object (cung cấp hết toàn bộ các thuộc tính của đối tượng)
# DELETE: Dùng để xóa 1 object.
# PATCH: (bản vá lỗi) cũng dùng dể chỉnh sửa 1 object (Muốn chỉnh sửa cái gì thì bỏ vào)
# OPTIONS: thường dùng để kiểm tra 1 URL nó hổ trợ mình những methods nào.

# Status code:
# Informational responses (100–199)

# Successful responses (200–299)
# 200 OK, 201 Created, 204 No content
# 200 OK thành công. 
# 201 Created thì nó sẽ dành cho HTTP method POST
# 204 No content: chỉnh sửa

# Redirection messages (300–399)

# Client error responses (400–499)
# 400 Bad Request: data gửi lên lỗi
# 401 Unthorized: chưa đăng nhập
# 403 Forbbiden: Không có quyền vào 1 resource nào đó
# 404 Not Found: object không tìm thấy
# 405 Method Not allow: HTTP method với URL đó không đc cho phép
# 408 Request Timeout: Server phản hồi chậm.
# 409 Conflict: thông tin tạo mới sẽ xung đột với cái có sẳn.

# Server error responses (500–599)
# 500 Internal Server 
# 502 Bad gateway
# 503 Service Unavailable

# R: Read 
# URL: /api/pets
# HTTP Method: GET
# HTTP response code: 200 OK
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_list_pets(request):
    pets = Pet.objects.all()
    results = []
    for pet in pets:
        results.append({
            'id': pet.id,
            'name': pet.name,
            'age': pet.age,
            'type': pet.type,
            'length': pet.length,
            'weight': pet.weight,
            'color': pet.color,
            'vacinated': pet.vacinated,
            'dewormed': pet.dewormed,
            'sterilized': pet.sterilized,
        })
    return Response(data=results, status=200)

# R: Read 
# URL: /api/pet/<pet_id>
# HTTP Method: GET
# HTTP response code: 
#   200 OK
#   404 Not found
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_detail_pet(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
        data = {
            'id': pet.id,
            'name': pet.name,
            'age': pet.age,
            'type': pet.type,
            'length': pet.length,
            'weight': pet.weight,
            'color': pet.color,
            'vacinated': pet.vacinated,
            'dewormed': pet.dewormed,
            'sterilized': pet.sterilized,
        }
        return Response(data=data, status=200)
    except Pet.DoesNotExist:
        return Response(data={'error': f'Pet with {pet_id} not found'}, status=404)

# C: CREATE 
# URL: /api/pet/add
# HTTP Method: POST
# HTTP response code: 
#   200 OK
#   409 Conflict
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_add_pet(request):
    try:
        pet_id = request.data['id']
        Pet.objects.get(id=pet_id)
        return Response(data={'error': f'Pet with {pet_id} already exist.'}, status=409)
    except Pet.DoesNotExist:
        pass

    try:
        pet_name = request.data['name']
        Pet.objects.get(name=pet_name)
        return Response(data={'error': f'Pet with {pet_name} already exist.'}, status=409)
    except Pet.DoesNotExist:
        pass

    Pet.objects.create(
        id=request.data['id'],
        name=request.data['name'],
        age=request.data['age'],
        type=request.data['type'],
        length=request.data['length'],
        weight=request.data['weight'],
        color=request.data['color'],
        vacinated=request.data['vacinated'],
        dewormed=request.data['dewormed'],
        sterilized=request.data['sterilized'],
    )
    return Response(status=201)

# U: Update 
# URL: /api/pet/update/<pet_id>
# HTTP Method: PUT
# HTTP response code: 
#   204 No content
#   404 Not found
#   400 Bad Request
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def api_update_pet(request, pet_id):
    try:
        if set(request.data.keys()) != set([ 'name', 'age', 'type', 'length', 'weight', 'color', 'vacinated', 'dewormed', 'sterilized']):
            return Response(data={'error': 'Your data request is invalid'}, status=400)
        pet = Pet.objects.get(id=pet_id)
        pet.name=request.data['name']
        pet.age=request.data['age']
        pet.type=request.data['type']
        pet.length=request.data['length']
        pet.weight=request.data['weight']
        pet.color=request.data['color']
        pet.vacinated=request.data['vacinated']
        pet.dewormed=request.data['dewormed']
        pet.sterilized=request.data['sterilized']
        pet.save()
        return Response(status=204)
    except Pet.DoesNotExist:
        return Response(data={'error': f'Pet with {pet_id} not found'}, status=404)

# D: DELETE
# URL: /api/pet/delete/<pet_id>
# HTTP Method: DELETE
# HTTP response code: 
#   204 No content
#   404 Not found
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def api_delete_pet(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
        pet.delete()
        return Response(status=204)
    except Pet.DoesNotExist:
        return Response(data={'error': f'Pet with {pet_id} not found'}, status=404)
