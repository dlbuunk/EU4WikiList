#!/bin/bash

EUPATH=$HOME/.steam/steam/SteamApps/common/Europa\ Universalis\ IV

cp "$EUPATH"/localisation/*_english.yml .
cp "$EUPATH"/map/default.map .
cp "$EUPATH"/map/continent.txt .
cp "$EUPATH"/map/region.txt .
cp "$EUPATH"/history/provinces/* .
cp "$EUPATH"/common/tradenodes/00_tradenodes.txt .

rename "s/[-\s]*//g" *

echo '# coding: utf-8' > localisation.py
echo 'loc = {' >> localisation.py
echo 'None: "",' >> localisation.py
for file in $(ls *.yml); do
  cat $file | grep '\".*\"' | sed -e "s/^\ /\'/" -e "s/\:/':/" -e 's/\"[\ \r]*$/\",/' >> localisation.py
done
echo '}' >> localisation.py

grep 'PROV[1-9][0-9]*:' *.yml | sed 's/.*yml://g' > prov_names.txt

for file in $(ls | grep "^[1-9][0-9]*"); do
  echo $file | sed -e "s/[A-Za-z].*//g" -e 's/^/\n\@\@/' -e 's/$/\@/' >> provinces.txt;
  cat $file >> provinces.txt;
done

python3 makewikilist.py

rm *.txt *.yml default.map localisation.py*
