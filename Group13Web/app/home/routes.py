# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import docker
import re
import collections
from kubernetes import client, config


UserPerferenceDict = {}

def get_running_services():

    # services_info_list = [[1,'tracker',"http://127.0.0.1:44711/","/page-service1.html"],[2,'analyzer',"http://34.123.51.246:44712/","/page-service2.html"],[3,'forecast',"http://127.0.0.1:44713/","/page-service3.html"],[4,'currency',"http://34.72.195.117:44714/","/page-service4.html"]]


    config.load_incluster_config()

    v1 = client.CoreV1Api()

    services = v1.list_service_for_all_namespaces(watch=False)

    services_info_list = []
    id = 1

    for service in services.items:
            if (service.status.load_balancer.ingress is not None and str(service.metadata.name) != 'web'):
                    running_service_info = (service.status.load_balancer.ingress)

                    service_name = (service.metadata.name)

                    service_port = service.spec.ports

                    info_list = str(running_service_info[-1]).split(",")

                    ip = info_list[-1].split(":")[-1]

                    ip = ip.replace("}","")

                    service_ip = ip.replace("'","")

                    port_info_list = str(service_port[-1]).split(",")

                    port_info = port_info_list[-1].split(":")[-1]

                    port = port_info.replace("}","")

                    port = port.replace("'","")

                    single_service_list = []

                    single_service_list.append(id)

                    single_service_list.append(service_name)

                    single_service_list.append(("http://"+service_ip+":"+port).replace(" ",""))

                    single_service_list.append('/page-service'+str(id)+'.html')

                    services_info_list.append(single_service_list)
                    id +=1



    return (services_info_list)

@blueprint.route('/index')
@login_required
def index():
    running_services = get_running_services().copy()
    global UserPerferenceDict,visDict,serviceList
    str_current_user = str(current_user)

    if UserPerferenceDict.get(str_current_user) is None:
        UserPerferenceDict.update({str_current_user: running_services.copy()})

    for using_service in UserPerferenceDict.get(str_current_user):
        if using_service not in get_running_services():
            UserPerferenceDict[str_current_user].remove(using_service)
            UserPerferenceDict[str_current_user] = UserPerferenceDict[str_current_user].sort()

    return render_template( 'index.html', segment='index',visibleservices = UserPerferenceDict.get(str_current_user))

@blueprint.route('/<template>',methods=['GET','POST'])
@login_required
def route_template(template):
    running_services = get_running_services().copy()
    global UserPerferenceDict,visDict,serviceList

    str_current_user = str(current_user)

    if UserPerferenceDict.get(str_current_user) is None:


        UserPerferenceDict.update({str_current_user: running_services.copy()})

    for using_service in UserPerferenceDict.get(str_current_user):
        if using_service not in get_running_services():
            UserPerferenceDict[str_current_user].remove(using_service)
            UserPerferenceDict[str_current_user].sort()

        # print(UserPerferenceDict.keys())
    segment = get_segment( request )
    try:
        if template == 'ReadremoveService':
            index = request.form.get("selectedServiceRed")
            servicesInUse = UserPerferenceDict.get(str_current_user).copy()
            servicesCanAdd = []

            for service in running_services:
                if service not in servicesInUse:
                    servicesCanAdd.append(service)


            if index == None:
                return redirect('/page-setting.html')
            index=re.sub('"','',index)

            for i in range(len(servicesInUse)):
                if str(servicesInUse[i][0]) == index:
                    UserPerferenceDict[str_current_user].remove(servicesInUse[i])
                    UserPerferenceDict[str_current_user].sort()

                    break

            print(UserPerferenceDict[str_current_user])
            return redirect('/page-setting.html')
        elif template == 'ReadappendService':
            index = request.form.get("selectedServiceAdd")
            servicesInUse = UserPerferenceDict.get(str_current_user).copy()
            servicesCanAdd = []

            for service in running_services:
                if service not in servicesInUse:
                    servicesCanAdd.append(service)
            if index == None:
                return redirect('/page-setting.html')
            index=re.sub('"','',index)
            for i in range(len(servicesCanAdd)):
                if str(servicesCanAdd[i][0]) == index:
                    # servicesInUse.append([servicesCanAdd[i][0],servicesCanAdd[i][1]])
                    # servicesCanAdd.pop(i)
                    (UserPerferenceDict[str_current_user]).append(servicesCanAdd[i])
                    (UserPerferenceDict[str_current_user]).sort()
                    break
            print(UserPerferenceDict[str_current_user])
            return redirect('/page-setting.html')

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )
        if template == "page-setting.html":
            servicesInUse = UserPerferenceDict.get(str_current_user)
            servicesCanAdd = []

            for service in running_services:
                if service not in servicesInUse:
                    servicesCanAdd.append(service)
            return render_template(template,segment=segment,selectedServiceAdd=servicesCanAdd,selectedServiceRed=servicesInUse,wholeList = running_services,content = servicesInUse,visibleservices = UserPerferenceDict.get(str_current_user))
        # Serve the file (if exists) from app/templates/FILE.html

        if template == "page-service1.html":
            if len(UserPerferenceDict.get(str_current_user)) >=1:
                title = UserPerferenceDict.get(str_current_user)[0][1]
                url = UserPerferenceDict.get(str_current_user)[0][2]
                print(title+url)
                return render_template("page-service1.html", segment=segment,visibleservices = UserPerferenceDict.get(str_current_user), service1title = title, service1url = url)
            else:
                return render_template('page-404.html'), 404
        elif template == "page-service2.html":
            if len(UserPerferenceDict.get(str_current_user)) >=2:
                title = UserPerferenceDict.get(str_current_user)[1][1]
                url = UserPerferenceDict.get(str_current_user)[1][2]
                print(title+url)
                return render_template("page-service2.html", segment=segment,visibleservices = UserPerferenceDict.get(str_current_user), service2title = title, service2url = url)
            else:
                return render_template('page-404.html'), 404
        elif template == "page-service3.html":
            if len(UserPerferenceDict.get(str_current_user)) >=3:
                title = UserPerferenceDict.get(str_current_user)[2][1]
                url = UserPerferenceDict.get(str_current_user)[2][2]
                print(title+url)
                return render_template("page-service3.html", segment=segment,visibleservices = UserPerferenceDict.get(str_current_user), service3title = title, service3url = url)
            else:
                return render_template('page-404.html'), 404
        elif template == "page-service4.html":
            if len(UserPerferenceDict.get(str_current_user)) >=4:
                title = UserPerferenceDict.get(str_current_user)[3][1]
                url = UserPerferenceDict.get(str_current_user)[3][2]
                print(title+url)
                return render_template("page-service4.html", segment=segment,visibleservices = UserPerferenceDict.get(str_current_user), service4title = title, service4url = url)
            else:
                return render_template('page-404.html'), 404
        elif template == "page-service5.html":
            if len(UserPerferenceDict.get(str_current_user)) >=5:
                title = UserPerferenceDict.get(str_current_user)[4][1]
                url = UserPerferenceDict.get(str_current_user)[4][2]
                print(title+url)
                return render_template("page-service5.html", segment=segment,visibleservices = UserPerferenceDict.get(str_current_user), service5title = title, service5url = url)
            else:
                return render_template('page-404.html'), 404
        return render_template(template, segment=segment,visibleservices = UserPerferenceDict.get(str_current_user))
    except TemplateNotFound:
        return render_template('page-404.html'), 404

    # except:
    #     return render_template('page-500.html'), 500

# Helper - Extract current page name from request
def get_segment( request ):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment
    except:
        return None
