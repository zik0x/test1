from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''тест на полученик ключа авторизации'''
    status, result = pf.res_get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    '''тест на получение списка всех животных'''
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


def test_post_add_information_about_new_pet_valid(name='EE', animal_type='ss', age='69', pet_photo='images/ddd.jpeg'):
    '''тест на добавление нового животного'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    pet_id = result['id']
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert pet_id == my_pets['pets'][0]['id']


def test_delete_pet_from_database_valid():
    '''Тест на удаление питомца из базы'''
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_information_about_new_pet(auth_key, name='EE', animal_type='ss', age='69', pet_photo='images/ddd.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    assert status == 200
    #assert pet_id != my_pets['pets'][0]['id']


def test_update_information_about_pet_valid(name ='second_name', animal_type='second_type', age='666'):
    '''Тест на обновление информации по животному'''
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_information_about_new_pet(auth_key, name='first_name', animal_type='first_type', age='69', pet_photo='images/ddd.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.update_information_about_pet(auth_key, pet_id, name, animal_type, age)
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        assert status == 200
        assert name == my_pets['pets'][0]['name']
        assert age == my_pets['pets'][0]['age']
    else:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_information_about_pet(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert name == result['name']


def test_get_all_pets_with_invalid_key(filter=''):
    '''негативный тест на получение списка всех c невалидным ключом'''
    auth_key = {'key': 'incorrect'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_get_all_pets_with_valid_key_and_invalid_key(filter='invalid'):
    '''негативный тест на получение списка всех животных по неправильному фильтру'''
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


def test_post_add_information_about_new_pet_invalid_foto(name='EE', animal_type='ss', age='69', pet_photo='images/test.txt'):
    '''тест на добавление нового животного c фото некорректного формата'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    assert status == 400

def test_get_all_pets_with_old_key(filter=''):
    '''тест на получение списка всех животных c истекшим токеном'''
    auth_key = {'key': '59d8d4905fabc75ee613fc3a0aca63bbfe02d6664846c389e30fbc99'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_get_all_pets_with_int_key(filter=''):
    '''тест на получение списка всех животных c токеном числом'''
    auth_key = {'key': '456435645643564364364563456'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_add_photo_of_incorrect_id_pet(pet_id = 'f5edbaf7-b5a4-4b6c-8d84-d84c5f5c4cc4', pet_photo='images/ddd.jpeg'):
    '''негативный тест на добавление фото по некорректному ид'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    status, _ = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 404


def test_duble_foto_dawnload(pet_photo='images/hello.jpg'):
    '''негативный тест на добавление второго фото для питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_information_about_new_pet(auth_key, name='first_name', animal_type='first_type', age='69', pet_photo='images/ddd.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 404
    else:
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 404

def test_create_new_pet_without_name(name='', animal_type='ss', age='69', pet_photo='images/ddd.jpeg'):
    '''Негативный тест на создание питомца без имени'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    assert status == 400


def test_update_information_about_pet_with_incorrect_id(pet_id = 'werq2314dsa123', name='ewrwer', animal_type='ss', age='69'):
    _, auth_key = pf.res_get_api_key(valid_email, valid_password)
    status, _ = pf.update_information_about_pet(auth_key, pet_id, name, animal_type, age)
    status == 404













