from flask import Flask, flash, redirect, render_template, request, url_for ,session,jsonify, json
from models.database import *
import math
from datetime import datetime, timedelta


try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

def checkToken(token):
  try:
    sel = "SELECT * FROM tbl_token tt where tt.token = '"+str(token)+"'"
    res = pyread(sel)
    status = "expired"
    now = datetime.today()
    if token!=0 or token !=None or token !="":
      if res:
      	if datetime.strptime(res[0][3],'%Y-%m-%d %H:%M:%S.%f')<now:
          prnt_R("Session expired")
          del_q = "delete from tbl_token where id = '"+str(res[0][0])+"'"
          crud_p(del_q)
          return status
      	else:
          remainingDate=datetime.strptime(res[0][3],'%Y-%m-%d %H:%M:%S.%f')+timedelta(hours=1)
          update = "update tbl_token set time_exp = '"+str(remainingDate)+"' where id = '"+str(res[0][0])+"'"
          prnt_Y(update)
          crud_p(update)
          return res
      else:
        prnt_R('No token')
        return status
    else:
      prnt_R('No token')
      return status

  except Exception as e:
    prnt_R(e)
    return e