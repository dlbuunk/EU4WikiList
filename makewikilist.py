# coding: utf-8

import re

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
'confucianism': "D7E38D",
'sunni': "009900",
'animism': "800000",
'protestant': "FFFFFF",
'reformed': "FFFFFF",
'sikhism': "FFFFFF",
'nahuatl': "3F723F",
'inti': "3F7272",
'mesoamerican_religion': "72723F",
'jewish': "9A1A66",
'zoroastrian': "80B333",
'tengri_pagan_reformed': "1A4DDA",
'mahayana': "CC4D80",
'vajrayana': "CC4D4D",
}

def recdict(ld, i):
    if ld[i] == '}':
        return (None,i+1)
    elif ld[i+1] == '=':
        dd = {}
        while ld[i] != '}':
            if ld[i] in dd and type(dd[ld[i]]) is tuple:
                if ld[i+2] != '{':
                    dd[ld[i]] = dd[ld[i]] + (ld[i+2],)
                    i = i + 3
                else:
                    tmp, it = recdict(ld, i+3)
                    dd[ld[i]] = dd[ld[i]] + (tmp,)
                    i = it
            elif ld[i] in dd:
                if ld[i+2] != '{':
                    dd[ld[i]] = (dd[ld[i]], ld[i+2])
                    i = i + 3
                else:
                    tmp, it = recdict(ld, i+3)
                    dd[ld[i]] = (dd[ld[i]], tmp)
                    i = it
            else:
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

f = open('localisation.txt')
loc_dat = f.read().split('\n')
f.close()

out = ['# coding: utf-8\nloc = {\nNone: "",\n']
for line in [line for line in loc_dat if re.search('\".*\"', line) != None]:
    tmp = re.sub("^\ ", "'", line)
    tmp = re.sub(":", "':", tmp)
    tmp = re.sub(" # .*", '', tmp)
    tmp = re.sub(" #E.*", '', tmp)
    out.append(re.sub("\"[\ \r]*$", '",\n', tmp))
out.append('}\n')

f = open('localisation.py', 'w')
f.write("".join(out))
f.close()

from localisation import loc

provtab = {}

f = open('prov_names.txt')
pna = f.read()
f.close()

for l in pna.split('\n')[:-1]:
    s = l.split(': "')
    provtab[int(s[0][5:])] = [s[1].strip('" ')]

f = open('area.txt', encoding="latin-1")
area = decode(f.read())[0]
f.close()

for a in area:
    for p in area[a]:
        provtab[int(p)].append(a)
for p in provtab:
    if len(provtab[p]) == 1:
        provtab[p].append(None)

f = open('region.txt', encoding="latin-1")
reg = decode(f.read())[0]
f.close()

for r in reg:
    if 'areas' not in reg[r]:
        continue
    for a in reg[r]['areas']:
        for p in provtab:
            if provtab[p][1] == a:
                provtab[p].append(r)
for p in provtab:
    if len(provtab[p]) == 2:
        provtab[p].append(None)

f = open('superregion.txt', encoding="latin-1")
sreg = decode(f.read())[0]
f.close()

for s in sreg:
    if sreg[s] == None:
        continue
    for r in sreg[s]:
        for p in provtab:
            if provtab[p][2] == r:
                provtab[p].append(s)
for p in provtab:
    if len(provtab[p]) == 3:
        provtab[p].append(None)

f = open('continent.txt', encoding="latin-1")
con = decode(f.read())[0]
f.close()

for c in con:
    try:
        for p in con[c]:
            provtab[int(p)].append(c)
    except TypeError:
        pass
for p in provtab:
    if len(provtab[p]) == 4:
        provtab[p].append(None)

dk = re.compile('1[0-9]{3}\.[0-9]{1,2}\.[0-9]{1,2}')

for num in provtab:
    provtab[num].append([])
    try:
        f = open(str(num), encoding="latin-1")
        dat = f.read()
        f.close()
    except FileNotFoundError:
        provtab[num] = provtab[num] + [None, None, None, None, None, None, None]
        continue
    dat = dat + '\n'
    dat = re.sub("\#.*\n","\n",dat)
    dat = re.sub('\".*\ .*\"', 'missing_string', dat)
    dat = decode(dat)[0]
    if dat == None:
        provtab[num] = provtab[num] + [None, None, None, None, None, None, None]
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

#    for key in sorted(upd):
#        try:
#            provtab[num][5].append(upd[key]['add_permanent_province_modifier']['name'])
#        except KeyError:
#            pass
#        except TypeError:
#            try:
#                for modifier in upd[key]['add_permanent_province_modifier']:
#                    provtab[num][5].append(modifier['name'])
#            except TypeError:
#               for modifier in upd[key]:
#                    try:
#                        provtab[num][5].append(modifier['add_permanent_province_modifier']['name'])
#                    except KeyError:
#                        pass
#                    except TypeError:
#                        for submod in modifier:
#                            provtab[num][5].append(submod['name'])

        try:
            dat['owner'] = upd[key]['owner']
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            dat['base_tax'] = upd[key]['base_tax']
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            dat['base_production'] = upd[key]['base_production']
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            dat['base_manpower'] = upd[key]['base_manpower']
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            dat['religion'] = upd[key]['religion']
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            dat['culture'] = upd[key]['culture']
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            dat['trade_goods'] = upd[key]['trade_goods']
        except KeyError:
            pass
        except TypeError:
            pass

    if 'add_permanent_province_modifier' in dat:
        if type(dat['add_permanent_province_modifier']) == tuple:
            for mod in dat['add_permanent_province_modifier']:
                provtab[num][5].append(mod['name'])
        else:
            provtab[num][5].append(dat['add_permanent_province_modifier']['name'])

    try:
        provtab[num].append(dat['owner'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['base_tax'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['base_production'])
    except KeyError:
        provtab[num].append(None)
    try:
        provtab[num].append(dat['base_manpower'])
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

for p in provtab:
    if provtab[p][6] == 'XXX':
        provtab[p][6] = None
    if provtab[p][10] != None:
        provtab[p][10] = provtab[p][10].strip('"')

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
    if len(provtab[p]) < 14:
        provtab[p].append(None)

f = open('default.map', encoding="latin-1")
sll = decode(f.read())[0]
f.close()

for s in sll['sea_starts']:
    if int(s) in provtab:
        provtab[int(s)].append('Sea')
for l in sll['lakes']:
    if int(l) in provtab:
        provtab[int(l)].append('Lake')
for p in provtab:
    if len(provtab[p]) < 15:
        provtab[p].append(None)

f = open('provinces.wiki', 'w')
f.write('{| class="wikitable sortable" style="font-size:95%; text-align:left"')
f.write('\n! ID')
f.write('\n! Name')
f.write('\n! Area')
f.write('\n! Region')
f.write('\n! Superregion')
f.write('\n! Continent')
f.write('\n! Owner (1444)')
f.write('\n! BT')
f.write('\n! BP')
f.write('\n! BM')
f.write('\n! Religion')
f.write('\n! Culture')
f.write('\n! Trade goods')
f.write('\n! Trade node')
f.write('\n! Permanent modifiers')
for p in provtab:
    f.write('\n|-')
    f.write('\n| ' + str(p))
    f.write('\n| ' + provtab[p][0])
    if provtab[p][14] == 'Lake':
        f.write('\n|bgcolor=#CCDDFF colspan="13"|Lake')
        continue
    if provtab[p][14] == 'Sea':
        if p in inland_seas:
            f.write('\n|bgcolor=#CCDDFF colspan="13"|Inland sea')
        else:
            f.write('\n|bgcolor=#CCDDFF colspan="13"|Sea')
        continue
    f.write('\n| ' + loc[provtab[p][4]])
    if provtab[p][7] == None:
        f.write('\n|bgcolor=#E5E5E5 colspan="12"|Wasteland')
        continue
    f.write('\n| ' + loc[provtab[p][3]])
    f.write('\n| ' + loc[provtab[p][2]])
    f.write('\n| ' + loc[provtab[p][1]])
    if provtab[p][6] == None:
        f.write('\n|')
    else:
        f.write('\n| [[' + loc[provtab[p][6]] + ']]')
    if provtab[p][7] == None:
        f.write('\n|')
    else:
        f.write('\n| ' + provtab[p][7])
    if provtab[p][8] == None:
        f.write('\n|')
    else:
        f.write('\n| ' + provtab[p][8])
    if provtab[p][9] == None:
        f.write('\n|')
    else:
        f.write('\n| ' + provtab[p][9])
    if provtab[p][10] == None:
        f.write('\n|')
    else:
        f.write('\n|bgcolor=#' + relcol[provtab[p][10]] + '|' + loc[provtab[p][10]])
    f.write('\n| ' + loc[provtab[p][11]])
    f.write('\n| ' + loc[provtab[p][12]])
    f.write('\n| ' + loc[provtab[p][13]])
    f.write('\n| ')
    for i in range(len(provtab[p][5])):
        f.write(loc[provtab[p][5][i]])
        if i + 1 < len(provtab[p][5]):
            f.write(' / ')
f.write('\n|}')
f.close()

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
                provtab[n][11] + "|" + \
                provtab[n][7] + "|" + \
                (loc[provtab[n][8]] if provtab[n][8] != None else "None") + "|" + \
                loc[provtab[n][9]] + "|" + \
                loc[provtab[n][10]] + "|" + \
                loc[provtab[n][-1]] + "|"
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

#for c in regions:
#    f = open(c[0] + '.wiki', 'w')
#    f.write('{| class="toccolours "\n')
#    f.write('! colspan="2" | Contents\n')
#    f.write('|-\n')
#    f.write("""| colspan="2" | '''[[#Province lists of regions|Province lists of regions]]'''""")
#
#    for rgrp in c[1]:
#        f.write('\n|-\n| style="text-align: right;" | ')
#        if rgrp[0] in loc:
#            f.write("[[#" + loc[rgrp[0]] + "|" + loc[rgrp[0]] + "]]")
#        else:
#            f.write(rgrp[0])
#        f.write('\n| style="padding-left:0.5em" | ')
#        for i in range(len(rgrp[1])):
#            f.write("[[#" + loc[rgrp[1][i]] + "|" + loc[rgrp[1][i]] + "]]")
#            if i + 1 < len(rgrp[1]):
#                f.write(" • ")
#
#    f.write('\n|}\n')
#    f.write('== Province lists of regions ==\n')
#    f.write('The table content is out of the files in {{path|history/provinces}} and refers to a game start on the 11th of November, 1444.\n\n')
#
#    for rgrp in c[1]:
#        try:
#            f.write(doregion(rgrp[0],c[0]))
#        except KeyError:
#            pass
#        for r in rgrp[1]:
#            f.write(doregion(r,c[0]))
#    f.close()

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

#f = open('india.wiki','w')
#for r in spec_reg_india:
#    f.write(doregion(r,'asia'))
#f.close()

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

#f = open('china.wiki','w')
#for r in spec_reg_china:
#    f.write(doregion(r,'asia'))
#f.close()

#for r in list(set([r for r in reg]) - set([r for rgrp in [rgrp for con in regions for rgrp in con[1]] for r in [rgrp[0]] + rgrp[1] if r in loc] + spec_reg_india + spec_reg_china)):
#    print('Region not output: ' + r)

def getOutgoingNodes(data,node):
    if 'outgoing' not in data[node]:
        return []
    if type(data[node]['outgoing']) is dict:
        return [data[node]['outgoing']['name'].strip('"')]
    ll = []
    for next_node in data[node]['outgoing']:
        ll.append(next_node['name'].strip('"'))
    return ll

def makeTradeTree(data,node):
    return node,[makeTradeTree(data, out_node) for out_node in getOutgoingNodes(data,node)]

def getIncomingNodes(data,node):
    ll = []
    for in_node in data:
        if 'outgoing' in data[in_node]:
            if type(data[in_node]['outgoing']) is dict:
                if data[in_node]['outgoing']['name'].strip('"') == node:
                    ll.append(in_node)
            else:
                for out_node in data[in_node]['outgoing']:
                    if out_node['name'].strip('"') == node:
                        ll.append(in_node)
    return ll

def makeReverseTradeTree(data, node):
    return node,[makeReverseTradeTree(data, in_node) for in_node in getIncomingNodes(data, node)]

def findDepth(tree):
    if tree[1] == []:
        return 0
    return max([findDepth(node) for node in tree[1]]) + 1

#ll = []
#for node in tra:
#    ll.append('\n|-\n| ')
#    ll.append(loc[node])
#    ll.append(' {{anchor|')
#    ll.append(node)
#    ll.append('}}\n| ')
#    if 'inland' in tra[node] and tra[node]['inland'] == 'yes':
#        ll.append('Inland')
#    ll.append('\n| ')
#    ll.append(loc[provtab[int(tra[node]['location'])][2]])
#    ll.append('\n| ')
#    ll.append(str(len(tra[node]['members'])))
#    ll.append('\n| ')
#    for in_node in getIncomingNodes(tra,node):
#        ll.append('\n* [[#')
#        ll.append(in_node)
#        ll.append('|')
#        ll.append(loc[in_node])
#        ll.append(']]')
#    ll.append('\n|')
#    for out_node in getOutgoingNodes(tra,node):
#        ll.append('\n* [[#')
#        ll.append(out_node)
#        ll.append('|')
#        ll.append(loc[out_node])
#        ll.append(']]')
##    ll.append('\n| ')
##    ll.append(str(findDepth(makeReverseTradeTree(tra,node))))
##    ll.append('\n| ')
##    ll.append(str(findDepth(makeTradeTree(tra,node))))
##    ll.append('\n| ')
##    ll.append(str(findDepth(makeReverseTradeTree(tra,node)) + 1 + findDepth(makeTradeTree(tra,node))))
#    ll.append('\n|')
#    for p in [int(p) for p in tra[node]['members'] if len(provtab[int(p)][4]) > 0]:
#        ll.append('\n* ')
#        ll.append(provtab[p][0])
#        ll.append(' (')
#        for i in range(len(provtab[p][4])):
#            if provtab[p][4][i] == 'center_of_trade_modifier':
#                ll.append('COT')
#            elif re.search(".*estuary_modifier", provtab[p][4][i]) != None:
#                ll.append('Estuary')
#            elif re.search(".*toll.*", provtab[p][4][i]) != None:
#                ll.append('Toll')
#            else:
#                ll.append(loc[provtab[p][4][i]])
#            if i + 1 < len(provtab[p][4]):
#                ll.append(', ')
#        ll.append(')')



#f = open('trade.wiki','w')
#f.write("".join(ll))
#f.close()
