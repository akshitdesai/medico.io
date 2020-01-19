from django.shortcuts import render
from patient.models import doctor
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import qrcode
from patient.models import patient
import json

import numpy as np
import pandas
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle

from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

count = 1001
# Create your views here.
def index(request):
    return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def dlogin(request):
    request.session['logged']=False
    email1 = request.POST.get('email')
    pass1 = request.POST.get('pass')
    go = doctor.objects.get(email=email1)
    if go is None:
        return render(request,'dregister.html')
    else:
        if pass1 == go.pass1:
            request.session['logged']=True
            return render(request,'home.html')
        else:
            return render(request,'home.html')
    return render(request,'home.html')

def dregir(request):
    return render(request,'dregister.html')

def dregister(request):
    fname1 = request.POST.get('fname')
    lname1 = request.POST.get('lname')
    degree1 = request.POST.get('degree')
    exper1 = request.POST.get('exper')
    hosname1 = request.POST.get('hosname')
    no1 = request.POST.get('no')
    email1 = request.POST.get('email')
    pass1 = request.POST.get('pass1')
    pass2 = request.POST.get('pass2')
    if pass1 == pass2:
        dd = doctor(no=no1,degree=degree1,exper=exper1,fname=fname1,hospname=hosname1,lname=lname1,email=email1,pass1=pass1)
        dd.save()
        return render(request,'login.html')
    else:
        return render(request,'dregister.html')
        

def pregister(request):
    if request.POST.get('patient')=='new patient':
        return render(request,'nregister.html')
    elif request.POST.get('patient')=='view patient':
        return render(request,'vregister.html')
    else:
        return render(request,'dispatient.html')



def nregister(request):
    return render(request,'nregister.html')

def vregister(request):
    fname1 = request.POST.get('fname')
    request.session['fname1']=fname1
    lname1 = request.POST.get('lname')
    email1 = request.POST.get('email')
    gen1 = request.POST.get('gen')
    height1 = request.POST.get('height')
    weight1 = request.POST.get('weight')
    address1 = request.POST.get('address')
    allergy1 = request.POST.get('allergy')
    no = request.POST.get('no')
    bgroup1 = request.POST.get('bgroup')
    global count
    qid= count
    count+=1
    request.session['qid']=qid
    fromaddr = "codestromer@gmail.com"
    pwd = "Harikrushna123"

    toaddr = "akshitdesai2000@gmail.com" #str("akshitdesai2000@gmail.com")
    reciver = "Akshit Desai" #str("Akshit Desai")
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(qid))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(str(qid)+'.jpg')
    img_name = str(qid)+'.jpg'

    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address 
    msg['From'] = fromaddr 

    # storing the receivers email address 
    msg['To'] = toaddr 

    # storing the subject 
    msg['Subject'] = "Registered"

    # string to store the body of the mail 
    body = "Hey "+reciver+",\n You have registered on Medico.io"

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # open the file to be sent 
    filename = img_name
    attachment = open(img_name, "rb") 

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 

    # encode into base64 
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

    # creates SMTP session 
    #s = smtplib.SMTP('smtp.gmail.com', 587)
    s= smtplib.SMTP('smtp.gmail.com:587')

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(fromaddr,pwd) 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 

    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    print(reciver+"  Done")
    # terminating the session 
    s.quit()
    gen1='M'
    en =  patient(fname=fname1,lname=lname1,Email=email1,height=height1,weight=weight1,gender=gen1,address=address1,allergy=allergy1,qid=qid,no=no)
    en.save()
    data = {}
    data[str(qid)] = []
    data[str(qid)].append({
        'description':'',
        'prescription':'',
        'hospname':'',
        'doctname':''
    })
    with open('data.json','w') as outfile:
        json.dump(data,outfile)
    git = {'fname1':fname1,'lname1':lname1,'email1':email1,'gen1':gen1,'height1':height1,'weight1':weight1,'address1':address1,'allergy1':allergy1,'no':no,'bgroup1':bgroup1}
    return render(request,'vregister.html',git)

def vdec(request):
    fname1 = request.session['fname1']
    qid = request.session['qid']
    with open('data.json') as json_file:
        data = json.load(json_file)
        qid = ''+str(qid)
        data1 = data[str(qid)]

    git = {'fname1':fname1,'data1':data1}

    return render(request,'show.html',git)
def data(request):
    return render(request,'inputfile.html')

def visit(request):
    qid = request.session['qid']

    desc = request.POST.get('description')
    presc = request.POST.get('Prescription')
    doct = request.POST.get('doctname')
    hos = request.POST.get('hospname')

    data = json.load(open('data.json'))


# append new item to data lit
    data[str(qid)].append({
        "description": desc,
        "prescription": presc,
        "doctname": doct,
        "hospname": hos
    })

    # write list to file
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    fname1 = request.session['fname1']
    with open('data.json') as json_file:
        data = json.load(json_file)
        qid = ''+str(qid)
        data1 = data[qid]

    git = {'fname1':fname1,'data1':data1}
    return render(request,'show.html',git)
# def dlogin(request):
#     return render(request,'login.html')
    
def predict(request):
    l1 = float(request.POST.get('l1'))
    l2 = float(request.POST.get('l2'))
    l3 = float(request.POST.get('l3'))
    l4 = float(request.POST.get('l4'))
    l5 = float(request.POST.get('l5'))
    l6 = float(request.POST.get('l6'))
    l7 = float(request.POST.get('l7'))
    l8 = float(request.POST.get('l8'))
    from .pre import predict_dia_sym
    temp=[l1,l2,l3,l4,l5,l6,l7,l8]
    tested = predict_dia_sym(temp)
    return render(request,'final.html',{'tested':tested[0][0]})