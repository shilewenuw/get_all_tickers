# get-all-tickers

I couldn't find any libraries to retrieve all the tickers of publicly traded stocks, so I decided to make my own library that could do this. The stock tickers are from the NYSE, NASDAQ, and the AMEX.

## features
-  getting a list of tickers from chosen exchanges (all of them by default)
-  saving a list of tickers from chosen exchanges as a CSV

### install
Use the following pip command:
```
pip install get_all_tickers
```
### examples
```
# tickers of all exchanges
tickers = get_tickers()
print(tickers[:5])

# tickers from NYSE and NASDAQ only
tickers = get_tickers(AMEX=False)

# default filename is tickers.csv, to specify, add argument filename='yourfilename.csv'
save_tickers()

# save tickers from NYSE and AMEX only
save_tickers(NASDAQ=False)
```
