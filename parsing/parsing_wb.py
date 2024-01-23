import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


class ParsingWB:
    def __init__(self, url):
        '''Проверка ссылки, есть ли размер у товара'''
        if len(self.get_id_product(url)) == 2:
            self.id_product = self.get_id_product(url)[0]
            self.id_size = int(self.get_id_product(url)[1])
        else:
            self.id_product = self.get_id_product(url)
        self.url = url

    @staticmethod
    def get_id_product(url: str):
        '''Функция достает id продукта и id размера'''
        return url.split('/')[-2], url.split('=')[-1] if 'size=' in url else url.split('/')[-2]

    def get_data(self):
        '''Функция достает все данные товара'''
        data = {}
        response = requests.get(f'https://card.wb.ru/cards/v1/detail?dest=-1257786&nm={self.id_product}').json()
        for i_data in response['data']['products']:
            data['Артикул'] = i_data.get('id')
            data['Бренд'] = i_data.get('brand')
            data['Имя товара'] = i_data.get('name')
            data['Рейтинг'] = i_data.get('reviewRating')

            # print(i_data)
            # print('id размера: ', self.id_size)
            # print('id: ', i_data['id'])
            # print('Бренд: ', i_data['brand'])
            # print('Имя товара: ', i_data['name'])
            # print('Рейтинг: ', i_data['reviewRating'])

            count = 0
            price = 0

            for i_sizes in i_data['sizes']:
                if i_sizes.get('optionId') == self.id_size:
                    count += sum([o['qty'] for o in i_sizes['stocks']])
                    data['Размер'] = i_sizes.get('name')
                    if not i_sizes.get('salePriceU'):
                        price += i_data.get('salePriceU') // 100
                    else:
                        price += i_sizes.get('salePriceU') // 100
                else:
                    if i_sizes.get('name') == '':
                        price += i_data.get('salePriceU') // 100
                        count += sum([o['qty'] for o in i_sizes['stocks']])

            data['Цена'] = price
            data['Количество'] = count

            # print(f'Цена: {price}')
            # print(f'Количество: {count}')
        return data

    def get_photo_product(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(self.url)
        sleep(1)
        class_photo = browser.find_element(By.CLASS_NAME, 'zoom-image-container')
        class_img = class_photo.find_element(By.XPATH, '//*[@id="imageContainer"]/div/div/img')
        src = class_img.get_attribute('src')
        return src
