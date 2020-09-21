from fastapi import FastAPI
from pydantic import BaseModel
import pymysql
import redis
import uvicorn
import uuid
import hashlib

db = pymysql.connect("192.168.37.111", "root", "huayang", "teppo")
cursor = db.cursor()

app = FastAPI()

redis_pool = redis.ConnectionPool(host='192.168.37.111', port=6379, max_connections=100)


class ManageKey(BaseModel):
    key: str
    password: str
    num = int = 1


class Key(BaseModel):
    key: str
    userId: str = None


class Success(BaseModel):
    key: str
    productName: str
    price: str
    site: str
    date: str


class getSuccess(BaseModel):
    start: int
    end: int


class abckData(BaseModel):
    text: str


class getAbckData(BaseModel):
    key: str
    num: int = 1


@app.post("/api")
def hello(key: Key):
    print(key.userId == None)
    sqlStr1 = 'INSERT INTO `keys`(teppo_key, user_id) values ("123-456", "iyou1")'
    sqlStr = 'select * from `keys` where teppo_key = "123-45"'
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    print(len(result))
    db.commit()
    return "hello world"


@app.post("/activeKey")
def activeKey(key: Key):
    sqlStr = f'select * from `keys` where teppo_key = "{key.key}"'
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    if len(result) == 0:
        return {
            'code': 400,
            'message': 'Key was error'
        }
    else:
        if result[0][1] == '' or result[0][1] == None:
            sqlStr1 = f'update `keys` set user_id = "{key.userId}" where teppo_key = "{key.key}"'
            cursor.execute(sqlStr1)
            db.commit()
            return {
                'code': 200,
                'message': 'success'
            }
        else:
            return {
                'code': 400,
                'message': 'key was used'
            }


@app.post("/putSuccess")
def putSuccess(successData: Success):
    sqlStr = f'INSERT INTO teppo_success(teppo_key, productName, price, site, su_date) values ("{successData.key}","{successData.productName}","{successData.price}","{successData.site}","{successData.date}")'
    cursor.execute(sqlStr)
    db.commit()
    return {
        'code': 200
    }


@app.post("/getAllSuccess")
def getAllSuccess(data: getSuccess):
    sqlStr = f'select * from teppo_success limit {data.start},{data.end}'
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    return result


@app.post("/putAbck")
def putAbck(data: abckData):
    try:
        conn = redis.Redis(connection_pool=redis_pool)
        for i in range(2):
            conn.lpush('teppo_abck', data.text)
    except Exception as e:
        print('Redis error:' + str(e))


@app.get("/getState/{country}")
def getState(country: str):
    usState = [
        {'value': 'AL', 'text': 'Alabama'},
        {'value': 'AK', 'text': 'Alaska'},
        {'value': 'AZ', 'text': 'Arizona'},
        {'value': 'AR', 'text': 'Arkansas'},
        {'value': 'CA', 'text': 'California'},
        {'value': 'CO', 'text': 'Colorado'},
        {'value': 'CT', 'text': 'Connecticut'},
        {'value': 'DE', 'text': 'Delaware'},
        {'value': 'DC', 'text': 'District of Columbia'},
        {'value': 'FL', 'text': 'Florida'},
        {'value': 'GA', 'text': 'Georgia'},
        {'value': 'HI', 'text': 'Hawaii'},
        {'value': 'ID', 'text': 'Idaho'},
        {'value': 'IL', 'text': 'Illinois'},
        {'value': 'IN', 'text': 'Indiana'},
        {'value': 'IA', 'text': 'Iowa'},
        {'value': 'KS', 'text': 'Kansas'},
        {'value': 'KY', 'text': 'Kentucky'},
        {'value': 'LA', 'text': 'Louisiana'},
        {'value': 'ME', 'text': 'Maine'},
        {'value': 'MD', 'text': 'Maryland'},
        {'value': 'MA', 'text': 'Massachusetts'},
        {'value': 'MI', 'text': 'Michigan'},
        {'value': 'MN', 'text': 'Minnesota'},
        {'value': 'MS', 'text': 'Mississippi'},
        {'value': 'MO', 'text': 'Missouri'},
        {'value': 'MT', 'text': 'Montana'},
        {'value': 'NE', 'text': 'Nebraska'},
        {'value': 'NV', 'text': 'Nevada'},
        {'value': 'NH', 'text': 'New Hampshire'},
        {'value': 'NJ', 'text': 'New Jersey'},
        {'value': 'NM', 'text': 'New Mexico'},
        {'value': 'NY', 'text': 'New York'},
        {'value': 'NC', 'text': 'North Carolina'},
        {'value': 'ND', 'text': 'North Dakota'},
        {'value': 'OH', 'text': 'Ohio'},
        {'value': 'OK', 'text': 'Oklahoma'},
        {'value': 'OR', 'text': 'Oregon'},
        {'value': 'PA', 'text': 'Pennsylvania'},
        {'value': 'RI', 'text': 'Rhode Island'},
        {'value': 'SC', 'text': 'South Carolina'},
        {'value': 'SD', 'text': 'South Dakota'},
        {'value': 'TN', 'text': 'Tennessee'},
        {'value': 'TX', 'text': 'Texas'},
        {'value': 'UT', 'text': 'Utah'},
        {'value': 'VT', 'text': 'Vermont'},
        {'value': 'VA', 'text': 'Virginia'},
        {'value': 'WA', 'text': 'Washington'},
        {'value': 'WV', 'text': 'West Virginia'},
        {'value': 'WI', 'text': 'Wisconsin'},
        {'value': 'WY', 'text': 'Wyoming'}
    ]
    if country == 'us':
        return usState
    else:
        return {
            'code': 404
        }


@app.post("/iyouGenKey")
def iyouGenKey(data: ManageKey):
    new_key = []
    mm = hashlib.md5()
    if data.password == 'teppoisbest' and data.key == '123-456':
        for i in range(int(data.num)):
            text = str(uuid.uuid4())
            mm.update(text.encode("utf-8"))
            result = list(str(mm.hexdigest()))
            result.insert(8, '-')
            result.insert(13, '-')
            result.insert(18, '-')
            result.insert(23, '-')
            result = ''.join(result)
            new_key.append(result)
    else:
        return {
            'code': 404
        }
    sqlData = []
    for i in new_key:
        sqlstr1 = f' ("{i}")'
        sqlData.append(sqlstr1)
    sqlstr2 = ','.join(sqlData)
    sqlstr3 = 'insert into teppo_status (teppo_key) values ' + sqlstr2
    cursor.execute(sqlstr3)
    db.commit()
    sqlstr5 = 'insert into `keys` (teppo_key) values ' + sqlstr2
    cursor.execute(sqlstr5)
    db.commit()
    return {
        'code': 200,
        'data': new_key
    }


@app.post("/getAbck")
def getAbck(data: getAbckData):
    sqlStr = f'select * from teppo_status where teppo_key = "{data.key}"'
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    if len(result) == 0:
        return {
            "code": 404
        }

    elif int(result[0][1]) == 0:
        return {
            "code": 403
        }
    else:
        conn = redis.Redis(connection_pool=redis_pool)
        result = conn.lrange('teppo_abck', 0, int(data.num) - 1)
        conn.ltrim('teppo_abck', int(data.num), -1)
        return result


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
