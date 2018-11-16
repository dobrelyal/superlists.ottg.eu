import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest
MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    '''тест нового посетителя'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        '''демонтаж'''
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        '''ожидать строку в таблице списка'''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException ) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        '''тест: можно начать список и получить его позже'''
        #Эдит слышала ро крутое новое приложение со списком
        #неотложных дел Она решает оценить его домашнюю страничку
        #страница снова обновляется и теперь показывает оба элимента ее списка
        self.browser.get(self.live_server_url)

        #она видит что заголовок напоминает ей о списке дел
    #    self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #ее приглашают сделать запись
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
         )

        #
        inputbox.send_keys('Купить павлиньи перья')

        #когда она набирает enter обновляется страница и теперь в списке есть "Купить павлиньи перья"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        #ей предлагается добавить нще один елемент в текстовом поле и она пишет"Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)


        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        #удовлетворенная она снова ложится спать

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''тест многочисленные пользователи могут начать списки по разным url '''
        #Эдит начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        #Она замечает что ее список имеет уникальный url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Теперь новый пользователь Фрэнсис приходит на сайт

        ##Мы используем новый сеанс браузера тем самым обеспечивая чтобы
        ##никакая информация  от Эдит не прошла через даные cookie
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Фрэнсис посещает домашнюю страницу  нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(' Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        #Фрэнсис начинает новый список вводя новый элемет он менее интересен чем список Эдит
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        #Френсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #Опять таки нет ни следа от списка Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(' Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

        #Удовлетворенные они оба ложаться спать


    def test_layout_and_styling(self):
        '''тест макета и стилевого оформления'''
        #Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        #Она замечает что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        #Она начинает новый список и видит что поле ввода там
        #тоже оккуратно центрировано
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
