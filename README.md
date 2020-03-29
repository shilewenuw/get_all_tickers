# get-all-tickers

I couldn't find any libraries to retrieve all the tickers of publicly traded stocks, so I decided to make my own library that could do this. The stock tickers are from the NYSE, NASDAQ, and AMEX.

## features
-  getting a list of tickers from chosen exchanges (all of them by default)
-  saving a list of tickers from chosen exchanges as a CSV
-  (planned) getting a list of tickers with different criteria (such as Market Cap, P/E)

### install
Use the following pip command:
```
pip install get-all-tickers
```
## methods & classes
```
get_tickers(NYSE=True, NASDAQ=True, AMEX=True)
```
Returns a list of tickers, set an exchange to false to exclude.

```
Region.DESIRED_REGION_HERE
```
Region constants include: AFRICA, EUROPE, ASIA, AUSTRALIA_SOUTH_PACIFIC, CARIBBEAN, SOUTH_AMERICA, MIDDLE_EAST, NORTH_AMERICA. Regions are used as arguments for region specific methods.

```
get_tickers_by_region(region)
```
Use a Region constant (e.g Region.EUROPE) as the argument. Returns a list of tickers in specified region.

```
save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv')
```
Set any exchange to False if you don't want to include it. Saves tickers to a csv file.

```
save_tickers_by_region(region, filename='tickers_by_region.csv')
```
Use a Region constant (e.g Region.EUROPE) as the argument. Saves tickers in specified region to csv

### examples
```
from get_all_tickers import get_tickers as gt
# tickers of all exchanges
tickers = gt.get_tickers()
print(tickers[:5])

# tickers from NYSE and NASDAQ only
tickers = gt.get_tickers(AMEX=False)

# default filename is tickers.csv, to specify, add argument filename='yourfilename.csv'
gt.save_tickers()

# save tickers from NYSE and AMEX only
gt.save_tickers(NASDAQ=False)

# get tickers from Asia
tickers_asia = get_tickers_by_region(Region.ASIA)
print(tickers_asia[:5])

# save tickers from Europe
save_tickers_by_region(Region.EUROPE, filename='EU_tickers.csv')
```
