from flask import Flask, flash, redirect, render_template, request, url_for ,session,jsonify, json,Blueprint, current_app as app
from models.database import *
import datetime, math ,os,base64, secrets
from datetime import date, timedelta,datetime
from flask_cors import CORS
from pathlib import Path, PurePath
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx','doc', 'xls','xlsx'])
IMAGE_FOLDER = os.path.join('static', 'image')

year=str(datetime.today().strftime('%Y'))
now=str(datetime.today().strftime('%Y-%m-%d'))
token=secrets.token_hex()

evacuation_centers = Blueprint('evacuation_centers',__name__)
CORS(evacuation_centers)
evacuation_centers.secret_key = '&^##*($top_secret&&#(@(@":fhakdog'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@evacuation_centers.route('/get_evaction_centers_data', methods=['GET', 'POST'])
def get_evaction_centers_data():
    try:
        sel="select * from tbl_evacuation_centers"
        rd=pyread(sel)
        return jsonify(rd)
    except Exception as e:
        prnt_R(e)
        return e

@evacuation_centers.route('/save_evacuationCenter', methods = ['POST','GET'])
def save_evacuationCenter():
    try:
        p = request.form
        print(p)
        rd = 0;
        if p['id'] == 0 or p['id'] == '0':
            print("insert")
            ins_q = """insert into tbl_evacuation_centers 
                        (evac_building_name,evac_address,evac_lat,evac_long,capacity,max_capacity,evac_status) 
                            values
                        (
                            '"""+str(p['evacuation_building_name'])+"""',
                            '"""+str(p['evacuation_address'])+"""',
                            '"""+str(p['evacuation_lat'])+"""',
                            '"""+str(p['evacuation_long'])+"""',
                            '"""+str(p['evacuation_capacity'])+"""',
                            '"""+str(p['evacuation_max_capacity'])+"""',
                            '"""+str(p['status'])+"""') RETURNING id
                    """
            rd = crud_p_lastInsertedID(ins_q)
            for filename_array in request.files:
                prnt_R("inside")
                file=request.files[filename_array]
                n_path = Path(__file__).parent / "../static/building_img" / str(rd)
                n_path.resolve()

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    if not os.path.exists(n_path):
                        os.mkdir(n_path)
                        app.config['UPLOAD_FOLDER']=n_path
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        prnt_B(filename)
                    else:
                        app.config['UPLOAD_FOLDER']=n_path
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        
                    location1="building_img//"+str(rd)
                    location1.replace("//", "\\\\");
                    location=location1+"/"+filename
                    path_location=location.replace("/", "\\\\");
                    prnt_R(path_location)
                    update="update tbl_evacuation_centers set evac_image_path='"+str(path_location)+"' where id='"+str(rd)+"'"
                    crud_p(update)
            message = "Insert"
        else:
            print("update")
            upt_q = """
                    update tbl_evacuation_centers set 
                        evac_building_name = '"""+str(p['evacuation_building_name'])+"""',
                        evac_address = '"""+str(p['evacuation_address'])+"""',
                        evac_lat = '"""+str(p['evacuation_lat'])+"""',
                        evac_long = '"""+str(p['evacuation_long'])+"""',
                        capacity = '"""+str(p['evacuation_capacity'])+"""',
                        max_capacity ='"""+str(p['evacuation_max_capacity'])+"""',
                        evac_status ='"""+str(p['status'])+"""'
                        where id = '"""+str(p['id'])+"""'
                    """
            crud_p(upt_q)
            prnt_B(rd)
            for filename_array in request.files:
                prnt_R("inside")
                file=request.files[filename_array]
                n_path = Path(__file__).parent / "../static/building_img" / str(p['id'])
                n_path.resolve()

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    if not os.path.exists(n_path):
                        os.mkdir(n_path)
                        app.config['UPLOAD_FOLDER']=n_path
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        prnt_B(filename)
                    else:
                        app.config['UPLOAD_FOLDER']=n_path
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        
                    location1="building_img//"+str(p['id'])
                    location1.replace("//", "\\\\");
                    location=location1+"/"+filename
                    path_location=location.replace("/", "\\\\");
                    prnt_R(path_location)
                    update="update tbl_evacuation_centers set evac_image_path='"+str(path_location)+"' where id='"+str(p['id'])+"'"
                    crud_p(update)
            message = "Update"

        return jsonify({"message":message, "status": 200})
    except Exception as e:
        prnt_R(e)
        return e

@evacuation_centers.route('/get_evaction_centers_public', methods=['GET', 'POST'])
def get_evaction_centers_public():
    try:
        sel="select * from tbl_evacuation_centers where evac_status = 0"
        rd=pyread(sel)
        return jsonify(rd)
    except Exception as e:
        prnt_R(e)
        return e


@evacuation_centers.route('/delete_evacuation', methods = ['POST','GET'])
def delete_evacuation():
    try:
        p = json.loads(request.data)
        del_q ="delete from tbl_evacuation_centers where id = '"+str(p['id'])+"'"
        crud_p(del_q)
        return jsonify({"status":200,"data":"success"})
    except Exception as e:
        prnt_R(e)
        return e

