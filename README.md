# get-all-tickers

I couldn't find any libraries to retrieve all the tickers of publicly traded stocks, so I decided to make my own library that could do this. The stock tickers are from the NYSE, NASDAQ, and AMEX. Support has been added for global tickers.  
Note: NASDAQ implemented anti-scraping features, requiring version 1.7 to incorporate changes to get around the anti-scraping mechanism, but as a result, get-all-tickers no longer works in Google Colab.
## features
-  getting a list of tickers from chosen US exchanges (all of them by default)
-  getting a list of tickers filtered by market caps and sectors
-  getting the top n biggest tickers, optionally by a given sector
-  getting tickers from any region of the world
-  saving tickers to a CSV

### install
Use the following pip command:
```
pip install get-all-tickers
```
## methods & classes
```python
get_tickers(NYSE=True, NASDAQ=True, AMEX=True)
```
Returns a list of tickers, set an exchange to false to exclude.
***
```python
get_tickers_filtered(mktcap_min=None, mktcap_max=None, sectors=None)
```
Returns a list of tickers with given filters (so far filters market cap only, feel free to give suggestions).
Minimum and maximum market caps are set through mktcap_min and mktcap_max, respectively (numbers are in millions).
You can have no upper bound for market cap if you leave mktcap_max as its default value, so `get_tickers_filtered(mktcap_min=200)` will
get tickers of market caps 200 million and up. Likewise, not setting mktcap_min will get tickers with market caps from $0 to mktcap_max. Support has been added for sectors, enter a list of SectorConstants.DESIRED_SECTOR. For example, `get_tickers_filtered(sectors=SectorConstants.FINANCE` would get finance companies.
***
```python
def get_biggest_n_tickers(top_n, sectors=None)
```
Returns a list of top_n biggest tickers by market cap. You can specify what sectors you how you would the previous method.
```python
Region.DESIRED_REGION_HERE
```
Region constants include: AFRICA, EUROPE, ASIA, AUSTRALIA_SOUTH_PACIFIC, CARIBBEAN, SOUTH_AMERICA, MIDDLE_EAST, NORTH_AMERICA. Regions are used as arguments for region specific methods.  
***
```python
get_tickers_by_region(region)
```
Use a Region constant (e.g Region.EUROPE) as the argument. Returns a list of tickers in specified region. 
***
```python
save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv')
```
Set any exchange to False if you don't want to include it. Saves tickers to a csv file.  
***
```python
save_tickers_by_region(region, filename='tickers_by_region.csv')
```
Use a Region constant (e.g Region.EUROPE) as the argument. Saves tickers in specified region to csv  

### examples
```python
from get_all_tickers import get_tickers as gt
from get_all_tickers.get_tickers import Region
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
tickers_asia = gt.get_tickers_by_region(Region.ASIA)
print(tickers_asia[:5])

# save tickers from Europe
gt.save_tickers_by_region(Region.EUROPE, filename='EU_tickers.csv')

# get tickers filtered by market cap (in millions)
filtered_tickers = gt.get_tickers_filtered(mktcap_min=500, mktcap_max=2000)
print(filtered_tickers[:5])

# not setting max will get stocks with $2000 million market cap and up.
filtered_tickers = gt.get_tickers_filtered(mktcap_min=2000)
print(filtered_tickers[:5])

# get tickers filtered by sector
filtered_by_sector = gt.get_tickers_filtered(mktcap_min=200e3, sectors=SectorConstants.FINANCE)
print(filtered_by_sector[:5])

# get tickers of 5 largest companies by market cap (specify sectors=SECTOR)
top_5 = gt.get_biggest_n_tickers(5)
print(top_5)
```
