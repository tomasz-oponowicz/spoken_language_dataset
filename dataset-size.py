import pandas as pd
import datetime

LANGUAGE_ATTR = 'Language'
DURATION_ATTR = 'Duration'

if __name__ == '__main__':
    results = {}
    data = pd.read_csv('./speech.csv')
    for index, row in data.iterrows():
        lang = row[LANGUAGE_ATTR]
        (h,m,s) = row[DURATION_ATTR].split(':')
        t = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        if lang in results:
            results[lang] += t
        else:
            results[lang] = t
    for k, v in results.items():
        print(k, str(v))
