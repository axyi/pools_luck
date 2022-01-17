import fcntl
import os
import sys
import uuid
from time import sleep

import requests
import logging
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from connections import TELEGRAM_API
from resources import LUCK_POOL_CHECKS

IMPLICITLY = 5
LOG_LEVEL = 'DEBUG'


class LuckInfo:
    """
    Класс определяет свойства сьруктуру удачи при поиске блока для пула
    """
    pool_name = str
    pool_link = str
    coin = str
    luck_info = [str]

    def __init__(self, pool_name: str, pool_link: str, coin: str, luck_info: [str]):
        self.pool_name = pool_name
        self.pool_link = pool_link
        self.coin = coin
        self.luck_info = luck_info

    def __repr__(self):
        return str(self.__dict__)

    def send_alert(self):
        """
        Отправка информации об удаче на пуле
        :return:
        """
        if len(self.luck_info) < 1:
            return

        message = 'На пуле [{}]({}) '.format(self.pool_name, self.pool_link)
        if self.coin and self.coin != '':
            message += 'удача для монеты **{}**:'.format(self.coin)
        else:
            message += 'удача'

        for val in self.luck_info:
            message += '\n```\n'
            message += val
            message += '```'
        send_telegram_message(message)


def send_telegram_message(message: str):
    """
    Отправляем сообщение в телеграм
    :param message: Отправленное сообщение
    :return: Результат отправки сообщения
    """
    u = TELEGRAM_API['base_url'] + 'bot' + TELEGRAM_API['token'] + '/sendMessage'
    data = {
        'chat_id': TELEGRAM_API['chat_id'],
        'text': message,
        'parse_mode': 'MarkdownV2',
        'disable_web_page_preview': True,

    }
    try:
        requests.post(
            u,
            json=data,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )
    except Exception as error:
        logger.error("Ошибка при отправке сообщения в Телеграм: {}".format(error))
    logger.info("Сообщение в телеграм успешно отправлено")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    session_id = str(uuid.uuid4())

    logger = logging.getLogger("get_luck")
    logger.setLevel(LOG_LEVEL)

    ch = logging.StreamHandler()
    ch_format = logging.Formatter("%(asctime)s [%(levelname)s][" + session_id + "] %(message)s", "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(ch_format)
    ch_loglevel = logging.getLevelName(LOG_LEVEL)
    ch.setLevel(ch_loglevel)
    logger.addHandler(ch)

    fp = open(os.path.realpath(__file__), 'r')
    try:
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        logger.warning("Попытка повторного запуска скрипта")
        sys.exit(0)

    ratings = []

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--profile-directory=Profile")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    for key, pool in enumerate(LUCK_POOL_CHECKS):
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                   options=chrome_options)
        try:
            browser.delete_all_cookies()
            # Валидация параметров
            if 'name' not in pool:
                logger.warning('name - is required param in {}'.format(key))
                continue

            if 'coin' not in pool:
                logger.warning('coin - is required param in {}'.format(pool['name']))
                continue

            if 'coin' not in pool:
                logger.warning('coin - is required param in {}'.format(pool['name']))
                continue

            url = pool['url']
            coin = pool['coin']
            name = pool['name']
            # Основной цикл проверки
            logger.info('Запускаем проверку для {}'.format(name))
            try:
                browser.implicitly_wait(IMPLICITLY)
                browser.get(url)
            except Exception as e:
                message = 'Ресурс недоступен: {}: {}'.format(url, e)
                send_telegram_message(message)
                logger.warning(message)
                continue

            try:
                myElem = WebDriverWait(browser, IMPLICITLY) \
                    .until(expected_conditions
                           .presence_of_element_located((By.ID,
                                                         pool[
                                                             'indicating_load_class'])))
                sleep(2)
            except TimeoutException:
                message = 'Загрузка превысила таймаут ожидания: {}'.format(url)
                send_telegram_message(message)
                logger.warning(message)
                continue

            response = browser.page_source
            source_soup = BeautifulSoup(response, 'html.parser')
            soup = source_soup.find('html', attrs={}, recursive=False)
            soup = soup.find('body', attrs={}, recursive=False)

            success = True
            for idx, element in enumerate(pool['structure']):
                try:
                    soup = soup.find(element['tag'], attrs=element['attr'], recursive=True)
                except AttributeError:
                    success = False
                    message = 'Не удалось найти атрибут №{} - {} на ресурсе: {}'.format(idx, element, url)
                    send_telegram_message(message)
                    logger.warning(message)
                    break
            if not success:
                continue

            luck_soup = soup
            try:
                luck_desc = pool['filter_func'](luck_soup)
                luck = LuckInfo(name, url, coin, luck_desc)
                logger.info("Успешно получена информация: {}".format(luck))
                luck.send_alert()
            except Exception as e:
                message = 'Не удалось получить информацию об удаче с ресурса {}. Error:'.format(name, e)
                send_telegram_message(message)
                logger.warning(message)
        except Exception as e:
            message = 'Ошибка при выполнении основного цикла проверки пула {}: {}'.format(name, e)
            send_telegram_message(message)
            logger.error(message)
        finally:
            browser.close()
