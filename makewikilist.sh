#!/bin/bash

rm -f [1-9]* *.txt *.yml

EUPATH=$HOME/.steam/steam/SteamApps/common/Europa\ Universalis\ IV

cp "$EUPATH"/localisation/*_english.yml .
cp "$EUPATH"/map/default.map .
cp "$EUPATH"/map/continent.txt .
cp "$EUPATH"/map/region.txt .
cp "$EUPATH"/history/provinces/* .
cp "$EUPATH"/common/tradenodes/00_tradenodes.txt .

rename "s/[-\s].*//g" [1-9]*

echo "" > localisation.txt
for file in $(ls *.yml); do cat $file >> localisation.txt; echo "" >> localisation.txt; done

grep 'PROV[1-9][0-9]*:' *.yml | sed 's/.*yml://g' > prov_names.txt

python3 makewikilist.py

for file in $(ls *.wiki); do sed 's/Naval\ Supplies/Naval\ supplies/' -i $file; done
