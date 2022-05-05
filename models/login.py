from flask import Flask, flash, redirect, render_template, request, url_for ,session,jsonify, json,Blueprint
from models.database import *
import datetime, math ,os,base64, secrets
from datetime import date, timedelta,datetime
from flask_cors import CORS

year=str(datetime.today().strftime('%Y'))
now=str(datetime.today().strftime('%Y-%m-%d'))
token=secrets.token_hex()

login = Blueprint('login',__name__)
CORS(login)
login.secret_key = '&^##*($top_secret&&#(@(@":fhakdog'

@login.route('/credentials', methods=['GET', 'POST'])
def credentials():
    try:
        print("here here")
        p = json.loads(request.data)
        sel="select * from tbl_user where username='"+str(p['username'])+"' and password='"+str(p['password'])+"'"
        rd=pyread(sel)
        prnt_B(rd)
        if rd:
            if rd!="":
                prnt_G("Authenticated!!")
                session['index']=True
                session['sessioned_user']=rd[0]['user_id']
                session['sessioned_token']=token;
                prnt_B(session)
                tkn = insertToken(rd[0]['user_id'],token)
                if tkn ==True:
                    print("trueee")
                    return jsonify({"status":200})
                else:
                    return jsonify({"status":400})
            else:
                prnt_R("username or password doesnt exist1")
                return jsonify({"status":400})
        else:
            prnt_R("username or password doesnt exist2")
            return jsonify({"status":400})
    except Exception as e:
        prnt_R(e)
        return e



def insertToken(log_id,tkn):
    try:
        now=datetime.today()+timedelta(hours=4)
        arg = (log_id,tkn,now)
        insToken = "insert into tbl_token (login_id,token,time_exp) values ('"+str(log_id)+"','"+str(tkn)+"','"+str(now)+"')"
        crud_p(insToken)
        return True
    except Exception as e:
        prnt_R(e)
        return e