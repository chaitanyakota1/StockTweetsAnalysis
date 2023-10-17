from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime,timedelta
import time
import requests


class TweetExtractor():  
  def __init__(self,StartDate,EndDate,Symbols):

    # Initialisation Variables (Start Date, End Date & List of Symbols)

    self.StartDate = datetime.strptime(StartDate,"%m/%d/%Y").strftime('%m/%d/%Y') 

    #Since tweets are give backwards, here start date is the end date of the date range

    self.EndDate = (datetime.strptime(EndDate,"%m/%d/%Y").date()- timedelta(1)).strftime('%m/%d/%Y') 

    #End date - 1 (Time delta) is done. Ex for 07/10/2022, tweets upto first tweet of 07/09/22 are extracted.

    self.Symbols = Symbols

    self.InitialDate = datetime.strptime(StartDate,"%m/%d/%Y").strftime('%m%d%Y') #For saving file

    self.FinalDate = datetime.strptime(EndDate,"%m/%d/%Y").strftime('%m%d%Y') #For saving file
  

  def ExtractorDate(self,Symbol):

    int_start_date = int(datetime.strptime(self.StartDate,"%m/%d/%Y").strftime('%Y%d%m'))

    int_end_date = int(datetime.strptime(self.EndDate,"%m/%d/%Y").strftime('%Y%d%m'))
    
    r_end = []
    initial = [] #+1 is done as url keeps id as Max
    jsonfil = []
    i = 0

    # Extracting tweets from starting date and will stop at end date
    end_id = 0
    err_count = 0
    break_count = 0
    err_url = []
    err_id = []
    while i >= 0:
      url = "https://api.stocktwits.com/api/2/streams/symbol/"+str(Symbol)+".X.json?\&max="+str(initial)
      try:
        jsonfil = requests.get(url).json()
        tweet_date_0 = jsonfil['messages'][0]['created_at']
        tweet_date_0 = int(datetime.strptime(tweet_date_0,"%Y-%m-%dT%H:%M:%S%z").strftime('%Y%d%m'))

        r_end.append(jsonfil['messages'])
        initial = jsonfil['cursor']['max']
        if tweet_date_0 == int_end_date or tweet_date_0 < int_end_date: #Condition to check if end date is reached (i.e until tweets from previous day start)
            print(tweet_date_0)
            print(int_end_date)
            print(url)
            end_id = initial
            print("i is",i)
            break
        i = i +1
      
      except:
        err_id.append(initial)
        err_count = err_count+1
        if err_count > 1 and initial == err_id[err_count-2]:
          break_count = break_count +1
        print("Error Found at",initial)
        initial = str(int(initial) + 1)
        err_url.append(url)
        
        if break_count >10: # No more tweets available.
          break


    date = []
    id = []
    message = []
    timestamp = []
    username = []
    tag = []
    userid = []
    for iter in r_end:
      for i in range(0,31):
        try:
          date.append(int(datetime.strptime(iter[i]['created_at'],"%Y-%m-%dT%H:%M:%S%z").strftime('%Y%d%m'))) 
          # Created a temporary date column to manage the dataframe
          message.append(iter[i]['body'])
          timestamp.append(iter[i]['created_at'])
          username.append(iter[i]['user']["username"])
          userid.append(iter[i]['user']["id"])
          id.append(iter[i]['id'])
          try:
            tag.append(iter[i]['entities']["sentiment"]["basic"])
          except:
            tag.append(None)
        except:
          continue
    print("Length of errors:",len(err_url))
    int_end_date = int_end_date + 100

    df = pd.DataFrame([date,timestamp,username,userid,tag,message,id])
    df = df.T
    df.columns = ["date","created_at","user_name","user_id", "bear_bull_tag","text","message_id"]

    df = df[(df['date'] <= int_start_date) & (df['date'] >= int_end_date)]
    
    if len(err_url)>0:
      print("Errors Found:",len(err_url))
      df1 = self.errorExtractor(err_url)
      frames = [df,df1]
      df = pd.concat(frames)
    # Deleting the unnecessary data
    df.drop('date',axis = 1, inplace=True)
    df.drop_duplicates(keep="first",inplace=True) #Deleting duplicates
    df.to_csv(f'****/{Symbol.split(".")[0]}.csv', index=False)
  
  def errorExtractor(self,urllist):
    err = []
    int_start_date = int(datetime.strptime(self.StartDate,"%m/%d/%Y").strftime('%Y%d%m'))

    int_end_date = int(datetime.strptime(self.EndDate,"%m/%d/%Y").strftime('%Y%d%m'))

    for url in urllist:
      try:
        jsonfil = requests.get(url).json()
        err.append(jsonfil['messages'])
      except:
        continue
    date = []
    id = []
    message = []
    timestamp = []
    username = []
    tag = []
    userid = []
    for iter in err:
      for i in range(0,31):
        try:
          date.append(int(datetime.strptime(iter[i]['created_at'],"%Y-%m-%dT%H:%M:%S%z").strftime('%Y%d%m'))) 
          # Created a temporary date column to manage the dataframe. Inspired from Anshuls implementation.
          message.append(iter[i]['body'])
          timestamp.append(iter[i]['created_at'])
          username.append(iter[i]['user']["username"])
          userid.append(iter[i]['user']["id"])
          id.append(iter[i]['id'])
          try:
            tag.append(iter[i]['entities']["sentiment"]["basic"])
          except:
            tag.append(None)
        except:
          continue
    
    int_end_date = int_end_date + 100

    df = pd.DataFrame([date,timestamp,username,userid,tag,message,id])
    df = df.T
    df.columns = ["date","created_at","user_name","user_id", "bear_bull_tag","text","message_id"]
    df = df[(df['date'] <= int_start_date) & (df['date'] >= int_end_date)]
    return df
    
  def Driver(self):
    # Driver block to initiate the extraction
    timesmark = []
    tickers = []
    for symbol in self.Symbols:
      print(f'[INFO] Extracting Tweets for {symbol}')
      #print(f'[INFO] It may run into error if incorrect format for symbol or date is entered')
      s = time.time()
      self.ExtractorDate(symbol)
      e = time.time()
      print("Time elaplsed in extraction for",symbol,"from",self.FinalDate,"to",self.InitialDate,"is:",e-s)

start = "10/05/2022"
end = "01/01/2015"
symbols = ['List of stock symbols']

extract = TweetExtractor(start,end,symbols)
extract.Driver()
