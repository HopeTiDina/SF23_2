import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect_user_rates(user_login, max_pages=5):
    page_num = 1
    data = []

    while page_num <= max_pages:
        url = f'https://letterboxd.com/{user_login}/films/diary/page/{page_num}/'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Не удалось получить страницу {page_num}, код: {response.status_code}')
            break

        soup = BeautifulSoup(response.text, 'lxml')

        entries = soup.find_all('tr', class_='diary-entry-row viewing-poster-container')
        if not entries:
            print('Больше записей не найдено, завершение парсинга.')
            break

        for entry in entries:
            # Название фильма
            film_info = entry.find('div', class_='productiondetails').find('h2', class_='name').find('a')
            film_name = film_info.text.strip()

            # Год выпуска
            year_tag = entry.find('div', class_='productiondetails').find('span', class_='releasedate')
            release_year = year_tag.find('a').text.strip() if year_tag else ''

            # Оценка
            rating_div = entry.find('td', class_='col-rating')
            rating_value = ''
            if rating_div:
                input_tag = rating_div.find('input', class_='rateit-field')
                if input_tag and 'value' in input_tag.attrs:
                    try:
                        rating_value = int(input_tag['value'])
                    except ValueError:
                        rating_value = ''
            print(f'Фильм: {film_name} ({release_year}), Оценка: {rating_value}')

            data.append({
                'Название фильма': film_name,
                'Год выхода': release_year,
                'Оценка': rating_value
            })

        page_num += 1

    return data

# Замените 'rfeldman9' на логин нужного пользователя
user_login = 'rfeldman9'
max_pages = 3  # укажите желаемое количество страниц
film_data = collect_user_rates(user_login, max_pages=max_pages)

# Создаем DataFrame
df = pd.DataFrame(film_data)

# Сохраняем в Excel файл
df.to_excel('letterboxd_films.xlsx', index=False)

print('Данные успешно сохранены в файл letterboxd_films.xlsx')