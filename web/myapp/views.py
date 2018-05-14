from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
import requests
#import execjs
import os
from bs4 import BeautifulSoup
import re
import pymysql
import time
capcha_url='http://www.travelsky.com/tsky/servlet/CallYanServlet?title=home'


def airplane(date, flight_number):
    global every
    url = 'http://www.variflight.com/flight/fnum/' + '{}.html'.format(
        flight_number) + '?AE71649A58c77&f' + 'date=2018{}'.format(date)
    data = requests.get(url=url).text
    soup = BeautifulSoup(data, 'html.parser')
    info_1 = soup.find('div', class_='f_content').find('div', class_='fly_list').find('div', class_='tit').get_text()
    info_1 = re.sub(r"\s{2,}", " ", info_1).replace('\n', '').rstrip()  # 标题，例如：PG4830 5月06号周日 共1次航班,多个空格合并成一个空格
    ur_2 = soup.find('div', class_='f_content').find('div', class_='fly_list').find('div', class_='li_box').find('a')[
        'href']
    url2 = 'http://www.variflight.com' + ur_2
    data2 = requests.get(url=url2).text
    soup2 = BeautifulSoup(data2, 'html.parser')
    info_2_1 = soup2.find('div', class_='f_content').find('div', class_='detail_main').find('div', class_='tit').find(
        'b').get_text()  # 航空公司
    info_2_1 = info_2_1.lstrip().split()[0]  # 只取航空公司名字，曼谷航空
    info_2 = soup2.find('div', class_='f_content').find('div', class_='detail_main').find_all('div', class_='fly_mian')
    for n in info_2:
        if n.find('div', class_='f_title f_title_a'):
            info_2_2 = n.find('div', class_='f_title f_title_a').get_text().replace('\n', ' ').lstrip().rstrip()  # 起飞信息
            info_2_2 = re.sub(r"\s{2,}", " ", info_2_2)  # 2018-05-06 周日计划起飞05:55 北京首都T3
            date_departure = info_2_2.split()[0]  # 2018-05-06
            time_departure = re.sub("\D", "", info_2_2.split()[1], 6)  # 05:55
            departure = info_2_2.split()[2]  # 北京首都T3
        elif n.find('div', class_='f_title f_title_c'):
            info_2_3 = n.find('div', class_='f_title f_title_c').get_text().replace('\n', ' ').lstrip().rstrip()  # 到达信息
            info_2_3 = re.sub(r"\s{2,}", " ", info_2_3)  # 2018-05-06 周日计划到达10:30 普吉T2
            date_arrival = info_2_3.split()[0]  # 2018-05-06
            time_arrival = re.sub("\D", "", info_2_3.split()[1], 6)  # 10:30
            arrival = info_2_3.split()[2]  # 普吉T2
    # print(info_1,'\n',info_2_1,'\n',info_2_2,'\n',info_2_3,'\n',departure,'\n',arrival)
    every.append(first)
    every.append(date_departure)
    every.append(time_departure)
    every.append(departure)
    every.append(date_arrival)
    every.append(time_arrival)
    every.append(arrival)
    every.append(info_2_1)
    every.append(third)
    every.append(fourth)
    print(every)
    every_all.append(every)
    '''
    db = pymysql.connect('101.236.24.202', 'root', 'oracle', 'trip', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS user_trip_info")
    sql_createtable = \'''CREATE TABLE IF NOT EXISTS user_trip_info(
            num long,
            name char(40),
            trip_num char(40),
	    date_departure date,
            time_departure char(40),
	    departure char(40),
	    date_arrival date,
	    time_arrival char(40),
	    arrival char(40),
	    airplane_company char(40),
	    flight_number char(40),
	    status char(40)

                    );
            \'''
    cursor.execute(sql_createtable)  # 建表格

    sql_data = \'''insert into user_trip_info
                (num,name,trip_num,date_departure,time_departure,departure,date_arrival,time_arrival,arrival,airplane_company,flight_number,status)
                values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');\'''.format(num, str(name),
                                                                                               str(first),
                                                                                               str(date_departure),
                                                                                               str(time_departure),
                                                                                               str(departure),
                                                                                               str(date_arrival),
                                                                                               str(time_arrival),
                                                                                               str(arrival),
                                                                                               str(info_2_1),
                                                                                               str(third), str(fourth))

    # print(sql_data)
    cursor.execute(sql_data)
    db.commit()
    cursor.close()
    db.close()
    '''



def db_save(num, name, first, date_departure, time_departure, departure, date_arrival, time_arrival, arrival, info_2_1,third, fourth):
    db = pymysql.connect('101.236.24.202', 'root', 'oracle', 'trip', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    # print('111111')
    # cursor.execute("CREATE TABLE IF NOT EXISTS user_trip_info")
    sql_createtable = '''CREATE TABLE IF NOT EXISTS user_trip_info(
            num long,
            name char(40),
            trip_num char(40),
	    date_departure date,
            time_departure char(40),
	    departure char(40),
	    date_arrival date,
	    time_arrival char(40),
	    arrival char(40),
	    airplane_company char(40),
	    flight_number char(40),
	    status char(40)

                    );
            '''
    cursor.execute(sql_createtable)  # 建表格

    sql_data = '''insert into user_trip_info
                (num,name,trip_num,date_departure,time_departure,departure,date_arrival,time_arrival,arrival,airplane_company,flight_number,status)
                values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');'''.format(num, str(name),
                                                                                               str(first),
                                                                                               str(date_departure),
                                                                                               str(time_departure),
                                                                                               str(departure),
                                                                                               str(date_arrival),
                                                                                               str(time_arrival),
                                                                                               str(arrival),
                                                                                               str(info_2_1),
                                                                                               str(third), str(fourth))

    # print(sql_data)
    cursor.execute(sql_data)
    db.commit()
    cursor.close()
    db.close()


def index(request):
    global s
    s = requests.session()
    img = s.get(capcha_url)
    name_time = str(int(time.time()))
    #print(s)
    with open('./myapp/static/{}.jpg'.format(name_time), 'wb')as f:
        f.write(img.content)


    aaa = '../static/{}.jpg'.format(name_time)
    return render(request , 'index.html' ,{'aaa' : aaa})
def hello(request):
    if request.method == 'POST':
        num = ticket_no
        name=ticket_name
        code=request.POST['capcha']
        print(num,name,code)

        url = 'http://www.travelsky.com/tsky/validate'
        headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                   'referer': 'http://www.travelsky.com/tsky/validate.jsp',
                   'Accept-Encoding': 'gzip,deflate'}
        data = {
            'validateFlag': '0',
            'eticketNo': '{}'.format(str(num)),
            'invoiceNo': '',
            'imgSrc': '/tsky/images/loading.gif',
            'eticketNoORIn': '{}'.format(str(num)),
            'passengerName_src': '{}'.format(str(name)),
            'passengerName': '{}'.format(str(name)),
            'isFromIndex': 'false',
            'randCode': '{}'.format(str(code))
        }
        #print(s)
        a = s.post(url=url, headers=headers, data=data)
        data = a.text

        soup = BeautifulSoup(data, 'html.parser')
        #print(soup)
        try:
            need1 = soup.find('div', class_='clearfix rs-box')
            # need2=soup.find('div',class_='view-info-box')#发票信息，备用
            info_1 = need1.find('ul', class_='clearfix info-ul').find('li').get_text().lstrip().replace('\n', ' ')
            # print (info_1)#欢迎信息

            info_2 = need1.find('div', class_='trip-table-box').find('table', class_='trip-table').find_all('tr')
            global every_all
            every_all=[]
            for y in info_2:
                global every,first,fourth,third,time
                every = []
                first = y.find('div', class_='coln coln-first').get_text().lstrip().rstrip()  # 航段一
                second = y.find('div', class_='coln coln-second').get_text()  # 05月06日 05:55
                third = y.find('div', class_='coln coln-third').get_text()  # PG4830
                fourth = y.find('div', class_=re.compile("coln coln-fourth")).get_text()
                # fourth=y.find('div',class_='coln coln-fourth coln-orange status_8 ').get_text()#未使用coln-green status_2
                date = re.sub("\D", "", second, 2).split()[0]  # 0506
                time = re.sub("\D", "", second, 2).split()[1]  # 05:55
                flight_number = third
                # print(first,second,third,fourth,date,flight_number)
                airplane(date, flight_number)
            bbb=every_all#所有的航段
            xvhao_list = []
            for i in range(0,len(bbb)):
                xvhao_list.append(str(i))


            bbb_new=dict(zip(xvhao_list,bbb))
            print(bbb_new)
            return render(request , 'hello.html' ,{'bbb':bbb})

        except:
            if '抱歉' in str(soup):
                print('抱歉，由于访问量增多，会有查询不到信息或信息不完整的情况，请多试几次或稍后再试!')

            else:
                # print(data)
                print('电子票号或姓名不正确')


            return HttpResponse('跳到异常处理')
    elif request.method=='GET':
        pass
def api(request):
    global order_id,ticket_name,ticket_no
    if request.method == 'POST':
        order_id = request.POST['order_id']
        ticket_no = request.POST['ticket_no']
        ticket_name = request.POST['ticket_name']
        print (order_id,ticket_no,ticket_name)
        return HttpResponse('OK')
    elif request.method == 'GET':
        print ('404')


