import json
import re

import bs4


def slush_pool_parce(some_bs4: bs4.element.Tag) -> ([str]):
    luck = []
    source_info = some_bs4.findAll('div', attrs={'class': 'k9b4LwhQ Tl31gjJs KOYJ53Ig IZBfxUDD e8NRYYLn'},
                                   recursive=True)
    for source in source_info:
        luck_info = ''
        percentil_info = source.find('div', attrs={'class': 'gQ2kNUeS Tl31gjJs KOYJ53Ig gJkPryAP'})
        percent_info = source.find('div', attrs={'class': '_ErQDvbQ Tl31gjJs KOYJ53Ig gJkPryAP'})
        if percentil_info:
            luck_info += percentil_info.find('span').text
            luck_info += ':'
        if percent_info:
            percent = re.findall(r'[\d\.]+', source.find('span', attrs={'data-role': 'value'}).text)[0]
            luck_info += percent
            luck_info += '%'
        if luck_info != '':
            luck.append(luck_info)

    return luck


def miningpoolhub_parce(some_bs4: bs4.element.Tag) -> ([str]):
    luck = []
    source_info = some_bs4.findAll('article', attrs={'class': 'module width_full'}, recursive=False)

    block_overview = source_info[1]
    overview_table = block_overview.find('table')
    overview_tbody = overview_table.find('tbody')
    table_content = overview_tbody.findAll('tr')
    for row in table_content:
        description = row.find('th').text.rstrip()
        values = row.findAll('td')
        value = values[7].text.rstrip().lstrip()
        luck_info = description + ': ' + value
        luck.append(luck_info)
    return luck


def two_miners(some_bs4: bs4.element.Tag) -> ([str]):
    luck = []
    source_info = some_bs4.findAll('div', attrs={'class': 'mining-list__item pool-card'}, recursive=False)
    for card in source_info:
        title = card.find('div', attrs={'class': 'pool-name'}, recursive=True).text
        pool_options = card.findAll('div', attrs={'class': 'pool-options__item'}, recursive=True)
        value = pool_options[1].find('div', attrs={'class': 'pool-options__val'}).text
        luck_info = title + ': ' + value
        luck.append(luck_info)
    return luck


LUCK_POOL_CHECKS = [
    {
        'name': 'SlushPool',
        'url': 'https://slushpool.com/ru/stats/btc/',
        'coin': 'BTC',
        'indicating_load_class': 'app',
        'filter_func': slush_pool_parce,
        'structure': [
            {
                'tag': 'section',
                'attr': {
                    'class': 'nPw6h2yK zfQnwI6U B04mJW0I',
                },
            },
            {
                'tag': 'div',
                'attr': {
                    'class': 'QS4bCW1U',
                },
            },
        ],
    },
    # {
    #     'name': 'MiningPoolHub',
    #     'url': 'https://ethereum.miningpoolhub.com/index.php?page=statistics&action=blocks',
    #     'coin': 'ETH',
    #     'indicating_load_class': 'main',
    #     'filter_func': miningpoolhub_parce,
    #     'structure': [
    #         {
    #             'tag': 'section',
    #             'attr': {
    #                 'id': 'main',
    #             },
    #         },
    #     ],
    # },
    # {
    #     'name': 'MiningPoolHub',
    #     'url': 'https://bitcoin-gold.miningpoolhub.com/index.php?page=statistics&action=blocks',
    #     'coin': 'BTG',
    #     'indicating_load_class': 'main',
    #     'filter_func': miningpoolhub_parce,
    #     'structure': [
    #         {
    #             'tag': 'section',
    #             'attr': {
    #                 'id': 'main',
    #             },
    #         },
    #     ],
    # },
    # {
    #     'name': '2miners',
    #     'url': 'https://2miners.com/',
    #     'coin': '',
    #     'indicating_load_class': 'mining-list-pplns',
    #     'filter_func': two_miners,
    #     'structure': [
    #         {
    #             'tag': 'div',
    #             'attr': {
    #                 'class': 'mining-list',
    #             },
    #         },
    #     ],
    # },
]
