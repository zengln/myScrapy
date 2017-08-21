from urllib import request
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt

def get_message():
    resp = request.urlopen("https://zhuanlan.zhihu.com/p/28619768")
    html_data = resp.read().decode('utf-8')
    return html_data

def get_article(html_data):
    article_soup = BeautifulSoup(html_data,'html.parser')
    text_list = article_soup.find_all('p')
    str_list = []
    for index in range(len(text_list)):
        str_list.append(text_list[index].get_text())
    return str_list

def write(str_list):
    file_write = open(r'D:\eclipse\workplace\python_demo\src\python_lspider\zh.txt',"a+",encoding = 'utf-8')
    file_write.write("\n".join(str_list))
    file_write.close()
    
def get_word():
    text_from_file_with_apath = open(r'D:\eclipse\workplace\python_demo\src\python_lspider\zh.txt',encoding = 'utf-8').read()
    wordlist_after_jieba = jieba.cut(text_from_file_with_apath,cut_all = True)
    wl_space_splot = " ".join(wordlist_after_jieba)
    print(wl_space_splot)
    my_wordcloud = WordCloud(font_path="simhei.ttf").generate(wl_space_splot)
    
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

def main():
    htmldata = get_message()
    article_text_list = get_article(htmldata)
    write(article_text_list)
    get_word()
main()