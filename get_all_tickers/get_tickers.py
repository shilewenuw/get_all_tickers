import pandas as pd
from enum import Enum
import io
import requests

_EXCHANGE_LIST = ['nyse', 'nasdaq', 'amex']

_SECTORS_LIST = set(['Consumer Non-Durables', 'Capital Goods', 'Health Care',
       'Energy', 'Technology', 'Basic Industries', 'Finance',
       'Consumer Services', 'Public Utilities', 'Miscellaneous',
       'Consumer Durables', 'Transportation'])


# headers and params used to bypass NASDAQ's anti-scraping mechanism in function __exchange2df
headers = {
    'authority': 'api.nasdaq.com',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'origin': 'https://www.nasdaq.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.nasdaq.com/',
    'accept-language': 'en-US,en;q=0.9',
}

def params(exchange):
    return (
        ('letter', '0'),
        ('exchange', exchange),
        ('download', 'true'),
    )

def params_region(region):
    return (
        ('letter', '0'),
        ('region', region),
        ('download', 'true'),
    )

# I know it's weird to have Sectors as constants, yet the Regions as enums, but
# it makes the most sense to me
class Region(Enum):
    AFRICA = 'AFRICA'
    EUROPE = 'EUROPE'
    ASIA = 'ASIA'
    AUSTRALIA_SOUTH_PACIFIC = 'AUSTRALIA+AND+SOUTH+PACIFIC'
    CARIBBEAN = 'CARIBBEAN'
    SOUTH_AMERICA = 'SOUTH+AMERICA'
    MIDDLE_EAST = 'MIDDLE+EAST'
    NORTH_AMERICA = 'NORTH+AMERICA'

class SectorConstants:
    NON_DURABLE_GOODS = 'Consumer Non-Durables'
    CAPITAL_GOODS = 'Capital Goods'
    HEALTH_CARE = 'Health Care'
    ENERGY = 'Energy'
    TECH = 'Technology'
    BASICS = 'Basic Industries'
    FINANCE = 'Finance'
    SERVICES = 'Consumer Services'
    UTILITIES = 'Public Utilities'
    DURABLE_GOODS = 'Consumer Durables'
    TRANSPORT = 'Transportation'


# get tickers from chosen exchanges (default all) as a list
def get_tickers(NYSE=True, NASDAQ=True, AMEX=True):
    tickers_list = []
    if NYSE:
        tickers_list.extend(__exchange2list('nyse'))
    if NASDAQ:
        tickers_list.extend(__exchange2list('nasdaq'))
    if AMEX:
        tickers_list.extend(__exchange2list('amex'))
    return tickers_list


def get_tickers_filtered(mktcap_min=None, mktcap_max=None, sectors=None):
    tickers_list = []
    for exchange in _EXCHANGE_LIST:
        tickers_list.extend(__exchange2list_filtered(exchange, mktcap_min=mktcap_min, mktcap_max=mktcap_max, sectors=sectors))
    return tickers_list


def get_biggest_n_tickers(top_n, sectors=None):
    df = pd.DataFrame()
    for exchange in _EXCHANGE_LIST:
        temp = __exchange2df(exchange)
        df = pd.concat([df, temp])
        
    df = df.dropna(subset={'marketCap'})
    df = df[~df['symbol'].str.contains("\.|\^")]

    if sectors is not None:
        if isinstance(sectors, str):
            sectors = [sectors]
        if not _SECTORS_LIST.issuperset(set(sectors)):
            raise ValueError('Some sectors included are invalid')
        sector_filter = df['Sector'].apply(lambda x: x in sectors)
        df = df[sector_filter]

    def cust_filter(mkt_cap):
        if 'M' in mkt_cap:
            return float(mkt_cap[1:-1])
        elif 'B' in mkt_cap:
            return float(mkt_cap[1:-1]) * 1000
        else:
            return float(mkt_cap[1:]) / 1e6
    df['marketCap'] = df['marketCap'].apply(cust_filter)

    df = df.sort_values('marketCap', ascending=False)
    if top_n > len(df):
        raise ValueError('Not enough companies, please specify a smaller top_n')

    return df.iloc[:top_n]['symbol'].tolist()


def get_tickers_by_region(region):
    if region in Region:
        response = requests.get('https://old.nasdaq.com/screening/companies-by-name.aspx', headers=headers,
                                params=params_region(region))
        data = io.StringIO(response.text)
        df = pd.read_csv(data, sep=",")
        return __exchange2list(df)
    else:
        raise ValueError('Please enter a valid region (use a Region.REGION as the argument, e.g. Region.AFRICA)')

def __exchange2df(exchange):
    r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params(exchange))
    data = r.json()['data']
    df = pd.DataFrame(data['rows'], columns=data['headers'])
    return df

def __exchange2list(exchange):
    df = __exchange2df(exchange)
    # removes weird tickers
    df_filtered = df[~df['symbol'].str.contains("\.|\^")]
    return df_filtered['symbol'].tolist()

# market caps are in millions
def __exchange2list_filtered(exchange, mktcap_min=None, mktcap_max=None, sectors=None):
    df = __exchange2df(exchange)
    df = df.dropna(subset={'marketCap'})
    df = df[~df['symbol'].str.contains("\.|\^")]

    if sectors is not None:
        if isinstance(sectors, str):
            sectors = [sectors]
        if not _SECTORS_LIST.issuperset(set(sectors)):
            raise ValueError('Some sectors included are invalid')
        sector_filter = df['sector'].apply(lambda x: x in sectors)
        df = df[sector_filter]

    def cust_filter(mkt_cap):
        if 'M' in mkt_cap:
            return float(mkt_cap[1:-1])
        elif 'B' in mkt_cap:
            return float(mkt_cap[1:-1]) * 1000
        elif mkt_cap == '':
            return 0.0
        else:
            return float(mkt_cap[1:]) / 1e6
    df['marketCap'] = df['marketCap'].apply(cust_filter)
    if mktcap_min is not None:
        df = df[df['marketCap'] > mktcap_min]
    if mktcap_max is not None:
        df = df[df['marketCap'] < mktcap_max]
    return df['symbol'].tolist()


# save the tickers to a CSV
def save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv'):
    tickers2save = get_tickers(NYSE, NASDAQ, AMEX)
    df = pd.DataFrame(tickers2save)
    df.to_csv(filename, header=False, index=False)

def save_tickers_by_region(region, filename='tickers_by_region.csv'):
    tickers2save = get_tickers_by_region(region)
    df = pd.DataFrame(tickers2save)
    df.to_csv(filename, header=False, index=False)


if __name__ == '__main__':

    # tickers of all exchanges
    tickers = get_tickers()
    print(tickers[:5])

    # tickers from NYSE and NASDAQ only
    tickers = get_tickers(AMEX=False)

    # default filename is tickers.csv, to specify, add argument filename='yourfilename.csv'
    save_tickers()

    # save tickers from NYSE and AMEX only
    save_tickers(NASDAQ=False)

    # get tickers from Asia
    tickers_asia = get_tickers_by_region(Region.ASIA)
    print(tickers_asia[:5])

    # save tickers from Europe
    save_tickers_by_region(Region.EUROPE, filename='EU_tickers.csv')

    # get tickers filtered by market cap (in millions)
    filtered_tickers = get_tickers_filtered(mktcap_min=500, mktcap_max=2000)
    print(filtered_tickers[:5])

    # not setting max will get stocks with $2000 million market cap and up.
    filtered_tickers = get_tickers_filtered(mktcap_min=2000)
    print(filtered_tickers[:5])

    # get tickers filtered by sector
    filtered_by_sector = get_tickers_filtered(mktcap_min=200e3, sectors=SectorConstants.FINANCE)
    print(filtered_by_sector[:5])

    # get tickers of 5 largest companies by market cap (specify sectors=SECTOR)
    top_5 = get_biggest_n_tickers(5)
    print(top_5)

