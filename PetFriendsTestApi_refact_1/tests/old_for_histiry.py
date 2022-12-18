from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest
from datetime import datetime
from decorators import log

pf = PetFriends()

@pytest.fixture(scope="class", autouse=True)
def get_key(email=valid_email, password=valid_password):
    '''тест на полученик ключа авторизации и получения ключа авторизации'''
    status, result = pf.res_get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    return result

@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print (f"\nТест шел: {end_time - start_time}")


def generate_string(n): #функция для генерации n символов
   return "x" * n

def russian_chars(): #функция русских символов
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars(): #функция китайских символов
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():  #функция спецсиволов
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

def is_age_valid(age): # Проверяем, что возраст - это число от 1 до 49 и целое
    if age.isdigit() and 0 < int(age) < 50 and float(age) == int(age):
        return False
    else:
        return True


class TestPositive: #надо перебирать, после параметризации все перемешается


    @pytest.mark.receiving
    @pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
    def test_get_all_pets_with_valid_key_positive(self, get_key, filter):
        '''тест на получение списка всех животных'''
        auth_key = get_key
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) >= 0


    @pytest.mark.receiving
    @pytest.mark.parametrize("filter", [generate_string(255), generate_string(1000), russian_chars(),
                                        chinese_chars(), special_chars()], ids=['255 simbols', '1000 simbols', 'russian_chars', 'chinese_chars', 'special_chars'])
    def test_get_all_pets_with_valid_key_negative(self, get_key, filter):
        '''тест на получение списка всех животных'''
        auth_key = get_key
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 400 or 500



    @pytest.mark.addition
    def test_post_add_information_about_new_pet_valid(self, get_key, name='EE', animal_type='ss', age='69', pet_photo='images/ddd.jpeg'):
        '''тест на добавление нового животного'''
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = get_key
        status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
        pet_id = result['id']
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
        assert pet_id == my_pets['pets'][0]['id']

    @pytest.mark.addition
    @pytest.mark.parametrize('name', [generate_string(255), generate_string(1001), russian_chars(),
                                      russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN',
                                  'chinese', 'specials', 'digit'])
    @pytest.mark.parametrize("animal_type", [generate_string(255), generate_string(1001), russian_chars(),
                                             russian_chars().upper(), chinese_chars(),special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese',
                                  'specials', 'digit'])
    @pytest.mark.parametrize("age", ['1'],
                             ids=['min'])
    def test_post_add_information_about_new_pet_valid_without_foto_positive(self, get_key, name, animal_type, age):
        '''тест на добавление нового животного без фото'''
        auth_key = get_key
        status, result = pf.post_add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
        pet_id = result['id']
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
        assert pet_id == my_pets['pets'][0]['id']

    @pytest.mark.addition
    @pytest.mark.parametrize('name', [''],
                             ids=['empty'])
    @pytest.mark.parametrize("animal_type", [''],
                             ids=['empty'])
    @pytest.mark.parametrize("age", ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                                     russian_chars(), russian_chars().upper(), chinese_chars()],
                             ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
                                  'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
    def test_post_add_information_about_new_pet_valid_without_foto_negative(self, get_key, name, animal_type, age):
        '''тест на добавление нового животного без фото'''
        auth_key = get_key
        status, result = pf.post_add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
        pet_id = result['id']
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")

        assert status == 200  # должно быть 400



    def test_delete_pet_from_database_valid(self, get_key):
        '''Тест на удаление питомца из базы'''
        auth_key = get_key
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        if len(my_pets['pets']) == 0:
            pf.post_add_information_about_new_pet(auth_key, name='EE', animal_type='ss', age='69', pet_photo='images/ddd.jpeg')
            _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet_from_database(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        assert status == 200
        #assert pet_id != my_pets['pets'][0]['id']


    def test_update_information_about_pet_valid(self, get_key, name ='second_name', animal_type='second_type', age='666'):
        '''Тест на обновление информации по животному'''
        auth_key = get_key
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


class TestNegative:
    def test_get_all_pets_with_invalid_key(self, filter=''):
        '''негативный тест на получение списка всех c невалидным ключом'''
        auth_key = {'key': 'incorrect'}
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 403


    def test_get_all_pets_with_valid_key_and_invalid_key(self, get_key, filter='invalid'):
        '''негативный тест на получение списка всех животных по неправильному фильтру'''
        auth_key = get_key
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 500


    @pytest.mark.skip(reason="Баг в продукте = дает загрузить фото некорректного формата")
    def test_post_add_information_about_new_pet_invalid_foto(self, get_key, name='EE', animal_type='ss', age='69', pet_photo='images/test.txt'):
        '''тест на добавление нового животного c фото некорректного формата'''
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = get_key
        status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        assert status == 400


    @pytest.mark.skip(reason="Баг в продукте дает авторизоваться со старым ключом")
    def test_get_all_pets_with_old_key(self, filter=''):
        '''тест на получение списка всех животных c истекшим токеном'''
        auth_key = {'key': '59d8d4905fabc75ee613fc3a0aca63bbfe02d6664846c389e30fbc99'}
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 403

    def test_get_all_pets_with_int_key(self, filter=''):
        '''тест на получение списка всех животных c токеном числом'''
        auth_key = {'key': '456435645643564364364563456'}
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 403


    @pytest.mark.skip(reason="Баг в продукте = возвращает неверный тип ошибки")
    def test_add_photo_of_incorrect_id_pet(self, get_key, pet_id = 'f5edbaf7-b5a4-4b6c-8d84-d84c5f5c4cc4', pet_photo='images/ddd.jpeg'):
        '''негативный тест на добавление фото по некорректному ид'''
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = get_key
        status, _ = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 404


    @pytest.mark.skip(reason="Баг в продукте = дает добавить второе фото")
    def test_duble_foto_dawnload(self, get_key, pet_photo='images/hello.jpg'):
        '''негативный тест на добавление второго фото для питомца'''
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = get_key
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


    @pytest.mark.skip(reason="Баг в продукте = дает создать без имени")
    def test_create_new_pet_without_name(self, get_key, name='', animal_type='ss', age='69', pet_photo='images/ddd.jpeg'):
        '''Негативный тест на создание питомца без имени'''
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = get_key
        status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
        assert status == 400


    def test_update_information_about_pet_with_incorrect_id(self, get_key, pet_id = 'werq2314dsa123', name='ewrwer', animal_type='ss', age='69'):
        '''Негативныйтест на обновление информации по невалиденому id'''
        auth_key = get_key
        status, _ = pf.update_information_about_pet(auth_key, pet_id, name, animal_type, age)
        status == 404












