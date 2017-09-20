def date_to_number(key):

    trans = {
        'months_abbrev': {
            'січ': '1',
            'лют': '2',
            'бер': '3',
            'кві': '4',
            'тра': '5',
            'чер': '6',
            'лип': '7',
            'сер': '8',
            'вер': '9',
            'жов': '10',
            'лис': '11',
            'гру': '12',
            'квіт': '4',
            'трав': '5',
            'черв': '6',
            'серп': '8',
            'жовт': '10',
            'лист': '11',
            'груд': '12',
            'янв': '1',
            'фев': '2',
            'мар': '3',
            'апр': '4',
            'май': '5',
            'июн': '6',
            'июл': '7',
            'авг': '8',
            'сен': '9',
            'окт': '10',
            'ноя': '11',
            'дек': '12',
        },
    }
    #print('date_to_number result: {}'.format(key))
    return trans['months_abbrev'][key.lower()]

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
