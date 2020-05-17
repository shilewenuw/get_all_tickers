import pandas
from enum import Enum

# urls of CSV, from which the tickers will be extracted
_NYSE_URL = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
_NASDAQ_URL = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
_AMEX_URL = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'
_URL_LIST = [_NYSE_URL, _NASDAQ_URL, _AMEX_URL]

class Region(Enum):
    AFRICA = 'AFRICA'
    EUROPE = 'EUROPE'
    ASIA = 'ASIA'
    AUSTRALIA_SOUTH_PACIFIC = 'AUSTRALIA+AND+SOUTH+PACIFIC'
    CARIBBEAN = 'CARIBBEAN'
    SOUTH_AMERICA = 'SOUTH+AMERICA'
    MIDDLE_EAST = 'MIDDLE+EAST'
    NORTH_AMERICA = 'NORTH+AMERICA'


# get tickers from chosen exchanges (default all) as a list
def get_tickers(NYSE=True, NASDAQ=True, AMEX=True):
    tickers_list = []
    if NYSE:
        tickers_list.extend(__url2list(_NYSE_URL))
    if NASDAQ:
        tickers_list.extend(__url2list(_NASDAQ_URL))
    if AMEX:
        tickers_list.extend(__url2list(_AMEX_URL))
    return tickers_list


def get_tickers_filtered(mktcap_min=None, mktcap_max=None):
    tickers_list = []
    for url in _URL_LIST:
        tickers_list.extend(__url2list_filtered(url, mktcap_min=mktcap_min, mktcap_max=mktcap_max))
    return tickers_list


def get_tickers_by_region(region):
    if region in Region:
        return __url2list(f'https://old.nasdaq.com/screening/'
                          f'companies-by-region.aspx?region={region.value}&render=download')
    else:
        raise ValueError('Please enter a valid region (use a Region.REGION as the argument, e.g. Region.AFRICA)')


def __url2list(url):
    df = pandas.read_csv(url)
    # removes weird tickers
    df_filtered = df[~df['Symbol'].str.contains("\.|\^")]
    return df_filtered['Symbol'].tolist()


def __url2list_filtered(url, mktcap_min=None, mktcap_max=None):
    df = pandas.read_csv(url)
    df = df.dropna(subset={'MarketCap'})
    df = df[~df['Symbol'].str.contains("\.|\^")]
    def cust_filter(mkt_cap):
        if 'M' in mkt_cap:
            return float(mkt_cap[1:-1])
        elif 'B' in mkt_cap:
            return float(mkt_cap[1:-1]) * 1000
        else:
            return float(mkt_cap[1:]) / 1e6
    df['MarketCap'] = df['MarketCap'].apply(cust_filter)

    if mktcap_min is not None:
        df = df[df['MarketCap'] > mktcap_min]
    if mktcap_max is not None:
        df = df[df['MarketCap'] < mktcap_max]
    return df['Symbol'].tolist()


# save the tickers to a CSV
def save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv'):
    tickers = get_tickers(NYSE, NASDAQ, AMEX)
    df = pandas.DataFrame(tickers)
    df.to_csv(filename, header=False, index=False)


def save_tickers_by_region(region, filename='tickers_by_region.csv'):
    tickers = get_tickers_by_region(region)
    df = pandas.DataFrame(tickers)
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
    print(filtered_tickers)
