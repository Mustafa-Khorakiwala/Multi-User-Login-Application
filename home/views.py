from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from home.models import Student,Teacher,Person
from django.contrib import messages
import smtplib
import random

r = 0
student = None
teacher = None
person = None
temp = None
temp1 = None
# Create your views here.
def student_register(request):
    global student
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        rollno = request.POST.get('rollno')
        password = hash(request.POST.get('password'))
        s = Student.objects.filter(rollno=rollno)
        s1 = Student.objects.filter(email=email)
        t1 = Teacher.objects.filter(email=email)
        p1 = Person.objects.filter(email=email)
        if s.count()>0:
            messages.add_message(request, 50,"This roll no is already registered")
        elif s1.count()>0 or t1.count()>0 or p1.count()>0:
            messages.add_message(request, 50, "Email is already registered")
        else:
            sendingMail(email)
            student = Student(name=name, email=email, password=password,rollno=rollno,date=datetime.today())
            return redirect('/verification')
    return render(request, 'student_register.html')

def teacher_register(request):
    if request.method=="POST":
        global teacher
        name = request.POST.get('name')
        email = request.POST.get('email')
        staffcode = request.POST.get('staffcode')
        password = hash(request.POST.get('password'))
        t = Teacher.objects.filter(staffcode=staffcode)
        s1 = Student.objects.filter(email=email)
        t1 = Teacher.objects.filter(email=email)
        p1 = Person.objects.filter(email=email)
        if t.count()>0:
            messages.add_message(request, 50,"This staff code is already registered")
        elif s1.count()>0 or t1.count()>0 or p1.count()>0:
            messages.add_message(request, 50, "Email is already registered")
        else:
            sendingMail(email)
            teacher = Teacher(name=name, email=email, password=password,staffcode=staffcode,date=datetime.today())
            return render(request, 'verification.html')
    return render(request, 'teacher_register.html')

def person_register(request):
    if request.method=="POST":
        global person
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phoneno')
        password = hash(request.POST.get('password'))
        p = Person.objects.filter(phone=phone)
        s1 = Student.objects.filter(email=email)
        t1 = Teacher.objects.filter(email=email)
        p1 = Person.objects.filter(email=email)
        if p.count()>0:
            messages.add_message(request, 50,"This phone no is already registered")
        elif s1.count()>0 or t1.count()>0 or p1.count()>0:
            messages.add_message(request, 50, "Email is already registered")
        else:
            sendingMail(email)
            person = Person(name=name, email=email, password=password,phone=phone,date=datetime.today())
            return render(request, 'verification.html')
    return render(request, 'person_register.html')

def login(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = hash(request.POST.get('password'))
        s1 = Student.objects.filter(email=email)
        t1 = Teacher.objects.filter(email=email)
        p1 = Person.objects.filter(email=email)
        if s1.count()>0:
            a = s1[0].password
            if a==password:
                return render(request, 'student_page.html')
            else:
                messages.add_message(request, 50, "Password is wrong")
        elif t1.count()>0:
            a = t1[0].password
            if a==password:
                return render(request, 'teacher_page.html')
            else:
                messages.add_message(request, 50, "Password is wrong")
        elif p1.count()>0:
            a = p1[0].password
            if a==password:
                return render(request, 'person_page.html')
            else:
                messages.add_message(request, 50, "Password is wrong")
        else:
            messages.add_message(request, 50, "Email has not been registered")
        
    
    return render(request, 'mainn.html')

def verification(request):
    if request.method=="POST":
        verify = request.POST.get('verify')
        if r==int(verify):
            global student, teacher, person
            if student is not None:
                student.save()
                student = None
                return render(request, 'student_page.html')
            if teacher is not None:
                teacher.save()
                teacher = None
                return render(request, 'teacher_page.html')
            if person is not None:
                person.save()
                person = None
                return render(request, 'person_page.html')
        else:
            messages.add_message(request, 50, "Verification Code is Wrong")
            return render(request, 'verification.html')
    return render(request, 'verification.html')


def sendingMail(email):
    global r
    r = random.randint(100000,999999)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("practicetest57@gmail.com",'Test@1234')
    subject = "Verification code"
    body = "Your 6 digit verification code is {}".format(r)
    message = "Subject:{}\n\n{}".format(subject, body)
    server.sendmail("practicetest57@gmail.com",email,message)
    server.quit()
    return

def register(request):
    if request.method=="POST":
        action = request.POST.get('action')
        action1 = request.POST.get('action1')
        action2 = request.POST.get('action2')
        if action=='_teacher':
            return render(request, 'teacher_register.html')
        elif action1=='_student':
            return render(request, 'student_register.html')
        elif action2=='_person':
            return render(request, 'person_register.html')
    return render(request, 'register.html')

def password_validation(request):
    global temp,temp1
    if request.method=="POST":
        email = request.POST.get('email')
        s1 = Student.objects.filter(email=email)
        t1 = Teacher.objects.filter(email=email)
        p1 = Person.objects.filter(email=email)
        if s1.count()>0:
            temp=s1
            temp1="student"
            sendingMail(email)
            return render(request, 'password_verify.html')
        elif t1.count()>0:
            temp=t1
            temp1="teacher"
            sendingMail(email)
            return render(request, 'password_verify.html')
        elif p1.count()>0:
            temp=p1
            temp1="person"
            sendingMail(email)
            return render(request, 'password_verify.html')
        else:
            messages.add_message(request, 50, "Email is not registered")

    return render(request, 'password_validation.html')

def password_verify(request):
    if request.method=="POST":
        verify = request.POST.get('verify')
        if r==int(verify):
            return render(request, 'forgot_password.html')
        else:
            messages.add_message(request, 50, "Verification Code is Wrong")
            return render(request, 'password_verify.html')
    return render(request, 'password_verify.html')

def forgot_password(request):
    if request.method=="POST":
        global temp, temp1
        passnew = request.POST.get('passnew')
        passre = request.POST.get('passre')
        if passnew!=passre:
            messages.add_message(request, 50, "Password mismatch")
            return render(request, 'forgot_password.html')
        else:
            var = hash(passnew)
            if temp1=='student':
                s = Student(name=temp[0].name,email=temp[0].email,rollno=temp[0].rollno,password=var,date=datetime.today())
                temp.delete()
                s.save()
                temp=None
                temp1=None
            elif temp1=='teacher':
                t = Teacher(name=temp[0].name,email=temp[0].email,staffcode=temp[0].staffcode,password=var,date=datetime.today())
                temp.delete()
                t.save()
                temp=None
                temp1=None
            elif temp1=='person':
                p = Person(name=temp[0].name,email=temp[0].email,phone=temp[0].phone,password=var,date=datetime.today())
                temp.delete()
                p.save()
                temp=None
                temp1=None
            return render(request, 'mainn.html')
    return render(request, 'forgot_password.html')