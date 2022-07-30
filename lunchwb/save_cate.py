category_dict = collections.OrderedDict()
category_dict['뷔페'] = ['해산물뷔페', '한식뷔페', '고기뷔페', '뷔페']
category_dict['아시아음식'] = ['터키음식', '동남아음식', '인도음식', '아시아음식']
category_dict['양식'] = ['스테이크,립', '햄버거', '피자', '해산물', '이탈리안', '멕시칸,브라질', '양식']
category_dict['일식'] = ['일본식라면', '일식집', '돈까스,우동', '참치회', '초밥,롤', '일식']
category_dict['한식'] = ['냉면', '국밥', '순대', '수제비', '죽', '설렁탕', '감자탕', '사철탕,영양탕', '곰탕', '두부전문점', '해물,생선', '해장국', '찌개,전골', '주먹밥', '육류,고기', '국수', '한정식', '쌈밥', '한식']
category_dict['패스트푸드'] = ['패스트푸드']
category_dict['패밀리레스토랑'] = ['패밀리레스토랑']
category_dict['치킨'] = ['치킨']
category_dict['분식'] = ['분식']
category_dict['중식'] = ['중식']

conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")


