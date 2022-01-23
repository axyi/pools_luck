import re
import datetime
import bs4


def slush_pool_parce(some_bs4: bs4.element.Tag) -> ([str]):
    luck = []
    send = False
    source_last_block_block = some_bs4.find('section',
                                            attrs={'class': 'nPw6h2yK zfQnwI6U xlaKWi82'},
                                            recursive=True)

    source_last_block_context = source_last_block_block.find('div',
                                                             attrs={'class': 'QS4bCW1U'},
                                                             recursive=True)
    source_last_block_time = source_last_block_context.find('div',
                                                            attrs={
                                                                'class': '_ErQDvbQ Tl31gjJs KOYJ53Ig gJkPryAP B04mJW0I'},
                                                            recursive=True)

    source_last_block_hour = source_last_block_time.find('span',
                                                         attrs={'data-role': 'hours'},
                                                         recursive=True)
    source_last_block_hour_nums = source_last_block_hour.findAll('span',
                                                                 attrs={'class': 'X8Buifb5'},
                                                                 recursive=True)
    source_last_block_minute = source_last_block_time.find('span',
                                                           attrs={'data-role': 'minutes'},
                                                           recursive=True)
    source_last_block_minute_nums = source_last_block_minute.findAll('span',
                                                                     attrs={'class': 'X8Buifb5'},
                                                                     recursive=True)

    source_last_block_second = source_last_block_time.find('span',
                                                           attrs={'data-role': 'seconds'},
                                                           recursive=True)
    source_last_block_second_nums = source_last_block_second.findAll('span',
                                                                     attrs={'class': 'X8Buifb5'},
                                                                     recursive=True)
    current_block_hours = ''
    for hour_nums in source_last_block_hour_nums:
        current_block_hours += hour_nums.text

    current_block_minutes = ''
    for minute_nums in source_last_block_minute_nums:
        current_block_minutes += minute_nums.text

    current_block_seconds = ''
    for second_nums in source_last_block_second_nums:
        current_block_seconds += second_nums.text

    delta_last_block = datetime.timedelta(hours=int(current_block_hours),
                                          minutes=int(current_block_minutes),
                                          seconds=int(current_block_seconds))
    last_block_info = 'Длительность раунда: {}'.format(delta_last_block)
    luck.append(last_block_info)

    source_luck_block = some_bs4.find('section',
                                      attrs={'class': 'nPw6h2yK zfQnwI6U B04mJW0I'},
                                      recursive=True)

    source_luck_context = source_luck_block.find('div',
                                                 attrs={'class': 'QS4bCW1U'},
                                                 recursive=True)
    source_luck_info = source_luck_context.findAll('div',
                                                   attrs={'class': 'k9b4LwhQ Tl31gjJs KOYJ53Ig IZBfxUDD e8NRYYLn'},
                                                   recursive=True)
    percent_last10blocks = 0.0
    percent_last50blocks = 0.0
    percent_last250blocks = 0.0
    for source in source_luck_info:
        luck_info = ''
        percentil_info = source.find('div', attrs={'class': 'gQ2kNUeS Tl31gjJs KOYJ53Ig gJkPryAP'})
        percent_info = source.find('div', attrs={'class': '_ErQDvbQ Tl31gjJs KOYJ53Ig gJkPryAP'})
        if percentil_info:
            luck_info += percentil_info.find('span').text
            luck_info += ': '
        if percent_info:
            percent = re.findall(r'[\d\.]+', source.find('span', attrs={'data-role': 'value'}).text)[0]
            blocks_num = re.findall(r'[\d\.]+', percentil_info.find('span').text)[0]
            if int(blocks_num) == 10:
                percent_last10blocks = float(percent)
            if int(blocks_num) == 50:
                percent_last50blocks = float(percent)
            if int(blocks_num) == 250:
                percent_last250blocks = float(percent)
            luck_info += percent
            luck_info += '%'
        if luck_info != '':
            luck.append(luck_info)

    # Референсные значения
    delta20min = datetime.timedelta(minutes=20)
    delta9hour = datetime.timedelta(hours=9)
    ref_last10blocks = 50.0
    ref_last50blocks = 75.0
    ref_last250blocks = 90.0

    # Условия отправки уведомлений
    if delta_last_block < delta20min:
        send = True

    if delta_last_block > delta9hour:
        send = True

    if percent_last10blocks < ref_last10blocks:
        send = True

    if percent_last50blocks < ref_last50blocks:
        send = True

    if percent_last250blocks < ref_last250blocks:
        send = True

    # print(luck)
    # print(delta_last_block)
    # print(percent_last10blocks)
    # print(percent_last50blocks)
    # print(percent_last250blocks)

    return luck, send


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


def baikalmine_parce(some_bs4: bs4.element.Tag) -> ([str]):
    luck = []
    source_info = some_bs4.find('ul', attrs={'class': 'list-group list-group-flush text-center'}, recursive=True)
    rows = source_info.findAll('li')
    luck_desc = rows[0].findAll('span')
    title = luck_desc[0].text.rstrip().lstrip()
    value = luck_desc[1].text.rstrip().lstrip()
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
            # {
            #     'tag': 'section',
            #     'attr': {
            #         'class': 'nPw6h2yK zfQnwI6U B04mJW0I',
            #     },
            # },
            # {
            #     'tag': 'div',
            #     'attr': {
            #         'class': 'QS4bCW1U',
            #     },
            # },
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
    #     'name': 'BaikalMine',
    #     'url': 'https://baikalmine.com/pools/pplns/clo/blocks',
    #     'coin': 'CLO',
    #     'filter_func': baikalmine_parce,
    #     'structure': [
    #         {
    #             'tag': 'bm-blocks-pools',
    #             'attr': {},
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
