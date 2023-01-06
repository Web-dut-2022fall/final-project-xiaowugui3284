# -*- coding:utf-8 -*-
import os
from flask import Flask, render_template, json, request, redirect, session, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = r'E:\JetBrains\PycharmProjects\ClassMag\static\image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ksy1452254'
app.config['MYSQL_DATABASE_DB'] = 'mclass'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

app.secret_key = 'you will never know'
mysql.init_app(app)

# 删除成员
@app.route('/delete_user_from_class', methods=['POST'])
def delete_user_from_class():
    try:
        if session.get('manager'):
            u_id = request.form['Uid']
            c_id = request.form['Cid']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteUser_fromClass', (u_id, c_id))
            result = cursor.fetchall()
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': u'发送信息错误'})
        else:
            return render_template('error.html', error=u'未授权访问')
    except Exception as e:
        print e
        return json.dumps({'status': str(e)})
    finally:
        cursor.close()
        conn.close()


# 模糊查询班级成员信息,按性别查找
@app.route('/search_user_by_sex', methods=['POST'])
def search_user_by_sex():
    try:
        if session.get('manager')or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            c_id = request.form['Id']
            key = request.form['keyword']
            cursor.callproc('sp_searchUser_bySex', (c_id, key))
            users = cursor.fetchall()
            users_dict = []
            for m in users:
                c_dict = {
                    'Id': m[0],
                    'Name': m[1],
                    'Sex': m[2],
                    'Loc': m[3],
                    'Email': m[4]
                }
                users_dict.append(c_dict)
            return json.dumps(users_dict)
        else:
            return render_template('error.html', error=u'未授权访问')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))


# 模糊查询班级成员信息,按姓名查找
@app.route('/search_user_by_name', methods=['POST'])
def search_user_by_name():
    try:
        if session.get('manager') or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            c_id = request.form['Id']
            key = request.form['keyword']
            cursor.callproc('sp_searchUser_byName', (c_id, key))
            users = cursor.fetchall()
            users_dict = []
            for m in users:
                c_dict = {
                    'Id': m[0],
                    'Name': m[1],
                    'Sex': m[2],
                    'Loc': m[3],
                    'Email': m[4]
                }
                users_dict.append(c_dict)
            return json.dumps(users_dict)
        else:
            return render_template('error.html', error=u'未授权访问')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))


# 模糊查询班级成员信息,按居住地查找
@app.route('/search_user_by_loc', methods=['POST'])
def search_user_by_loc():
    try:
        if session.get('manager')or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            c_id = request.form['Id']
            key = request.form['keyword']
            cursor.callproc('sp_searchUser_byLoc', (c_id, key))
            users = cursor.fetchall()
            users_dict = []
            for m in users:
                c_dict = {
                    'Id': m[0],
                    'Name': m[1],
                    'Sex': m[2],
                    'Loc': m[3],
                    'Email': m[4]
                }
                users_dict.append(c_dict)
            return json.dumps(users_dict)
        else:
            return render_template('error.html', error=u'未授权访问')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))


# 精确查询班级成员信息,按电子邮箱查找
@app.route('/search_user_by_email', methods=['POST'])
def search_user_by_email():
    try:
        if session.get('manager')or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            c_id = request.form['Id']
            key = request.form['keyword']
            cursor.callproc('sp_searchUser_byEmail', (c_id, key))
            users = cursor.fetchall()
            users_dict = []
            for m in users:
                c_dict = {
                    'Id': m[0],
                    'Name': m[1],
                    'Sex': m[2],
                    'Loc': m[3],
                    'Email': m[4]
                }
                users_dict.append(c_dict)
            return json.dumps(users_dict)
        else:
            return render_template('error.html', error=u'未授权访问')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))


# 转到班级公告页面
@app.route('/show_class_notice')
def show_class_notice():
    return render_template('usernotice.html')


# 转到班级成员页面
@app.route('/show_classmate')
def show_classmate():
    return render_template('userclass.html')


# 增加班级成员
@app.route('/user_add_into_class', methods=['POST'])
def user_add_into_class():
    try:
        if session.get('user'):
            Uid = session.get('user')
            Cid = request.form['Cid']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addClassmate', (Uid, Cid))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': '加入成功！'})
            else:
                return json.dumps({'message': '用户已存在于该班级！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 获得所有的该班级的成员信息
@app.route('/get_user_by_class', methods=['POST'])
def get_user_by_class():
    try:
        if session.get('manager') or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            c_id = request.form['Id']
            cursor.callproc('sp_getUser_byClass', (c_id,))
            users = cursor.fetchall()
            users_dict = []
            for m in users:
                user_dict = {
                    'Id': m[0],
                    'Name': m[1],
                    'Sex': m[2],
                    'Loc': m[3],
                    'Email': m[4]
                }
                users_dict.append(user_dict)
            return json.dumps(users_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 增加公告
@app.route('/add_notice', methods=['POST'])
def add_notice():
    try:
        if session.get('manager'):
            title = request.form['Title']
            desc = request.form['Desc']
            class_id = request.form['ClassId']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createNotice', (title, desc, class_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': "OK"})
            else:
                return json.dumps({'status': "该公告已经存在！"})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 删除公告
@app.route('/delete_notice', methods=['POST'])
def delete_notice():
    try:
        if session.get('manager'):
            no_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteNotice', (no_id, ))
            result = cursor.fetchall()
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '发送信息错误！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 获得所有的该班级的公告信息
@app.route('/get_notice_by_class', methods=['POST'])
def get_notice_by_class():
    try:
        if session.get('manager') or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            class_id = request.form['Id']
            cursor.callproc('sp_getallNotice', (class_id, ))
            notices = cursor.fetchall()
            notices_dict = []
            for m in notices:
                c_dict = {
                    'Id': m[0],
                    'Title': m[1],
                    'Desc': m[2],
                    'Date': m[3]
                }
                notices_dict.append(c_dict)
            return json.dumps(notices_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 获得某个特定id的公告信息
@app.route('/get_notice_byid', methods=['POST'])
def get_notice_byid():
    try:
        if session.get('manager') or session.get('user'):
            no_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getNotice_byid', (no_id,))
            result = cursor.fetchall()
            notice = list()
            notice.append({'Title': result[0][0], 'Desc': result[0][1]})

            return json.dumps(notice)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 更新公告信息
@app.route('/update_notice', methods=['POST'])
def update_notice():
    try:
        if session.get('manager'):
            no_title = request.form['Title']
            no_desc = request.form['Desc']
            no_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateNotice', (no_id, no_title, no_desc))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '该条公告已经存在！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 模糊查询公告信息
@app.route('/search_notice', methods=['POST'])
def search_notice():
    try:
        if session.get('manager') or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            class_id = request.form['Id']
            key = request.form['keyword']
            cursor.callproc('sp_searchNotice', (class_id, key))
            notices = cursor.fetchall()
            notices_dict = []
            for m in notices:
                c_dict = {
                    'Id': m[0],
                    'Title': m[1],
                    'Desc': m[2],
                    'Date': m[3]
                }
                notices_dict.append(c_dict)
            return json.dumps(notices_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 增加班级
@app.route('/add_class', methods=['POST'])
def add_class():
    try:
        if session.get('manager'):
            title = request.form['classTitle']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createClass', (title,))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '该班级已经存在！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 删除班级
@app.route('/delete_class', methods=['POST'])
def delete_class():
    try:
        if session.get('manager'):
            class_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteClass', (class_id, ))
            result = cursor.fetchall()
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '该班级已经存在！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 获得所有的班级信息
@app.route('/get_all_class')
def get_all_class():
    try:
        if session.get('manager') or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getallClass', )
            classes = cursor.fetchall()
            classes_dict = []
            for m in classes:
                c_dict = {
                    'Id': m[0],
                    'Title': m[1]
                }
                classes_dict.append(c_dict)
            return json.dumps(classes_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 获得某个特定id的班级信息
@app.route('/get_class_byid', methods=['POST'])
def get_class_byid():
    try:
        if session.get('manager') or session.get('user'):
            class_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getClass_byid', (class_id,))
            result = cursor.fetchall()
            cls = list()
            cls.append({'Id': result[0][0], 'Title': result[0][1]})
            return json.dumps(cls)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 更新班级信息
@app.route('/update_class', methods=['POST'])
def update_class():
    try:
        if session.get('manager'):
            class_title = request.form['Title']
            class_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateClass_byid', (class_id, class_title))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '该班级已经存在！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 模糊查询班级信息
@app.route('/search_class', methods=['POST'])
def search_class():
    try:
        if session.get('manager') or session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            key = request.form['keyword']
            cursor.callproc('sp_searchClass', (key, ))
            classes = cursor.fetchall()
            classes_dict = []
            for m in classes:
                c_dict = {
                    'Id': m[0],
                    'Title': m[1]
                }
                classes_dict.append(c_dict)
            return json.dumps(classes_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 返回管理班级主页
@app.route('/show_manage_class')
def show_manage_class():
    return render_template('magclass.html')


# 返回管理班级成员主页
@app.route('/show_manage_classmate')
def show_manage_classmate():
    return render_template('magclassmate.html')


# 更改管理员密码
@app.route('/update_manager_psw', methods=['POST'])
def update_manager_psw():
    try:
        if session.get('manager'):
            manager_id = session.get('manager')
            conn = mysql.connect()
            cursor = conn.cursor()
            Oldpsw = request.form['Oldpsw']
            Newpsw = request.form['Newpsw']
            cursor.callproc('sp_getManagerpsw_byid', (manager_id,))
            data = cursor.fetchall()
            if len(data) > 0:
                if check_password_hash(str(data[0][0]), Oldpsw):
                    psw = generate_password_hash(Newpsw)
                    cursor.callproc('sp_updateManagerpsw', (manager_id, psw))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        return json.dumps({'status': '修改成功！'})
                    else:
                        return json.dumps({'status': '修改失败！'})
                else:
                    return json.dumps({'status': '原密码输入错误！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 更改用户密码
@app.route('/update_user_psw', methods=['POST'])
def update_user_psw():
    try:
        if session.get('user'):
            user_id = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            Oldpsw = request.form['Oldpsw']
            Newpsw = request.form['Newpsw']
            cursor.callproc('sp_getUserpsw_byid', (user_id,))
            data = cursor.fetchall()
            if len(data) > 0:
                if check_password_hash(str(data[0][0]), Oldpsw):
                    psw = generate_password_hash(Newpsw)
                    cursor.callproc('sp_updateUserpsw', (user_id, psw))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()               # 需要确认修改信息，否则没用！！
                        return json.dumps({'status': '密码修改成功！'})
                else:
                    return json.dumps({'status': '原密码输入错误！'})
            return json.dumps({'status': '密码修改失败！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))


# 查找管理员信息
@app.route('/search_manager', methods=['POST'])
def search_manager():
    try:
        if session.get('manager'):
            conn = mysql.connect()
            cursor = conn.cursor()
            key = request.form['keyword']
            cursor.callproc('sp_searchManager', (key, ))
            managers = cursor.fetchall()
            managers_dict = []
            if cursor.rowcount is 0:  # 表示查找集合为空
                return json.dumps(managers_dict)
            else:
                for m in managers:
                    m_dict = {
                        'Id': m[0],
                        'Account': m[1],
                        'Level': m[2]
                    }
                    managers_dict.append(m_dict)
                return json.dumps(managers_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 获得所有的管理员信息
@app.route('/get_all_manager')
def get_all_manager():
    try:
        if session.get('manager'):
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getallManager', )
            managers = cursor.fetchall()
            managers_dict = []
            if cursor.rowcount is 0:  # 表示查找集合为空
                return json.dumps(managers_dict)
            else:
                for m in managers:
                    m_dict = {
                        'Id': m[0],
                        'Account': m[1],
                        'Level': m[2]
                    }
                    managers_dict.append(m_dict)
                return json.dumps(managers_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/get_manager_byid')
def get_manager_byid():
    try:
        if session.get('manager'):
            manager_id = session.get('manager')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getManager_byid', (manager_id,))
            result = cursor.fetchall()
            manager = list()
            manager.append({'Id': result[0][0], 'Account': result[0][1], 'Level': result[0][2]})
            return json.dumps(manager)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 返回root管理员主页
@app.route('/show_manager_home')
def show_manager_home():
    m = session.get('manager')
    if m is 1:
        return render_template('root_maghome.html')
    elif m > 0:
        return render_template('ord_maghome.html')
    else:
        return render_template('error.html', error=u'未授权访问！')


#  root权限的管理员添加普通管理员功能，不成功时需要返回错误信息
@app.route('/create_manager', methods=['POST'])
def create_manager():
    try:
        if session.get('manager'):      # 检测会话是否有效
            account = request.form['Account']
            password = request.form['Password']
            conn = mysql.connect()
            cursor = conn.cursor()      # 连接数据库，获得数据指针
            hash_psd = generate_password_hash(password)
            cursor.callproc('sp_createManager', (account, hash_psd))
            data = cursor.fetchall()    # 获取数据库返回信息
            if len(data) == 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '管理员已经存在！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 管理员登录功能，登陆失败时返回错误信息
@app.route('/manager_validate_login', methods=['POST'])
def manager_validate_login():
    try:
        account = request.form['inputAccount']
        password = request.form['inputPassword']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_validateManagerlogin', (account,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][1]), password):
                session['manager'] = data[0][0]
                return redirect('/show_manager_home')
            else:
                return render_template('error.html', error=u'账号或密码错误！')
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 注销功能，退出登录
@app.route('/manager_logout')
def manager_logout():
    session.pop('manager', None)    # 销毁会话
    return redirect('/')


@app.route('/delete_manager', methods=['POST'])
def delete_manager():
    try:
        if session.get('manager'):
            manager_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteManager', (manager_id, ))
            result = cursor.fetchall()
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '删除失败！'})
        else:
            return render_template('error.html', u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/delete_memo', methods=['POST'])
def delete_memo():
    try:
        if session.get('user'):
            memo_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteMemo', (memo_id, ))
            result = cursor.fetchall()
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '删除失败！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/add_memo', methods=['POST'])
def add_memo():
    try:
        if session.get('user'):
            _title = request.form['Title']
            _description = request.form['Desc']
            _user = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createMemo', (_title, _description, _user))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '该备忘录已经存在！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/get_user_memo')
def get_user_memo():
    try:
        if session.get('user'):
            m_user = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getMemo_byuser', (m_user, ))
            memos = cursor.fetchall()
            memos_dict = []
            for memo in memos:
                memo_dict = {
                    'Id': memo[0],
                    'Title': memo[1],
                    'Desc': memo[2],
                    'Date': memo[3]
                }
                memos_dict.append(memo_dict)
            return json.dumps(memos_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/get_memo_byid', methods=['POST'])
def get_memo_byid():
    try:
        if session.get('user'):
            memo_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getMemo_byid', (memo_id,))
            result = cursor.fetchall()
            memo = list()
            memo.append({'Id': result[0][0], 'Title': result[0][1], 'Desc': result[0][2]})
            return json.dumps(memo)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/update_memo', methods=['POST'])
def update_memo():
    try:
        if session.get('user'):
            user_id = session.get('user')
            memo_title = request.form['Title']
            memo_desc = request.form['Desc']
            memo_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateMemo', ( memo_id,memo_title, memo_desc, user_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '发生错误！'})
    except Exception as e:
        print e
        return render_template('error.html', error=u'未授权访问！')
    finally:
        cursor.close()
        conn.close()


@app.route('/search_memo', methods=['POST'])
def search_memo():
    try:
        if session.get('user'):
            user_id = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            key = request.form['keyword']
            cursor.callproc('sp_searchMemo', (key, user_id))
            memos = cursor.fetchall()
            memos_dict = []
            if cursor.rowcount is 0:       # 表示查找集合为空
                return json.dumps(memos_dict)
            else:
                for memo in memos:
                    memo_dict = {
                        'Id': memo[0],
                        'Title': memo[1],
                        'Description': memo[2],
                        'Date': memo[3]
                    }
                    memos_dict.append(memo_dict)
                return json.dumps(memos_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_signin')
def show_signin():
    return render_template('signin.html')


@app.route('/show_manager_log')
def show_manager_log():
    return render_template('manager_login.html')


@app.route('/show_user_home')
def show_user_home():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return json.dumps({'error': 'session error'})


# 注册功能，针对用户的注册，不成功时需要返回错误信息
@app.route('/sign_in', methods=['POST'])
def sign_in():
    try:
        account = request.form['inputTel']
        password = request.form['inputPassword']
        if account and password:              # 传入数据，检查如果不空
            conn = mysql.connect()
            cursor = conn.cursor()          # 连接数据库，获得数据指针
            hash_psd = generate_password_hash(password)
            cursor.callproc('sp_createUser', (account, hash_psd))
            data = cursor.fetchall()        # 获取数据库返回信息
            if len(data) == 0:
                conn.commit()
                return json.dumps({'message': '用户创建成功!'})
            else:
                return json.dumps({'message': data[0]})
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 登录功能，登陆失败时返回错误信息
@app.route('/user_validate_login', methods=['POST'])
def user_validate_login():
    try:
        tel = request.form['inputTel']
        password = request.form['inputPassword']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_validateUserlogin', (tel,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][1]), password):
                session['user'] = data[0][0]
                return redirect('/show_user_home')
            else:
                return render_template('error.html', error=u'账户错误！')
        else:
            return render_template('error.html', error=u'密码错误！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 注销功能，退出登录
@app.route('/user_logout')
def user_logout():
    session.pop('user', None)    # 销毁会话
    return redirect('/')


# 获得用户的备忘录信息
@app.route('/get_user_info')
def get_user_info():
    try:
        if session.get('user'):
            user_id = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getUser_byid', (user_id, ))
            result = cursor.fetchall()
            user_info = list()
            user_info.append({'Name': result[0][0], 'Sex': result[0][1],
                              'Loc': result[0][2], 'Email': result[0][3]})
            return json.dumps(user_info)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    try:
        if session.get('user'):
            user_id = session.get('user')
            user_name = request.form['Name']
            user_sex = request.form['Sex']
            user_loc = request.form['Loc']
            user_email = request.form['Email']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateUserinfo', (user_id, user_name, user_sex, user_loc, user_email))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '更新失败！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
