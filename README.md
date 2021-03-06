# Find Hero Matchups from OPENDOTA (https://www.opendota.com)
This script queries OPENDOTA for matches with a given hero matchup.

# Dependencies
* [requests](https://requests.readthedocs.io/en/latest/user/install/#install) 

# How To Run
1. `git clone https://github.com/daniel-bencic/dota2-matchups.git`
2. `cd dota2-matchups`
3. `python dota2-matchups.py -h`

## List Hero IDs
`python list-heroes.py`

## Query Matchup
The following command searches for Lina vs Monkey King matchups on the midlane:\
`python dota2-matchups.py 25 114 2 2`

![demo](doc/demo.png)
