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

        # DB에 값 크롤링 해서 넣는 코드
        # data_set = []
        # for code in data_set:
        #     code = str(code)
        #     data = parse_data(code)
        #     if data[0] == "":
        #         try:
        #             WasteBoat.objects.get(title=data[1])
        #         except WasteBoat.DoesNotExist:
        #             response = requests.get(data[8])
        #             binary_data = response.content
        #             temp_file = BytesIO()
        #             temp_file.write(binary_data)
        #             lat = 36 + round(random.random(), 6)
        #             lon = 127 + round(random.random(), 6)
        #             boat = WasteBoat.objects.create(latitude=lat,
        #                                             longitude=lon,
        #                                             title=data[1])
        #             boat.wasted_img.save(code+'.jpg', File(temp_file))
        #             print(code + "가 등록됐어요(Wasted)")
        #         except Boat.MultipleObjectsReturned:
        #             print(code + " 가 중복됐어요(Wasted)")
        #     else:
        #         try:
        #             Boat.objects.get(imo=data[1])
        #         except Boat.DoesNotExist:
        #             response = requests.get(data[8])
        #             binary_data = response.content
        #             temp_file = BytesIO()
        #             temp_file.write(binary_data)
        #             boat = Boat.objects.create(name=data[0],
        #                                        imo=data[1],
        #                                        calsign=data[2],
        #                                        mmsi=data[3],
        #                                        vessel_type=data[4],
        #                                        build_year=data[5],
        #                                        current_flag=data[6],
        #                                        home_port=data[7])
        #             boat.main_img.save(code+'.jpg', File(temp_file))
        #             print(code + '가 등록됐어요')
        #         except Boat.MultipleObjectsReturned:
        #             print(code + " 가 중복됐어요")
        # print(WasteBoat.objects.all())
        # for k in range(21,27):
        #     i = WasteBoat.objects.get(id=k)
        #     i.delete()
        # print(WasteBoat.objects.all())