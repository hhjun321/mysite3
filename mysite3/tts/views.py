from django.shortcuts import render
from tts.dust_utils import *

from urllib import request
from urllib.parse import quote, urlencode
from urllib.request import urlopen
import json
import pandas as pd
from sqlalchemy import create_engine
from django.http import JsonResponse, HttpResponse


def index(request):
    return render(request, 'tts/index.html', { 'welcome_text': 'Hello World!' })

def test(request):
    db_config = 'mysql+pymysql://root:93115301@121.169.179.234:40/soomcast?charset=utf8'
    engine = create_engine(db_config, echo=False, encoding = 'utf-8')
    #final_df.to_sql(name='measure_station', con=engine, if_exists = 'append', index=False, chunksize=1000000)
    
    
    df = pd.read_sql('SELECT * FROM measure_station where item="SO2, CO, O3, NO2, PM10, PM25" and mangName="C";', con=engine)
    
    x = '37.4670256'
    y = '127.12843240000007'
    
    
    result_list=[]
    for i in range(len(df)):
        fx = df.iloc[i]['dmX']
        fy = df.iloc[i]['dmY']
        distance = getDistance(x,y,fx,fy)
        result_list.append(distance)
    
    
    df['result'] = result_list
    df = df.sort_values(['result'])[0:10]
    
    names = list(df['stationName'])
    value_list = []
    for name in names:
    
        url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
        urllist = [
                    url, '?stationName=',quote(name),'&dataTerm=DAILY','&numOfRows=150',
                    '&ServiceKey=', '9KoytWfk%2B9Gyf9buuTarVdO6z2tD03e8v5JWtlS0Ot6UBfECalPP89BZrBWlcx%2B3Cyx68hKkdrpWk0ogdeFlnQ%3D%3D', '&_returnType=json'
                ]
        url2 = ''.join(urllist)
    
    
        response = urlopen(url2).read().decode("utf-8")
        jsondata = json.loads(response)
        j_list = jsondata['list'][0]
    
        df1 = pd.DataFrame([j_list],columns=j_list.keys())
        df1 = df1[['pm25Value','pm10Value','dataTime']]
        df1['stationName'] = name
        value_list.append(df1)
    
    df1 = pd.concat(value_list)
    final_df = pd.merge(df, df1)
    final_df = final_df[ (final_df['pm25Value'] != '-') & (final_df['pm10Value'] != '-') ]
    final_df.sort_values(['result'], inplace=True)
    
    pm25 = final_df.iloc[0]['pm25Value']
    pm10 = final_df.iloc[0]['pm10Value']
    station_name = final_df.iloc[0]['stationName']
    
    pm10 = int(pm10)
    pm25 = int(pm25)
    
    txt='g'
    
    if (pm10 > 0 and pm10 <= 30) and (pm25>0 and pm25 <=15):
        print("green")
        txt='g'
        #os.system("echo '"+txt+"' > /dev/rfcomm0")
    
    elif (pm10 > 30 and pm10 <= 80) or (pm25>15 and pm25 <=50):
        print('yellow')
        txt='y'
        #os.system("echo '"+txt+"' > /dev/rfcomm0")
    elif (pm10 > 80) or (pm25>50):
        print("red")
        txt='r'
        #os.system("echo '"+txt+"' > /dev/rfcomm0")
    else:
        print("others")
        txt='g'
        #os.system("echo '"+txt+"' > /dev/rfcomm0")
    
    ## 테스트용 Python Dictionary
    context = {
        'txt': txt,
        'stationName': station_name        
    }
    
    
    # JSON 인코딩
    json_context = json.dumps(context, ensure_ascii=False)

    
    
    print(json_context)
    
    return HttpResponse(json_context, content_type='application/json; charset=utf-8')


 

    
    