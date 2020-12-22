import requests
from bs4 import BeautifulSoup


def parse_data(code):
    url = "http://www.shipspotting.com/ships/ship.php?imo=" + code
    res = requests.get(url)
    charset = res.encoding
    decode = res.content.decode(charset)
    soup = BeautifulSoup(decode, 'html.parser')
    my_titles = soup.select('.whiteboxstroke')
    url = soup.select('.content')
    for img in url:
        imgUrl = img.img['src']
        break
    for title in my_titles:
        idx = title.text.find('name')
        idx2 = title.text.find('IMO')
        idx3 = title.text.find('Callsign')
        idx4 = title.text.find('MMSI')
        idx5 = title.text.find('Vessel')
        idx6 = title.text.find('Build year')
        idx7 = title.text.find('Current flag')
        idx8 = title.text.find('Home port')
        idx9 = title.text.find('Photos')
        name = title.text[idx+6:idx2]
        imo = title.text[idx2+5:idx3]
        callsign = title.text[idx3+10:idx4]
        mmsi = title.text[idx4+6:idx5]
        vessel = title.text[idx5+13:idx6]
        year = title.text[idx6+12:idx7]
        flag = title.text[idx7+14:idx8]
        port = title.text[idx8+11:idx9]
        return name, imo, callsign, mmsi, vessel, year, flag, port, imgUrl
