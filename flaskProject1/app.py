from flask import *
from captcha.image import ImageCaptcha
from random import randint
import base64
from io import BytesIO
import sqlite3
import time
from email import header
import requests
app = Flask(__name__)


def rom():
    lists = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            '', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
            'W', 'X', 'Y', 'Z']
    chars = ''
    for i in range(4):
        chars += lists[randint(0, 61)]
    image = ImageCaptcha().generate_image(chars)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str=bytes.decode(img_str)
    return (img_str,chars)
def smz(cards,name):
    headers = {"Authorization": "APPCODE ",
               'X-Requested-With': 'XMLHttpRequest',
               'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
    datas = {}
    datas["cardNo"]=cards
    datas["realName"]=name
    r = requests.post("https://zid.market.alicloudapi.com/idcheck/Post", headers=headers, data=datas)
    return r.text

@app.route('/',methods=['GET','POST'])
def index():
    info = []
    imgs,mm=rom()
    seeds=round(time.time() * 1000)
    mm=str.lower(mm)
    sq=sqlite3.connect("data.data")
    sq.cursor()
    sq.execute("INSERT INTO yzm values (?,?);",(seeds,mm))
    sq.commit()
    sq.close()
    if request.method == 'POST':
        act=request.form['act']
        if (act=="smz"):
            sfz=str(request.form["sfz"])
            names=request.form["name"]
            ids=request.form["ids"]
            yzm=request.form["yzm"]
            yzm=str.lower(yzm)
            seed=request.form["seed"]
            sq=sqlite3.connect("data.data")
            sq.cursor()
            try:
                biaoda=sq.execute("SELECT daan from yzm where id=?;",(int(seed),)).fetchall()[0][0]
            except:
                info = ["验证码错误"]
                return render_template("index.html", img_stream=imgs, seed=seeds, info=info)
            sq.close()
            if (yzm==biaoda):
                sq = sqlite3.connect("data.data")
                sq.cursor()
                sq.execute("DELETE FROM yzm where id=?;",(seed,) )
                sq.commit()
                sq.close()
                years=int(time.strftime("%Y", time.localtime()))-int(sfz[6:10])
                if(years>=18):
                    _json=smz(sfz,names)
                    ls=json.loads(_json)
                    ls=ls["result"]["isok"]
                    if(ls==True):
                        sq = sqlite3.connect("data.data")
                        sq.cursor()
                        sq.execute("INSERT INTO player values (?,?);",(ids,seed))
                        sq.commit()
                        sq.close()
                        info=["恭喜！实名认证成功"]
                    else:
                        info=["联网验证失败，请确定输入是否错误。"]

                else:
                    info=["您还没有成年"]
                    return render_template("index.html", img_stream=imgs, seed=seeds, info=info)
            else:
                info=["验证码错误"]
                return render_template("index.html", img_stream=imgs, seed=seeds, info=info)

    return render_template("index.html", img_stream=imgs,seed=seeds,info=info)

@app.route('/api/',methods=['GET','POST'])
def apis():
    act=request.args.get("act")
    user=request.args.get("user")
    logins=request.args.get("logins")
    if(act=="chack"):
        sq=sqlite3.connect("data.data")
        sq.cursor()
        ls=sq.execute("SELECT seed from player where id=?;",(user,)).fetchall()
        if (ls== []):
            ls=sq.execute("SELECT time,day,last from wcn where id=?;",(user,)).fetchall()
            if(ls==[]):
                sq.execute('INSERT INTO wcn values (?,"0",?,?);',(user,time.strftime("%Y-%m-%d", time.localtime()),int(time.time())))
                sq.commit()
                sq.close()
                return "pass"
            else:
                if(ls[0][1]==time.strftime("%Y-%m-%d", time.localtime())):
                    if(int(ls[0][0])>=3600):
                        sq.close()
                        return "no"
                    else:
                        nows=int(time.time())-int(ls[0][2])+int(ls[0][0])
                        if (logins!="t"):
                            sq.execute('UPDATE wcn set time=?,last=? where id=?;',(nows,int(time.time()),user))
                        else:
                            sq.execute('UPDATE wcn set last=? where id=?;', (int(time.time()), user))
                        sq.commit()
                        sq.close()
                        if(nows>=3600):
                            return "no"
                        else:
                            return "pass"

                else:
                    sq.execute('UPDATE wcn set day=?,last=?,time="0" where id=?;',(time.strftime("%Y-%m-%d", time.localtime()),int(time.time()),user))
                    sq.commit()
                    sq.close()
                    return "pass"
        else:
            sq.close()
            return "pass"

@app.route('/chack/',methods=['GET','POST'])
def chack():
    info = []
    if request.method == 'POST':
        act = request.form['act']
        user=request.form['user']
        if(act=="bmd"):
            sq=sqlite3.connect("data.data")
            sq.cursor()
            info=sq.execute("SELECT * from player where id=?;",(user,)).fetchall()
            sq.close()
        if(act=="times"):
            sq = sqlite3.connect("data.data")
            sq.cursor()
            info = sq.execute("SELECT * from wcn where id=?;", (user,)).fetchall()
            sq.close()
        if (info==[]):
            info=["没有查询到结果，请确定输入是否正确。"]
    return render_template("chack.html",info=info)
if __name__ == '__main__':
    app.run(debug=1)
