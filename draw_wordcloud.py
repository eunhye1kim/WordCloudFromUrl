%matplotlib inline
import requests                  # 웹 페이지의 HTML을 가져오는 모듈
import newspaper
from bs4 import BeautifulSoup    # HTML을 파싱하는 모듈
from konlpy.tag import Mecab
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def draw_wordcloud_from_url(url_link):
    # 웹 페이지를 가져온 뒤 BeautifulSoup 객체로 만듦
    response = requests.get(url_link)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', { 'class': 'gall_list' })    # <table class="table_develop3">을 찾음
    links = []                            # 링크를 저장할 리스트 생성
    news_text = ''
    for tr in table.find_all('tr', class_="ub-content"):      # 모든 <tr.ub-content> 태그를 찾아서 반복(각 지점의 데이터를 가져옴)
        title = tr.find('td', class_="gall_tit")
        link = title.find('a').text
        links.append(link)

        article = newspaper.Article(link, language='ko')
        article.download()
        article.parse()
        news_text += article.text

    # konlpy, Mecab: 형태소 분석을 통해 본문에서 명사추출, 1글자는 단어는 삭제
    engine = Mecab()
    nouns = engine.nouns(news_text)
    nouns = [n for n in nouns if len(n) > 1]

    # Counter: 단어수 세기, 가장 많이 등장한 단어(명사) 40개
    count = Counter(nouns)
    tags = count.most_common(40)

    # WordCloud, matplotlib: 단어 구름 그리기
    font_path = '/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf'
    wc = WordCloud(font_path=font_path, background_color='white', width=800, height=600)
    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10,8))
    plt.axis('off')
    plt.imshow(cloud)
     
url_link = 'https://gall.dcinside.com/mgallery/board/lists/?id=pebble&list_num=100&sort_type=N&search_head=&page=1'
draw_wordcloud_from_url(url_link)
