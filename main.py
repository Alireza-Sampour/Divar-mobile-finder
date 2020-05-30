import requests
import json
from bs4 import BeautifulSoup
from telegram import Bot, InputMediaPhoto
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from apscheduler.schedulers.blocking import BlockingScheduler

URL = 'https://divar.ir'

bot = Bot('TOKEN')
users = [USERS ID]
sent_messages = []


def check_previous_sent_messages(text):
    with open('previous_messages.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        if text in line.replace('\n', ''):
            return False

    return True


def is_message_in_black_list(description, title):
    with open('black_list.txt', 'r') as file:
        lines = file.readlines()
    if len(lines) == 0:
        return True
    for line in lines:
        print(line.replace('\n', ''))
        if description.strip() in line.replace('\n', '').strip() or title.strip() in line.replace('\n', '').strip():
            return False

    return True


def check_data(link, title, description, price, images, lines, caption):
    for line in lines:
        if json.loads(line)['name'].lower() in title.lower() or json.loads(line)['name'].lower() in description.lower():
            try:
                if float(price) <= float(json.loads(line)['price']):
                    if check_previous_sent_messages(link):
                        if is_message_in_black_list(description, title):
                            if len(images) == 0:
                                for user in users:
                                    bot.send_message(chat_id=user, text=caption, parse_mode='html')
                            else:
                                images[0].caption = caption
                                images[0].parse_mode = 'html'
                                for user in users:
                                    bot.send_media_group(chat_id=user, media=images)
                        sent_messages.append(link)
                        sent_messages.append('\n')
                        return
            except:
                pass


def get_link_content(ad_link, lines):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    print(ad_link)
    response = session.get(ad_link)
    if response.status_code == 200:
        images = []
        soup = BeautifulSoup(response.content, 'lxml')
        title = soup.find('h1', {'class': 'post-header__title'}).text
        description = soup.find('div', {'class': 'post-page__description'}).text
        price = soup.find_all('div', {'class': 'post-fields-item__value'})[-1].text.replace('تومان', '').replace('٫',
                                                                                                                 '').strip()
        real_price = soup.find_all('div', {'class': 'post-fields-item__value'})[-1].text.replace('تومان', '').strip()
        status = soup.find_all('div', {'class': 'post-fields-item__value'})[3].text
        brand = soup.find_all('div', {'class': 'post-fields-item__value'})[2].text
        brand = brand.split('::')[1] if '::' in brand else brand
        text = '<b>' + title + '</b>' + '\n\n' + description + '\n\n' + '<b>' + 'برند :' + '</b>' + ' ' + brand + '\n\n' + '<b>' + 'وضعیت :' + '</b>' + ' ' + status + '\n\n' + '<b>' + 'قیمت :' + '</b>' + ' ' + real_price + ' تومان' + '\n\n' + '<b>' + 'لینک آگهی :' + '</b>' + ' ' + '\n' + ad_link
        for i in range(0, len(soup.find_all('li'))):
            images.append(InputMediaPhoto(media=soup.find_all('li')[i].img['src']))

        check_data(ad_link, title, description, price, images, lines, text)


def delete_previous_messages():
    with open('previous_messages.txt', 'w') as file:
        file.write('')


def main():
    with open('data.json', 'r') as file:
        lines = file.readlines()
    with open('current_city.txt', 'r') as file1:
        city = file1.readlines()
    MOBILE_URL = 'https://divar.ir/s/' + str(city[0].replace('\n', '')) + '/mobile-phones'
    TABLET_URL = 'https://divar.ir/s/' + str(city[0].replace('\n', '')) + '/tablet'
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(MOBILE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        for link in soup.find_all('a', {'class': 'col-xs-12 col-sm-6 col-xl-4 p-tb-large p-lr-gutter post-card'}):
            get_link_content(URL + link['href'], lines)

    response = session.get(TABLET_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        for link in soup.find_all('a', {'class': 'col-xs-12 col-sm-6 col-xl-4 p-tb-large p-lr-gutter post-card'}):
            get_link_content(URL + link['href'], lines)
    global sent_messages
    with open('previous_messages.txt', 'a') as file:
        file.writelines(sent_messages)
    sent_messages.clear()


scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', minutes=10)
scheduler.add_job(delete_previous_messages, 'interval', days=15)
scheduler.start()

