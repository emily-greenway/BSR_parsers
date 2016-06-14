# Parser: bixixml (For older bixi streams, used to be common)
from bs4 import BeautifulSoup
import re

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # get the ONE line with all the data
    for line in data.split("\n"):
        match = re.match("\s*exml.parseString\(\'(.+)\'\);", line)
        if match:
            xml_data = match.group(1)
            break

    # parse out desired info
    soup = BeautifulSoup(xml_data)
    
    # capture clean results in clean_stations_list
    clean_stations_list = []

    id = 0
    for station in soup.find_all('placemark'):
        id += 1

        # Get station name
        res_name = re.search("margin-bottom:10px\">(.+?)<", station.description.encode("utf-8")) # non-greedy name match
        if not res_name:
            # something weird, skip
            continue

        # Get bikes and spaces
        res_bs = re.search(">([\-0-9]+?)<br\s?/>([\-0-9]*?)<br\s?/></div>(</div>)?]]", station.description.encode("utf-8"))
        if not res_bs:
            # something weird, skip
            continue

        # get lat/long
        ll = station.find('coordinates').string.split(',')

        # total number of docks
        if res_bs.group(1) == "" or res_bs.group(2) == "":
            # something weird, skip
            print station
            continue

        docks = int(res_bs.group(1)) + int(res_bs.group(2))

        # we want stnid, lat, lng, docks, bikes, spaces, name, active
        clean_stations_list.append([id, ll[1], ll[0], str(docks), res_bs.group(1), res_bs.group(2), res_name.group(1).decode('utf-8'), 'yes'])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser did not find any station's data."
        return False

    return clean_stations_list