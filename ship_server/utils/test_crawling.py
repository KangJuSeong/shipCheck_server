# import requests
# from bs4 import BeautifulSoup


# def parse_data(code):
#     url = "https://finance.naver.com/item/sise_day.nhn?code=" + code + "&page=1"
#     res = requests.get(url)
#     charset = res.encoding
#     decode = res.content.decode(charset)
#     test = ['종가', '시가', '고가', '저가', '거래량']
#     data_lst = []
#     soup = BeautifulSoup(decode, 'html.parser')
#     data = soup.find_all(attrs={'class':'tah p11'})
#     data_len = len(soup.find_all(attrs={'class':'tah p11'}))
#     data_dict = {'날짜': '','종가', '시가', '고가', '저가', '거래량'}
#     # for i in range(data_len):
#     #     if data[i].get_text() == '0':
#     #     else:
#     #         data_lst.append(data[i].get_text())
#     all_data = []
#     flag = 0
#     for i in range(10):
#         data_dict['날짜'] = soup.find_all(attrs={'class':'tah p10 gray03'})[i].get_text()
#         for j in range(5):
#             data_dict[test[j]] = data_lst[flag]
#             flag = flag + 1
#         all_data.append(data_dict)
#         print(data_dict)

        # data['날짜'] = soup.find_all(attrs={'class':'tah p10 gray03'})[i].get_text()
        #             state = soup.find_all('img')[flag_2]['alt']
        #             flag_2 = flag_2 + 1
        #             print(state)
        #             if state == '상승':
        #                 data['전일비'] = soup.find_all(attrs={'class':'tah p11 red02'})[flag_1].get_text()[5:-5] + ' (상승)'
        #                 flag_1 = flag_1 + 1
        #             elif state == '하락':
        #                 data['전일비'] = soup.find_all(attrs={'class':'tah p11 nv01'})[flag_3].get_text()[5:-5] + ' (하락)'
        #                 flag_3 = flag_3 + 1