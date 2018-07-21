#!/usr/bin/python3

#All credit to setndex (youtube)
#Python program to train the chatbot

import sqlite3 
import pandas as pd

timeframes = ['2011-07']

for timeframe in timeframes: 
  connection = sqlite3.connect('/home/lara/dataset/ai-brain/{}.db'.format(timeframe))
  c = connection.cursor()
  limit = 5000
  last_unix = 0
  cur_length = limit 
  counter = 0
  test_done = False 
  while cur_length == limit: 
    df = pd.read_sql("""SELECT * FROM parent_reply WHERE unix > {} AND 
                      parent not null AND score > 0 
 		      ORDER BY unix ASC LIMIT {}""".format(last_unix, limit), connection)
    last_unix = df.tail(1)['unix'].values[0]
    cur_length = len(df)
    if not test_done:
      with open("/home/lara/dataset/ai-brain/test.from", 'a', encoding='utf8') as f:
        for content in df['parent'].values:
          f.write(content+'\n')

      with open("/home/lara/dataset/ai-brain/test.to", 'a', encoding='utf8') as f:
        for content in df['comment'].values:
          f.write(content+'\n')
      test_done = True
    else: 
      with open("/home/lara/dataset/ai-brain/train.from", 'a', encoding='utf8') as f:
        for content in df['parent'].values:
          f.write(content+'\n')

      with open("/home/lara/dataset/ai-brain/train.to", 'a', encoding='utf8') as f:
        for content in df['comment'].values:
          f.write(content+'\n')
  
    counter += 1
    if counter % 20 == 0:
      print(counter*limit, 'Rows completed so far')
