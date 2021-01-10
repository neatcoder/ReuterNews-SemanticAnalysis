import re
from pymongo import MongoClient


def connection():
    client = MongoClient('', 27017) #Add URI
    db = client.ReuterDb
    collection = db.news
    return collection


def extract(path):
    file = open(path, "r")
    text = file.read()
    file.close()
    return text


def transform(file):
    x = re.findall("(?<=<TITLE>).*(?=</TITLE)", file)
    y = []
    for each in x:
        y.append(re.sub("&.*?>", "", each))
    return y


def load(texts, dbcollection):
    for text in texts:
        obj = {
            'text': text.lower()
        }
        dbcollection.insert_one(obj)


if __name__ == '__main__':
    conn = connection()
    fileOne = extract("reut2-009.sgm")
    fileTwo = extract("reut2-014.sgm")
    t1 = transform(fileOne)
    t2 = transform(fileTwo)
    load(t1, conn)
    load(t2, conn)

