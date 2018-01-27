from urllib import request
from bs4 import BeautifulSoup
from _ast import IsNot
def content(html):
    #内容分割
    str = '<article class="article-content">'
    content = html.partition(str)[2]
    str1 = '<div class="article-social>'
    content = content.partition(str1)[0]
    return content

def title(content,beg = 0):
    try:
        soup = BeautifulSoup(content,'html.parser')
        img_list = soup.find_all('img')
        index = 0
        title_list = []
        while True:
            dic = {}
            num1 = content.index('】', beg)
            num2 = content.index('</p>', num1)
            key = 'title' + str(index)
            img_key = 'img' + str(index)
            dic[key] = content[num1+1:num2]
            dic[img_key] = (img_list[index])['src']
            title_list.append(dic)
            beg = num2
            index += 1
    except ValueError:
        return title_list

def get_title(html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    message_list = soup.find_all('p')
    message_dict = {}
    all_message_list = []
    img_index = 0;
    for index in range(len(message_list)):
        if message_list[index].get_text() is "" :
            img_key = 'img' + str(img_index)
            message_dict[img_key] = (message_list[index].find('img'))['src']
            img_index += 1
        else:
            if message_dict:
                all_message_list.append(message_dict) 
                message_dict = {}        
            message_dict['title'] = message_list[index].get_text()
            img_index = 0;
    return all_message_list
            
def data_out(data):
    file_open = open(r'D:\\eclipse\workplace\python_demo\src\python_lspider\test.txt',"a+",encoding='utf-8')
    file_open.write("\n")
    file_open.write("\n".join(data))
    file_open.close()
    
def list_to_string(list_data):
    file_list = []
    for index in range(len(list_data)):
        list_data_str = ''
        list_data_str += (list_data[index])["title"]
        list_data_str += '\n'
        list_data_str += (list_data[index])["img0"] 
        if len(list_data[index]) > 2 :
            list_data_str += '\n'
            length =len(list_data[index]) - 2
            img_index = 'img' + str(length)
            list_data_str += (list_data[index])[img_index]
        file_list.append(list_data_str)
    return file_list

def main():
    resp = request.urlopen('https://bohaishibei.com/post/29543/')
    html_data = resp.read().decode('utf-8')
#     content1 = content(html_data)
#     ls_str = list_to_string(title(content1))
#     data_out(ls_str)
    ls_str = list_to_string(get_title(html_data))
    data_out(ls_str)

main();
    