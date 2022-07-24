import collections
import requests
import pandas as pd
import numpy as np


##카카오 API
def whole_region(keyword, start_x, start_y, end_x, end_y):
    page_num = 1

    all_data_list = []

    while (True):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': keyword, 'page': page_num, 'rect': f'{start_x},{start_y},{end_x},{end_y}'}
        headers = {"Authorization": "KakaoAK bde0ccb3c7c732a5380910cd2be9a535"}

        resp = requests.get(url, params=params, headers=headers)
        search_count = resp.json()['meta']['total_count']

        if search_count > 45:
            print('좌표 4등분')
            dividing_x = (start_x + end_x) / 2
            dividing_y = (start_y + end_y) / 2

            all_data_list.extend(whole_region(keyword, start_x, start_y, dividing_x, dividing_y))
            all_data_list.extend(whole_region(keyword, dividing_x, start_y, end_x, dividing_y))
            all_data_list.extend(whole_region(keyword, start_x, dividing_y, dividing_x, end_y))
            all_data_list.extend(whole_region(keyword, dividing_x, dividing_y, end_x, end_y))

            return all_data_list

        else:
            if resp.json()['meta']['is_end']:
                print('데이터추가')
                all_data_list.extend(resp.json()['documents'])

                return all_data_list

            else:
                print('다음페이지')
                page_num += 1
                all_data_list.extend(resp.json()['documents'])


def overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y):
    overlapped_result = []

    for i in range(1, num_x + 1):  ## 1,10
        end_x = start_x + next_x
        initial_start_y = start_y
        for j in range(1, num_y + 1):  ## 1,6
            end_y = initial_start_y + next_y
            each_result = whole_region(keyword, start_x, initial_start_y, end_x, end_y)
            overlapped_result.extend(each_result)
            initial_start_y = end_y
        start_x = end_x

    return overlapped_result


# 시작 좌표 및 증가값
keyword = '음식점'
start_x = 126.8991376
start_y = 37.4393374
next_x = 0.01
next_y = 0.01
num_x = 10
num_y = 6

overlapped_result = overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y)

# 최종 데이터가 담긴 리스트 중복값 제거
results = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in overlapped_result)))
X = []
Y = []
stores = []
road_address = []
place_url = []
ID = []

for place in results:
    if "관악구" in place['road_address_name']:
        X.append(float(place['x']))
        Y.append(float(place['y']))
        stores.append(place['place_name'])
        road_address.append(place['road_address_name'])
        place_url.append(place['place_url'])
        ID.append(place['id'])

        ar = np.array([ID, stores, X, Y, road_address, place_url]).T
        df = pd.DataFrame(ar, columns=['ID', 'stores', 'X', 'Y', 'road_address', 'place_url'])
        print("가게명", place['place_name'], "주소", place['road_address_name'])

print('total_reuslt_number = ', len(df))

print(df)
