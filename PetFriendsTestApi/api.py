import requests
import json
from settings import valid_email, valid_password
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'


    def res_get_api_key(self, email: str, password: str):
        '''GET /api/key метод обращается к API авторизации и позвращает статус код и ключ'''
        headers = {
            'email' : email,
            'password' : password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter:str =''):
        '''Get /api/pets метод получения списка вех питомцев'''
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_information_about_new_pet(self, auth_key, name: str, animal_type: str, age: str, pet_photo):
        '''POST /api/pets метод добавления нового питомца'''
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key, pet_id: str):
        '''Delete /api/pets/{pet_id} метод для удаления из базы'''
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_information_about_pet(self, auth_key, pet_id: str, name:str = '', animal_type:str = '', age:str = ''):
        '''PUT /api/pets/{pet_id} метод для редактирования'''
        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'animal_type': animal_type,
                'age': age,}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_information_about_new_pet_without_photo(self, auth_key, name: str, animal_type: str, age: str):
        '''POST /api/create_pet_simple метод добавления нового питомца без фото'''
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
                }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def Add_photo_of_pet(self,auth_key, pet_id: str, pet_photo):
        '''POST /api/pets/set_photo/{pet_id} метод добавления только фото'''
        data = MultipartEncoder(fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result






# p = PetFriends()
# _, key = p.res_get_api_key(valid_email, valid_password)
# print(key)
# status, result= p.res_get_api_key('', valid_password)
# print(status)
# print(result)
# status, result = p.post_add_information_about_new_pet(key, 'EE', 'ss', '69', 'tests/images/ddd.jpeg')
# print(status)
# print(result)
# key = {'key': 'incorrect'}
# status, result = p.get_list_of_pets(key, filter="my_pets")
# print(status)
# print(result)
# status, result = p.delete_pet_from_database(key, 'cfd7c618-c5a3-4c68-a8d2-cd42bdf7c989')
# print(status)
# print(result)
# status, result = p.update_information_about_pet(key, pet_id='79e8de4e-3c7e-4cb0-997c-0bbdbe65934c', name='first')
# print(status)
# print(result)
# status, result = p.post_add_information_about_new_pet_without_photo(key, '', 'ss', '69')
# print(status)
# print(result)
# status, result = p.Add_photo_of_pet(key, pet_id = '25c198dd-d172-42a6-bf3c-0308bc10cda8', pet_photo='tests/images/ddd.jpeg')
# print(status)
# print(result)