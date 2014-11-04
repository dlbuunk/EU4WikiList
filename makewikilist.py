# coding: utf-8

import re
from localisation import loc

inland_seas = [
# Baltic
1254, 1256, 1252, 1253, 1928, 1926, 1927, 1255, 1257, 1258, 1925, 1259,
# Black sea
1323, 1322, 1324, 1321,
# Medditeranean
1320, 1319, 1317, 1316, 1315, 1932, 1314, 1318,
1308, 1309, 1310, 1311, 1312, 1313, 1307, 1306, 1305, 1304, 1303, 1302,
1298, 1297, 1300, 1296, 1299, 1301, 1295, 1294,
# Red sea
1328, 1329,
# Persian Gulf
1335, 1334,
# China and Japan
1370, 1371, 1372,
1375, 1374, 1373, 1389, 1392,
1390, 1391,
1376, 1377, 1378, 1388, 1980, 1387, 1386, 1379,
1380, 1384, 1381, 1383, 1385, 1441, 1382,
]

relcol = {
'shiite': "00CC00",
'catholic': "CCCC00",
'ibadi': "006600",
'totemism': "807373",
'orthodox': "B38000",
'buddhism': "CC4D00",
'shinto': "CC0000",
'coptic': "B27F7F",
'hinduism': "00CCCC",
'shamanism': "804D4D",
'confucianism': "CC00E6",
'sunni': "009900",
'animism': "800000",
}

def recdict(ld, i):
    if ld[i] == '}':
        return (None,i+1)
    elif ld[i+1] == '=':
        dd = {}
        while ld[i] != '}':
            if ld[i+2] != '{':
                dd[ld[i]] = ld[i+2]
                i = i + 3
            else:
                dd[ld[i]], it = recdict(ld, i+3)
                i = it
        return (dd,i+1)
    else:
        ll = []
        while ld[i] != '}':
            if ld[i] != '{':
                ll = ll + ld[i].split()
                i = i + 1
            else:
                el, i = recdict(ld,i+1)
                ll = ll + [el]
        return (ll,i+1)

def decode(raw):
    raw = re.sub("\#.*\n","\n",raw)
    d = re.split('(\{|\}|\=|\s)', raw)
    d = [el.strip() for el in d]
    d = [el for el in d if el != '']
    return recdict(d + ['}'], 0)

provtab = {}

f = open('prov_names.txt')
pna = f.read()
f.close()

for l in pna.split('\n')[:-1]:
    s = l.split(': "')
    provtab[int(s[0][5:])] = [s[1].strip('" ')]

f = open('default.map', encoding="latin-1")
sll = decode(f.read())[0]
f.close()

for s in sll['sea_starts']:
    provtab[int(s)].append('Sea')
for l in sll['lakes']:
    provtab[int(l)].append('Lake')
for p in provtab:
    if len(provtab[p]) == 1:
        provtab[p].append(None)

f = open('continent.txt', encoding="latin-1")
con = decode(f.read())[0]
f.close()

for c in con:
    for p in con[c]:
        provtab[int(p)].append(c)
for p in provtab:
    if len(provtab[p]) == 2:
        provtab[p].append(None)

f = open('region.txt', encoding="latin-1")
reg = decode(f.read())[0]
f.close()

for p in provtab:
    provtab[p] = provtab[p] + [[], []]
for r in reg:
    for p in reg[r]:
        provtab[int(p)][3].append(r)

f = open('provinces.txt', encoding="latin-1")
pro = f.read()
f.close()

dk = re.compile('1[0-9]{3}\.[0-9]{1,2}\.[0-9]{1,2}')

for p in pro.split('@@')[1:]:
    num, dat = p.split('@')
    num = int(num)
    dat = re.sub("\#.*\n","\n",dat)
    dat = re.sub('\".*\ .*\"', 'missing_string', dat)
    if len(re.findall('add_permanent_province_modifier', dat)) > 2:
        print("3 specials...")
    elif len(re.findall('add_permanent_province_modifier', dat)) == 2:
        dat = dat.replace('add_permanent_province_modifier', 'add_permanent_province_modifier_1', 1)
    dat = decode(dat)[0]
    if dat == None:
        provtab[num] = provtab[num] + [None, None, None, None, None, None]
        continue

    upd = {}
    for key in dat:
        if dk.match(key):
            year,month,day = key.split('.')
            if int(year) > 1444:
                continue
            if int(year) == 1444 and int(month) > 11:
                continue
            if int(year) == 1444 and int(month) == 11 and int(day) > 11:
                continue
            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day
            upd[year+month+day] = dat[key]

    for key in sorted(upd):
        try:
            provtab[num][4].append(upd[key]['add_permanent_province_modifier']['name'])
        except KeyError:
            pass
        try:
            provtab[num][4].append(upd[key]['add_permanent_province_modifier_1']['name'])
        except KeyError:
            pass
        try:
            dat['owner'] = upd[key]['owner']
        except KeyError:
            pass
        try:
            dat['base_tax'] = upd[key]['base_tax']
        except KeyError:
            pass
        try:
            dat['manpower'] = upd[key]['manpower']
        except KeyError:
            pass
        try:
            dat['religion'] = upd[key]['religion']
        except KeyError:
            pass
        try:
            dat['culture'] = upd[key]['culture']
        except KeyError:
            pass
        try:
            dat['trade_goods'] = upd[key]['trade_goods']
        except KeyError:
            pass

    try:
        provtab[num].append(dat['owner'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['base_tax'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['manpower'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['religion'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['culture'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['trade_goods'])
    except KeyError:
        provtab[num].append(None)

for i in provtab:
    if len(provtab[i]) < 11:
        provtab[i] = provtab[i] + [None, None, None, None, None, None]

for p in provtab:
    if provtab[p][8] != None:
        provtab[p][8] = provtab[p][8].strip('"')
    if provtab[p][1] != None:
        continue
    elif provtab[p][6] == None:
        provtab[p][1] = 'Wasteland'
    else:
        provtab[p][1] = 'Land'

f = open('00_tradenodes.txt', encoding="latin-1")
tra = decode(f.read())[0]
f.close()

for node in tra:
    for member in tra[node]['members']:
        try:
            provtab[int(member)].append(node)
        except KeyError:
            pass
for p in provtab:
    if len(provtab[p]) < 12:
        provtab[p].append(None)

f = open('provinces.wiki', 'w')
f.write('{| class="wikitable sortable" style="font-size:95%; text-align:left"')
f.write('\n! ID')
f.write('\n! Name(1444)')
f.write('\n! Continent')
f.write('\n! Region')
f.write('\n! Owner (1444)')
f.write('\n! BT')
f.write('\n! BM')
f.write('\n! [[Religion]]')
f.write('\n! Culture')
f.write('\n! Trade goods')
f.write('\n! Trade node')
f.write('\n! Permanent modifiers')
for p in provtab:
    f.write('\n|-')
    f.write('\n| ' + str(p))
    f.write('\n| ' + provtab[p][0])
    if provtab[p][1] == 'Lake':
        f.write('\n|bgcolor=#CCDDFF colspan="10"|Lake')
        continue
    if provtab[p][1] == 'Sea':
        if p in inland_seas:
            f.write('\n|bgcolor=#CCDDFF colspan="10"|Inland sea')
        else:
            f.write('\n|bgcolor=#CCDDFF colspan="10"|Sea')
        continue
    f.write('\n| ' + loc[provtab[p][2]])
    if (provtab[p][1] == 'Wasteland'):
        f.write('\n|bgcolor=#E5E5E5 colspan="9"|Wasteland')
        continue
    f.write('\n| ')
    for i in range(len(provtab[p][3])):
        f.write(loc[provtab[p][3][i]])
        if i + 1 < len(provtab[p][3]):
            f.write(' / ')
    if provtab[p][5] == None:
        f.write('\n|')
    else:
        f.write('\n| [[' + loc[provtab[p][5]] + ']]')
    if provtab[p][6] == None:
        f.write('\n|')
    else:
        f.write('\n| ' + provtab[p][6])
    if provtab[p][7] == None:
        f.write('\n|')
    else:
        f.write('\n| ' + provtab[p][7])
    if provtab[p][8] == None:
        f.write('\n|')
    else:
        f.write('\n|bgcolor=#' + relcol[provtab[p][8]] + '|' + loc[provtab[p][8]])
    f.write('\n| ' + loc[provtab[p][9]])
    f.write('\n| ' + loc[provtab[p][10]])
    f.write('\n| ' + loc[provtab[p][11]])
    f.write('\n| ')
    for i in range(len(provtab[p][4])):
        f.write(loc[provtab[p][4][i]])
        if i + 1 < len(provtab[p][4]):
            f.write(' / ')
f.write('\n|}')
f.close()

regions = [
("europe",[
('scandinavian_region',['swedish_region','finnish_region','danish_region','norwegian_region']),
('british_isles',['great_britain_region','irish_region','danelaw','essex','highlands','lowlands','northumbria','mercia','welsh_region']),
('Islands',['icelandic_region', 'shetland_and_faroarna','atlantic_ocean_islands']),
('the_low_countries',['spanish_netherlands']),
('french_region',['gallia','breton_region','aquitania','occitania']),
('',['lotharingia']),
('german_region',['westphalian_region','franconia','swabia','austrian_region']),
('',['helvetia']),
('italian_region',['lombardia','two_sicilies']),
('iberian_peninsula',['spanish_region','andalusia']),
('The Baltics',['the_baltics','lithuanian_region']),
('East-Central Europe',['bohemian_region','hungarian_region','wielkopolska','malopolska']),
('Southeast Europe',['western_balkans','eastern_balkans','greece_region','dacia','croatian_region','serbian_region','bulgarian_region']),
('Eastern Europe',['belarus','ukrainian_region','russian_region','kaffa_and_azow','steppes']),
('',['caucasus']),
('Turkey',['anatolia','asia_minor']),
]),
("asia",[
('Siberia',['western_siberia','eastern_siberia']),
('',['central_asia']),
('Far East',['korean_region','japanese_region']),
('indonesian_region',['javan_region','sumatran_region','borneo_region','malay_peninsula_region','spice_islands']),
('',['indochinan_region','eastasian_trade_ports','east_asian_cot']),
('persian_region',['baluchistan_region','khorasan_region','afghanistan_region','tabarestan_region','sistan_region']),
('arab_region',['hedjazi_region','yemeni_region','omani_region','nejdi_region']),
('middle_east',['armenian_region','azerbaijani_region','mesopotamian_region','syrian_region']),
]),
("oceania",[
('new_zealand_region',[]),
('australian_coast',[]),
('pacific_ocean_islands',[]),
]),
("africa",[
('north_africa',['moroccan_region','algerian_region','tunisian_region','tripoli_region','cyrenaica_region']),
('',['saharan_region','egypt_region','funj_spawning_region']),
('central_africa',['west_african_coast','guinean_coast','niger_delta','senegambia','fulo_spawning_region','kongo']),
('',['manding','timbuktu_region','southern_sahara','volta_basin','ashanti_region','lower_niger']),
('',['middle_niger','hausaland','lake_chad','kodugu']),
('',['banaadir_region','haud_region','kaffa_region','tigray_region','amhara_region','maakhir_region','oromo_spawn_region']),
('',['mascarene_islands','south_africa']),
]),
("north_america",[
('northern_america',['northwestern_america','northeastern_america','greenland_region']),
('',['columbia_region','hudson_bay_region','st_lawrence_region','canada_region','newfoundland_region','acadia_region']),
('',['western_america','great_plains','the_mississippi_region','eastern_america','the_thirteen_colonies']),
('central_america',['mesoamerica_region','yucatan_region','the_carribean']),
]),
("south_america",[
('the_spanish_main',['guyana_region','venezuela_region','new_andalucia_region','castilla_del_oro_region','new_granada_region']),
('the_andes',['chile_region','bolivia_region','qullasuyu_region','antisuyu_region','kuntisuyu_region','chinchaysuyu_region','quito_region']),
('',['amazonas']),
('brazil_region',['rio_grande_do_sol_region','minas_gerais_region','goias_region','mato_grosso_region','sao_paolo_region','rio_de_janeiro_region','bahia_region','pernambuco_region','maranhao_region','grao_para_region']),
('pampas_region',['paraguay_region','la_plata_region','southern_pampas_region']),
('patagonia_region',['cuyo_region','buenos_aires_region','tucuman_region','chaco_region','banda_oriental_region']),
]),
]

def doregion(name,cont):
    s = "=== " + loc[name] + " ===\n{{Regions table\n| rows="
    for p in reg[name]:
        n = int(p)
        if provtab[n][1] != 'Land':
            s = s + "{{RTR|" + p + "|" + provtab[n][0] + "|Natives|||None||Unknown||Wasteland"
        else:
            s = s + "{{RTR|" + p + "|" + provtab[n][0] + "|" + \
                (loc[provtab[n][5]] if provtab[n][5] != None else "Natives") + "|" + \
                provtab[n][6] + "|" + \
                (provtab[n][7] if provtab[n][7] != None else "") + "|" + \
                (loc[provtab[n][8]] if provtab[n][8] != None else "None") + "|" + \
                loc[provtab[n][9]] + "|" + \
                loc[provtab[n][10]] + "|" + \
                loc[provtab[n][11]] + "|"
        if provtab[n][4] != []:
            for i in range(len(provtab[n][4])):
                s = s + loc[provtab[n][4][i]]
                if i + 1 < len(provtab[n][4]):
                    s = s  + ' / '
        s = s + "}}\n"
    s = s + "}}\n"
    ooc = [(int(p),provtab[int(p)][2]) for p in reg[name] if p not in con[cont]]
    continents = ['europe','asia','oceania','africa','north_america','south_america']
    for c in continents:
        prs = [p[0] for p in ooc if p[1] == c]
        if len(prs) > 0:
            if len(prs) == 1:
                s = s + "The province "
            else:
                s = s + "The provinces "
            for i in range(len(prs)):
                s = s + provtab[prs[i]][0] + ' (' + str(prs[i]) + ')'
                if i + 2 == len(prs):
                    s = s + ' and '
                elif i + 2 < len(prs):
                    s = s + ', '
            if len(prs) == 1:
                s = s + " belongs to " + loc[c] + '.\n'
            else:
                s = s + " belong to " + loc[c] + '.\n'
    return s

for c in regions:
    f = open(c[0] + '.wiki', 'w')
    f.write('{| class="toccolours "\n')
    f.write('! colspan="2" | Contents\n')
    f.write('|-\n')
    f.write("""| colspan="2" | '''[[#Province lists of regions|Province lists of regions]]'''""")

    for rgrp in c[1]:
        f.write('\n|-\n| style="text-align: right;" | ')
        if rgrp[0] in loc:
            f.write("[[#" + loc[rgrp[0]] + "|" + loc[rgrp[0]] + "]]")
        else:
            f.write(rgrp[0])
        f.write('\n| style="padding-left:0.5em" | ')
        for i in range(len(rgrp[1])):
            f.write("[[#" + loc[rgrp[1][i]] + "|" + loc[rgrp[1][i]] + "]]")
            if i + 1 < len(rgrp[1]):
                f.write(" • ")

    f.write('\n|}\n')
    f.write('== Province lists of regions ==\n')
    f.write('The table content is out of the files in {{path|history/provinces}} and refers to a game start on the 11th of November, 1444.\n\n')

    for rgrp in c[1]:
        try:
            f.write(doregion(rgrp[0],c[0]))
        except KeyError:
            pass
        for r in rgrp[1]:
            f.write(doregion(r,c[0]))
    f.close()

spec_reg_india = [
'indian_region',
'indian_coast',
'hindustan_region',
'punjab_region',
'bengal_region',
'bihar_region',
'jharkhand_region',
'gondwana_region',
'orissa_region',
'telingana_region',
'andhra_region',
'coromandel_region',
'konkan_region',
'kerala_region',
'malwa_region',
'rajputana_region',
'sindh_region',
'tamil_region',
'karnataka_region',
'maharashtra_region',
'assam_region',
'himalayas_region',
'kashmir_region',
'lanka_region',
'gujarat_region',
'indian_ocean_islands',
]

f = open('india.wiki','w')
for r in spec_reg_india:
    f.write(doregion(r,'asia'))
f.close()

spec_reg_china = [
'chinese_region',
'chinese_coast',
'manchuria',
'outer_manchuria',
'inner_manchuria',
'mongolia',
'inner_mongolia',
'outer_mongolia',
'tarim_basin',
'zungaria',
'tibet',
'north_zhili',
'shandong',
'south_zhili',
'zhejiang',
'jiangxi',
'fujian',
'taiwan',
'guangdong',
'guangxi',
'yunnan',
'sichuan',
'huguang',
'henan',
'shanxi',
'shaanxi',
'guizhou',
]

f = open('china.wiki','w')
for r in spec_reg_china:
    f.write(doregion(r,'asia'))
f.close()

for r in list(set([r for r in reg]) - set([r for rgrp in [rgrp for con in regions for rgrp in con[1]] for r in [rgrp[0]] + rgrp[1] if r in loc] + spec_reg_india + spec_reg_china)):
    print('Province not output: ' + loc[r])