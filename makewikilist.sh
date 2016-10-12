#!/bin/bash

rm -f [1-9]* *.txt *.yml

EUPATH=$HOME/.local/share/Steam/steamapps/common/Europa\ Universalis\ IV

cp "$EUPATH"/localisation/*_english.yml .
cp "$EUPATH"/map/default.map .
cp "$EUPATH"/map/continent.txt .
cp "$EUPATH"/map/superregion.txt .
cp "$EUPATH"/map/region.txt .
cp "$EUPATH"/map/area.txt .
cp "$EUPATH"/history/provinces/* .
cp "$EUPATH"/common/tradenodes/00_tradenodes.txt .
cp "$EUPATH"/common/cultures/00_cultures.txt .

rename "s/[-\s].*//g" [1-9]*

echo "" > localisation.txt
for file in $(ls *.yml); do cat $file >> localisation.txt; echo "" >> localisation.txt; done
sed -i -e "s/:[0-9]/:/g" -e "s/§Y\"//g" -e "s/\"§//g" \
  -e "s/\"Beeldenstorm\"//g" \
  -e "s/\"only a girl,\"//g" \
  -e "s/\"Try and try again,\"//g" \
  -e "s/\"foreign languages.\"//g" \
  -e "s/\"divine visions.\"//g" \
  -e "s/\"degregado.\"//g" \
  -e "s/\"the Land of Flames.\"//g" \
  -e "s/\"challenges\"//g" \
  -e "s/\"problems\"//g" \
  -e "s/\"Grosse Kirchenordnung\"//g" \
  -e "s/\"\"When \[Root.Consort.GetName\]//g" \
  localisation.txt
echo " madagascan: \"Madagascan\"" >> localisation.txt

grep 'PROV[1-9][0-9]*:' *.yml | sed 's/.*yml://g' | sed 's/:0/:/g' > prov_names.txt

python3 makewikilist.py

for file in $(ls *.wiki); do sed 's/Naval\ Supplies/Naval\ supplies/' -i $file; done
