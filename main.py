import csv
import requests
from bs4 import BeautifulSoup

with open('table.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['author', 'a_ref', 'title', 'ref', 'tag', 'time'])

    for i in range(1, 10):
        data = requests.get(
            'https://habr.com/ru/search/page' + str(i) + '/?q=web-scraping&target_type=posts&order=relevance')
        if data.status_code == 200:
            page = data.content.decode('utf-8')
            data_bs = BeautifulSoup(page, 'html.parser')
            blocks = data_bs.find_all('div', {'class':'tm-article-snippet'})
            for block in blocks:
                block_author = block.find('a', {'class': 'tm-user-info__username'})
                block_time = block.find('span', {'class': 'tm-article-snippet__datetime-published'})
                block_title = block.find('a', {'class':'tm-article-snippet__title-link'})
                block_tags = block.find_all('a', {'class':'tm-article-snippet__hubs-item-link'})

                tmp_tag = ''
                for tag in block_tags:
                    tmp_tag += '{}, '.format(tag.get_text())

                writer.writerow([block_author.get_text().strip(),
                'https://habr.com{}'.format(block_author.get('href')),                               
                block_title.get_text(),
                'https://habr.com{}'.format(block_title.get('href')),
                tmp_tag,
                block_time.get_text()])
        else:
            break