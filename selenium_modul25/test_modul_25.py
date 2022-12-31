import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



@pytest.fixture(autouse=True)
def web_browser():
   pytest_driver = webdriver.Chrome(r'C:\Users\koshelevrd\PycharmProjects\chromedriver.exe')
   pytest_driver.set_window_size(1400, 1000)
   pytest_driver.implicitly_wait(5)  #неявное ожидание
   # Переходим на страницу авторизации
   pytest_driver.get('http://petfriends.skillfactory.ru/login')


   yield pytest_driver

   pytest_driver.quit()


def test_show_my_pets(web_browser):
    web_browser.find_element(By.ID, "email").send_keys('frontFL-9275@gmail.com')
    # Вводим пароль
    web_browser.find_element(By.ID, "pass").send_keys('frontFL-9275')
    # Нажимаем на кнопку входа в аккаунт
    web_browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    web_browser.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
    count_pets = web_browser.find_element(By.XPATH, '//div[@class =".col-sm-4 left"]')  #количество животных сверху
    element = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tbody/tr"))) # Явное ожидание
    all_pets = web_browser.find_elements(By.XPATH, '//tbody/tr')
    foto_pets = web_browser.find_elements(By.XPATH, '//img[contains(@src, "data")]')
    fio_pets = web_browser.find_elements(By.XPATH, '//tbody/tr')
    set_name = set()
    set_fio = set()
    assert int(count_pets.text.split()[2]) == len(all_pets)   #проверка что количество совпадает
    assert int(count_pets.text.split()[2]) / 2 <= len(foto_pets)   #проверка что у половины есть фото
    for el in fio_pets:
        fio = el.text.split()
        set_fio.add((fio[0],fio[1],fio[2]))
        set_name.add(fio[0])
        assert len(fio[0]) > 0      #проверка что есть имя
        assert len(fio[1]) > 0      #проверка что есть порода
        assert len(fio[2]) > 0      #проверка что есть возраст
    assert len(set_name) == int(count_pets.text.split()[2])     #проверка что имена у всех уникальные
    assert len(set_fio) == int(count_pets.text.split()[2])      #проверка что фио у всех уникальные

