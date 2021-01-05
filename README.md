# mtgmanager2aetherhub
Populates MTG Manager CSV with Scryfall ID from Aetherhub

This script takes input from a CSV file in the following format:
`"collector_number","extras","language","name","oracle_id","quantity","scryfall_id","set_code","set_name"`

and with a minimum of Name and set_code filled in, searches the Scryfall API, populates the corresponding Scryfall ID and returns an updated CSV.


## To Run
`python scryfall.py`


### Required Libraries
* Python3+
* openpyxl (pip3 install openpyxl)
* requests (pip3 install requests)
* pandas (pip3 install pandas)
* base64 (pip3 install base64)
* selenium (pip3 install selenium)
* webdriver_manager (pip3 install webdriver-manager)

Specify CSV file in the config.py:
csv_file = 'cards-sample.csv'

### Standards
Written using the pep-8 standard

# EXAMPLES
## Search for "Ashes to Ashes" from the "The Dark" set
#### EXAMPLE INPUT
`"","","en","Ashes to Ashes","","2","","DRK",""`

#### API Call
https://api.scryfall.com/cards/search?q=set%3Ddrk%2Bname%3DAshes%20to%20Ashes

#### EXAMPLE OUTPUT
`"","","en","Ashes to Ashes","","2","825496e5-19c7-4f50-8070-0265a58608dc","DRK",""`

## Search for "Ashes to Ashes" from the "4th Edition" set
#### EXAMPLE INPUT
`"","","en","Ashes to Ashes","","2","","4ed",""`

#### API Call
https://api.scryfall.com/cards/search?q=set%3D4ed%2Bname%3DAshes%20to%20Ashes

#### EXAMPLE OUTPUT
`"","","en","Ashes to Ashes","","2","28f40650-9dd5-473d-a660-448672d475a5","4ED",""`

## Search for "Archaeomancer" from the "Commander 2017" set
#### EXAMPLE INPUT
`"","","en","Archaeomancer","","2","","C17",""`

#### API Call
https://api.scryfall.com/cards/search?q=set%3Dc17%2Bname%3DArchaeomancer

#### EXAMPLE OUTPUT
`"","","en","Archaeomancer","","1","4a67be8d-5db6-42c3-8c89-f07bfbd2dd51","C17",""`

# SUPPORTING DOCUMENTATION
Uses the Scryfall Card Search API:
https://scryfall.com/docs/api/cards/search
