import datetime
import sqlite3
import os
import time
import requests
import schedule

url = 'https://api.ivao.aero/getdata/whazzup/whazzup.txt'
dir_path = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(dir_path, 'data.db'))
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS plots
                  (vid INTEGER, lat REAL, lon REAL, alt INTEGER, date TEXT);
               """)


def main():
    for line in requests.get(url).text.splitlines():
        if 'PILOT' in line:
            date = datetime.datetime.now().isoformat(' ')
            line = line.split(':')
            cursor.execute('INSERT INTO plots VALUES (?, ?, ?, ?, ?);',
                           (line[1], line[5], line[6], line[7], date))
    db.commit()

schedule.every(15).seconds.do(main)

print('Starting download.')
while True:
    schedule.run_pending()
    time.sleep(1)
