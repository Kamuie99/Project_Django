from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Create your views here.
def index(request):
  return render(request, 'weathers/index.html')

#============================================= 문제 1번 =================================================
def problem1(request):
  csv_path = 'weather_data.csv'
  df = pd.read_csv(csv_path)
  
  context = {
    'df' : df
  }
  return render(request, 'weathers/problem1.html', context)


#============================================= 문제 2번 =================================================

def problem2(request):
  csv_path = 'weather_data.csv'
  df = pd.read_csv(csv_path)
  
  dates = pd.to_datetime(df['Date'])
  temperatures = df[['TempHighF', 'TempAvgF', 'TempLowF']]

  plt.figure(figsize=(10, 6))
  plt.plot(dates, temperatures['TempHighF'], color='skyblue', linestyle='-', label='High Temperature')
  plt.plot(dates, temperatures['TempAvgF'], color='orange', linestyle='-', label='Average Temperature')
  plt.plot(dates, temperatures['TempLowF'], color='lightgreen', linestyle='-', label='Low Temperature')
  plt.title('Temperature Variation')
  plt.xlabel('Date')
  plt.ylabel('Temperature (Fahrenheit)')
  plt.legend(loc='lower center')
  plt.grid(True)

  # 그래프를 이미지로 변환하여 base64로 인코딩
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
  buffer.close()

  # 렌더링할 HTML 페이지와 전달할 데이터를 정의하여 context에 저장
  context = {
      'image': f'data:image/png;base64,{image_base64}',
  }

  # problem2.html 페이지를 렌더링하여 반환
  return render(request, 'weathers/problem2.html', context)

#============================================= 문제 3번 =================================================

def problem3(request):
    csv_path = 'weather_data.csv'
    df = pd.read_csv(csv_path, usecols=['Date', 'TempHighF', 'TempAvgF', 'TempLowF'])
    
    df['Date'] = pd.to_datetime(df['Date'])

    group_by_month = df.groupby([df['Date'].dt.year, df['Date'].dt.month]).mean()
    
    # df['Year-Month'] = df['Date'].dt.to_period('M')

    # 온도 필드를 숫자형식으로 변환
    # df[['TempHighF', 'TempAvgF', 'TempLowF']] = df[['TempHighF', 'TempAvgF', 'TempLowF']].apply(pd.to_numeric, errors='coerce')

    # 월별 최고, 평균, 최저 온도의 평균 계산
    # monthly_stats = df.groupby('Year-Month').agg({'TempHighF': 'max', 'TempAvgF': 'mean', 'TempLowF': 'min'})
    # monthly_stats.columns = ['Max Temp', 'Mean Temp', 'Min Temp']
    
    # 라인 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.plot(group_by_month['Date'], group_by_month['TempHighF'], label='High Temperature', color='skyblue')
    plt.plot(group_by_month['Date'], group_by_month['TempAvgF'], label='Average Temperature', color='orange')
    plt.plot(group_by_month['Date'], group_by_month['TempLowF'], label='Low Temperature', color='lightgreen')
    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature (Fahrenheit)')
    # plt.xticks([str(period) for period in monthly_stats.index[1::6]]) 
    plt.yticks(range(40, 110, 10))# Convert PeriodIndex to strings=
    plt.legend(loc='lower right')
    plt.grid(True)

    # 그래프를 이미지로 변환하여 base64로 인코딩
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # 렌더링할 HTML 페이지와 전달할 데이터를 정의하여 context에 저장
    context = {
        'image': f'data:image/png;base64,{image_base64}',
    }

    # problem3.html 페이지를 렌더링하여 반환
    return render(request, 'weathers/problem3.html', context)
  
#============================================= 문제 4번 =================================================

def problem4(request):
    csv_path = 'weather_data.csv'
    df = pd.read_csv(csv_path)

    events_count = df['Events'].str.split(',').explode().str.strip().value_counts()
    # events_count = events_count.replace('', 'No events')
    events_count = dict(events_count)
    events_count['No Events'] = events_count.pop('')
    # 추가한거
    events_count_sorted = {k: events_count[k] for k in sorted(events_count, key=lambda x: x != 'No Events')}

    
    print(events_count)
    events = list(events_count_sorted.keys())
    counts = list(events_count_sorted.values())

    plt.figure(figsize=(8, 6))
    plt.bar(events, counts)
    plt.title('Event Counts')
    plt.xlabel('Event')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.grid(True)

    # Convert the plot to an image and encode it in base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Pass the base64-encoded image in the context
    context = {
        'image': f'data:image/png;base64,{image_base64}',
    }

    return render(request, 'weathers/problem4.html', context)


