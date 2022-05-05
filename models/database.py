import psycopg2
import psycopg2.extras
import os, sys

if sys.platform.lower() == "win32":
    os.system('color')

class style():
    BLACK = lambda x: '\033[30m' + str(x)
    RED = lambda x: '\033[31m' + str(x)
    GREEN = lambda x: '\033[32m' + str(x)
    YELLOW = lambda x: '\033[33m' + str(x)
    BLUE = lambda x: '\033[36m' + str(x)
    MAGENTA = lambda x: '\033[35m' + str(x)
    WHITE = lambda x: '\033[37m' + str(x)
    UNDERLINE = lambda x: '\033[4m' + str(x)
    RESET = lambda x: '\033[0m' + str(x)

def prnt_Y(msg):
	clr=print(style.YELLOW(msg),style.RESET(''))
	return clr

def prnt_R(msg):
	clr=print(style.RED(msg),style.RESET(''))
	return clr

def prnt_W(msg):
	clr=print(style.MAGENTA(msg),style.RESET(''))
	return clr

def prnt_B(msg):
	clr=print(style.BLUE(msg),style.RESET(''))
	return clr

def prnt_G(msg):
	clr=print(style.GREEN(msg),style.RESET(''))
	return clr

try:
	conn = psycopg2.connect(host='localhost',database='db_lnengage',user='postgres',password='')
	print("Successfuly Connected to Database")
except Exception as e:
	print("Failed to connect database try to restart server")


def crud(sql,ar):
	try:
		db = psycopg2.connect(host='localhost',database='db_lnengage',user='postgres',password='')
		con = db.cursor()
		con.execute(sql, ar)
		db.commit()
		prnt_G("Affected rows"+str(con.rowcount))
		if(db.is_connected()):
			db.close()
			con.close()
			print(style.GREEN("Successfuly queried") + style.RESET(""))
		# return "success"
	except Exception as e:
		print(style.RED("posgres error in loading: '"+str(e)+"'") + style.RESET(""))
		return "1062"

def crud_p(sql):
	try:
		db = psycopg2.connect(host='localhost',database='db_lnengage',user='postgres',password='')
		con = db.cursor()
		con.execute(sql)
		db.commit()
		prnt_G("Affected rows"+str(con.rowcount))
		db.close()
		con.close()
		print(style.GREEN("Successfuly queried") + style.RESET(""))
		# return "success"
	except Exception as e:
		print(style.RED("posgres error in loading: '"+str(e)+"'") + style.RESET(""))
		return "1062"

def crud_p_lastInsertedID(sql):
	try:
		db = psycopg2.connect(host='localhost',database='db_lnengage',user='postgres',password='')
		con = db.cursor()
		con.execute(sql)
		db.commit()
		prnt_G("Affected rows"+str(con.rowcount))
		ids = con.fetchone()[0]
		db.close()
		con.close()
		print(style.GREEN("Successfuly queried") + style.RESET(""))
		return ids
	except Exception as e:
		print(style.RED("posgres error in loading: '"+str(e)+"'") + style.RESET(""))
		return "1062"


def pyread(sql):
	try:
		connection = psycopg2.connect(host='localhost',database='db_lnengage',user='postgres',password='')
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		fetch_all_as_dict = lambda cursor: [dict(row) for row in cursor]
		cur.execute(sql) 	
		connection.close();
		return fetch_all_as_dict(cur);

		# with connection.cursor() as cursor:
		# 	# Read a single record
		# 	result = cursor.fetchall()
	except Exception as e:
		print(style.RED("MYSQL error in pyMSQL: '"+str(e)+"'") + style.RESET(""))