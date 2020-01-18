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
    else:
        return render(request,'vregister.html')

def nregister(request):
    return render(request,'nregister.html')

def vregister(request):
    fname1 = request.POST.get('fname')
    lname1 = request.POST.get('lname')
    email1 = request.POST.get('email')
    gen1 = request.POST.get('gen')
    height1 = request.POST.get('height')
    weight1 = request.POST.get('weight')
    address1 = request.POST.get('address')
    allergy1 = request.POST.get('allergy')
    no = request.POST.get('no')
    global count
    qid= count
    count+=1
    
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
    
    en =  patient(fname=fname1,lname=lname1,Email=email1,height=height1,weight=weight1,gender=gen1,address=address1,allergy=allergy1,qid=qid,no=no)
    en.save()

    return render(request,'vregister.html')

# def dlogin(request):
#     return render(request,'login.html')
    