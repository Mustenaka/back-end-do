import datetime

from flask import Flask, request, jsonify

import fileControl.fileCont as fileControl


app = Flask(__name__)

# 响应数组
errorCode = [
    "operate failed", "operate successful", "An event is about to expire.",
    "Cannot add job to scheduler", "Cannot del job to scheduler", "both cannot add and del job to scheduler"
]



def add_sched(id_job, end_time):
    try:
    # 添加任务调度
        pos_time = (datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") -
                    datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        # job = fileControl.fileControl().writeNote(id_job)
        scheduler.add_job(job, 'date', run_date=pos_time,
                          args=id_job, id=id_job)
    except:
        return "3"


def del_sched(id_job):
    # 取消任务调度
    try:
        scheduler.remove_job(id_job)
    except:
        return "4"


def update_sched(id_job, end_time):
    # 更新任务调度
    try:
        del_sched(id_job)
        add_sched(id_job, end_time)
    except:
        return "5"



@app.route('/')
def hello_world():
    return 'hello world!'


@app.route('/add', methods=['GET', 'POST'])
def get_add():
    if request.method == 'POST':
        try:
            id_user = str(request.json.get('id_user'))
            id_job = str(request.json.get('id_job'))
            id_class = str(request.json.get('id_class'))
            end_time = str(request.json.get('end_time'))
            job_content = str(request.json.get('job_content'))
            fileControl.fileControl().writeJob(
                id_user, id_job, id_class, end_time, job_content
            )
            add_sched(id_job, end_time)
            return 'From POST'
        except:
            return 'ERROR'
    else:
        return '请使用POST请求'


@ app.route('/del', methods=['GET', 'POST'])
def get_del():
    if request.method == 'POST':
        try:
            id_job = str(request.json.get('id_job'))
            fileControl.fileControl().delJobbyID(id_job)
            del_sched(id_job)
            return 'From POST'
        except:
            return 'ERROR'
    else:
        return '请使用POST请求'


@ app.route('/query', methods=['GET', 'POST'])
def get_query():
    if request.method == 'POST':
        try:
            id_job = str(request.json.get('id_job'))
            ans = fileControl.fileControl().readJobbyID(id_job)
            # 查询任务调度情况
            jobs = scheduler.get_jobs()
            print(jobs)
            if ans == "0":
                return jsonify({
                    "error": "Not found anything"
                })
            return jsonify({
                'id_user': ans[0],
                'id_job': ans[1],
                'id_class': ans[2],
                'start_time': ans[3],
                'end_time': ans[4],
                'job_content': ans[5],
            })
        except:
            return 'ERROR'
    else:
        return '请使用POST请求'


@ app.route('/modify', methods=['GET', 'POST'])
def get_modify():
    if request.method == 'POST':
        try:
            id_job = str(request.json.get('id_job'))
            end_time = str(request.json.get('end_time'))
            job_content = str(request.json.get('job_content'))
            update_sched(id_job, end_time)
            fileControl.fileControl().modifybyID(id_job, end_time, job_content)
            return 'From POST'
        except:
            return 'ERROR'
    else:
        return '请使用POST请求'


if __name__ == '__main__':
    # 启动任务调度器
    scheduler = BackgroundScheduler()
    scheduler.start()
    # 启动Flask服务
    app.run(debug=False, host='127.0.0.1', port=5000)
