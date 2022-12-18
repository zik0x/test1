from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest
from datetime import datetime
from decorators import log
from support_func import generate_string, russian_chars, chinese_chars, special_chars, is_age_valid

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


@pytest.mark.receiving
@pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
@pytest.mark.parametrize("content_type", ['application/json'], ids=['application/json'])
def test_get_all_pets_with_valid_key_positive(get_key, content_type, filter):
    '''тест на получение списка всех животных'''
    auth_key = get_key
    status, result = pf.get_list_of_pets(auth_key, content_type, filter)
    assert status == 200
    assert len(result['pets']) >= 0

@pytest.mark.addition
def test_post_add_information_about_new_pet_valid(get_key, name='EE', animal_type='ss', age='69', pet_photo='images/ddd.jpeg'):
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
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_post_add_information_about_new_pet_valid_without_foto_positive(get_key, name, animal_type, age):
    '''Позитивный тест на добавление нового животного без фото'''
    auth_key = get_key
    status, result = pf.post_add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    pet_id = result['id']
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert pet_id == my_pets['pets'][0]['id']


def test_delete_pet_from_database_valid(get_key):
    '''Позитивный тест на удаление питомца из базы'''
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


def test_update_information_about_pet_valid(get_key, name ='second_name', animal_type='second_type', age='666'):
    '''Позитивный тест на обновление информации по животному'''
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
