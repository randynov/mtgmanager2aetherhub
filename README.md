# mtgmanager2aetherhub
Populates MTG Manager CSV with Scryfall ID from Aetherhub

This script takes input from a CSV file in the following format:
`"collector_number","extras","language","name","oracle_id","quantity","scryfall_id","set_code","set_name"`

and with a minimum of Name and set_code filled in, searches the Scryfall API, populates the corresponding Scryfall ID and returns an updated CSV.

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
