from time import sleep
import requests
import re
import json
from collections import defaultdict
from bs4 import BeautifulSoup


def find_word_forms(elem):
    rows = elem.findAll('tr')
    top_row = rows.pop(0)
    categories_top = [e.text.strip() for e in top_row.findAll('th')]
    forms_dict = {}
    for row in rows:
        category = row.find('th')
        if category:
            category = category.text.strip()
        word_forms = [e.text.split('\\')[0].strip() for e in row.findAll('td')]
        if len(word_forms) == len(categories_top):
            for category_top, word_form in zip(categories_top, word_forms):
                forms_dict[word_form] = [category_top]
                if category:
                    forms_dict[word_form].append(category)
    return forms_dict


def get_word_translations_dict(soup):
    n_translations = 0
    word_translations = []
    word_form_translations = []
    word_type = None
    forms_dict = None
    for elem in soup.findAll(['div', 'h3', 'table']):
        if elem.name == 'h3':
            if span := elem.find('span', {'class': 'titredef'}):
                if word_form_translations:
                    translation_dict = {
                        'type': word_type,
                        'translations': word_form_translations
                    }
                    if forms_dict:
                        translation_dict['forms'] = forms_dict
                    word_translations.append(translation_dict)
                word_form_translations = []
                forms_dict = None
                word_type = span.text
        elif elem.name == 'table' and 'flextable-fr-mfsp' in elem.get('class', []):
            forms_dict = find_word_forms(elem)
        elif elem.name == 'div' and 'boite' in elem.get('class', []):
            if (nav_head := elem.find('div', {'class': 'NavHead'}))\
                    and (translations_div := elem.find('div', {'class': 'translations'})):
                definition = nav_head.text
                translations_tmp = [line.rsplit('\xa0: ', 1)
                                    for line in translations_div.text.splitlines() if '\xa0' in line]
                definition_translations_dict = defaultdict(list)
                for _, trad in filter(lambda x: len(x) == 2, translations_tmp):
                    n_translations += 1
                    for translation, lang_code in re.findall(r'((?: ?\w+\b)+)\xa0\((\w+)\)', trad):
                        definition_translations_dict[lang_code].append(translation.strip())
                if len(definition_translations_dict) >= 5:
                    translation_dict = {
                        'definition': definition,
                        'translations': definition_translations_dict
                    }
                    word_form_translations.append(translation_dict)
    if word_form_translations:
        translation_dict = {
            'type': word_type,
            'translations': word_form_translations
        }
        if forms_dict:
            translation_dict['forms'] = forms_dict
        word_translations.append(translation_dict)
    return word_translations


def main():
    with open(f'data/scraper_info.json', 'r') as fp:
        scraper_info = json.load(fp)
        last_scrapped_word = scraper_info['last_scrapped_word']
        last_scrapped_page = scraper_info['last_scrapped_page']
    print('last word: ', last_scrapped_word)
    word_page_url = last_scrapped_page
    r = requests.get(word_page_url)
    word_page_soup = BeautifulSoup(r.text, "html.parser")
    translations_dict = {}
    scrap = (last_scrapped_word == '')

    while True:
        words_elem = word_page_soup.find('div', {'id': 'mw-pages'})
        words_elem = words_elem.find('div', {'class': 'mw-category-group'})
        for elem in words_elem.findAll('a'):
            href = elem['href']
            word = elem.text
            with open(f'data/scraper_info.json', 'w') as fp:
                scraper_info['last_word'] = word
                json.dump(scraper_info, fp, indent=4)
            if word.lower() == last_scrapped_word:
                scrap = True
                continue
            if not scrap:
                continue
            url = 'https://fr.wiktionary.org' + href
            try:
                r = requests.get(url)
            except requests.exceptions.ConnectionError:
                sleep(20)
                r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            if word_translations_dict := get_word_translations_dict(soup):
                translations_dict[word] = word_translations_dict
                print(f'[{len(translations_dict):}/100] {word}')
            if len(translations_dict) >= 100:
                first_word, *_, last_word = translations_dict.keys()
                with open(f'data/translations/{first_word[:3]}-{last_word[:3]}.json', 'w') as fp:
                    json.dump(translations_dict, fp, indent=4)
                with open(f'data/scraper_info.json', 'w') as fp:
                    scraper_info['last_scrapped_word'] = last_word.lower()
                    scraper_info['last_scrapped_page'] = word_page_url
                    json.dump(scraper_info, fp, indent=4)
                translations_dict = {}

        for elem in word_page_soup.findAll('a'):
            if elem.text == 'page suivante':
                next_page_href = elem.get('href')
                word_page_url = 'https://fr.wiktionary.org' + next_page_href
                r = requests.get(word_page_url)
                word_page_soup = BeautifulSoup(r.text, "html.parser")
                break


if __name__ == '__main__':
    main()
