import pandas


# urls of CSV, from which the tickers will be extracted
NYSE_URL = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
NASDAQ_URL = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
AMEX_URL = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'


# get tickers from chosen exchanges (default all) as a list
def get_tickers(NYSE=True, NASDAQ=True, AMEX=True):
    tickers_list = []
    if NYSE:
        tickers_list.extend(__url2list(NYSE_URL))
    if NASDAQ:
        tickers_list.extend(__url2list(NASDAQ_URL))
    if AMEX:
        tickers_list.extend(__url2list(AMEX_URL))
    return tickers_list


def __url2list(url):
    df = pandas.read_csv(url)
    df_filtered = df[~df['Symbol'].str.contains("\.|\^")]
    return df_filtered['Symbol'].tolist()


# save the tickers to a CSV
def save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv'):
    tickers = get_tickers(NYSE, NASDAQ, AMEX)
    df = pandas.DataFrame(tickers)
    df.to_csv(filename, index=False)


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
