from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question, table,seller,verif,farmer,corporate,cart
from django.template import loader
from django.core.mail import send_mail,BadHeaderError
import smtplib
import string
from polls.forms import sellerform


### admin page   username=varun  pass=9494868523

# Create your views here.

# as you add any function here update in urls to connect it
# this urls map to needed page by address 


#Each view is responsible for doing one of two things:
#  returning an HttpResponse object containing the content for the requested page, 
# or raising an exception such as Http404. 
def index(request):
    return HttpResponse("hello world .you are at polls index .so in myproject .url server checks the maching in url patterns with --127.0.0.1:800/xxxx/ that xxx/ with any of the path in the urls pattern in path there are 4 argmnets we need only 2 or 3  one is route :like polls/ or xxx/ server checked with this ,next is view :when it find the match it creates an http request object and calls the view function and it returns a httpresponse and it may give some name for our purpose")

def results(request,question_id):
    text="you r looking at result of %s"
    return HttpResponse(text%question_id)

#to add these new functionalities we alo need to add at urls.py in polls

# this is connecting views to database see this carefully
#to use db tables import from .models and type table name

def index1(request):
    latest_q=Question.objects.order_by('-pub_date')[:5]
    output=', '.join([q.question_text for q in latest_q])
    return HttpResponse(output)

#: the page’s design is hard-coded in the view. 
# If you want to change the way the page looks,
#  you’ll have to edit this Python code. So let’s use Django’s 
# template system to separate the design from Python by creating a
#  template that the view can use.   
#so create a templatess directory in polls directory.

#Your project’s TEMPLATES setting describes 
# how Django will load and render templates

#. In other words, your template should be at polls/templates/polls/index.html.
#  Because of how the app_directories template loader works as described above,
#  you can refer to this template within Django as polls/index.html.

# because the html is fixed by using this king of above views we are are 
# using templates in this way this needs loader and 

def index2(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

#  The context is a dictionary mapping template variable names to Python objects.
  
# if we need not to loader to import then we can use this   
def index3(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request,'polls/index1.html',context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def signupfarm(request):
    if request.GET:
        na=request.GET
        if "cancel" in na:
            return render(request,'polls/signupfarm.html')
        name=na['who']
        pswrd=na['pass']
        phn=na['phn']
        ema=na['email']
        ident=na['ident']
        if len(name)==0 or len(pswrd)==0 or len(ident)==0 or len(phn)!=10:
            return render(request,'polls/signupfarm.html',{'mssg':"enter the details"})

        try:
            obj=verif.objects.get(user_name=name)
        except:
            return render(request,'polls/signupfarm.html',{'mssg':"invalid farmer id"})

        if obj.user_id==ident:
            t=farmer(user_name=name,password=pswrd,email=ema,phn=phn)
            t.save()
            return HttpResponseRedirect('/polls/loginfarm/')
                #render(request,'polls/succsesful.html')
        else:
            return render(request,'polls/signupfarm.html',{'mssg':"invalid farmer id"})
    else:    
        return render(request,'polls/signupfarm.html')

    


def signup(request):
    # if no data is sent is showing error see that
    #print(name)
    #print(request.POST)
    if request.GET:
        na=request.GET
        if "cancel" in na:
            return render(request,'polls/signup.html')
        name=na['who']
        pswrd=na['pass']
        phn=na['phn']
        ema=na['email']
            #print("entered buyyer email==",ema)
        if len(name)==0 or len(pswrd)==0 or len(ema)==0 or len(phn)!=10:
            #print("in if  ")
            return render(request,'polls/signup.html',{'mssg':"enter the details"})
            #print("out of if")
        t=table(user_name=name,password=pswrd,email=ema,phn=phn)
        t.save()
        return HttpResponseRedirect('/polls/login/')
        #render(request,'polls/succsesful.html')
    else:    
        return render(request,'polls/signup.html')
    
nm="none"
def loginfarm(request):
    if request.GET:
        na=request.GET
        if "cancel" in na:
            return render(request,'polls/loginfarm.html')
        
        name=na['who']
        pswrd=na['pass']
        global nm
        print(nm)
        nm=name
        #nm=name
        print(nm)
        try:
            obj=farmer.objects.get(user_name=name)
        except:
            return render(request,'polls/loginfarm.html',{'mssg':"invalid password or username"})
            
        if obj.password == pswrd:
            return render(request,'polls/buyAndSell.html',{'name':name})
        else:
            return render(request,'polls/loginfarm.html',{'mssg':"invalid password or username"})
    else:
        return render(request,'polls/loginfarm.html')


def login(request):
    if request.GET:
        na=request.GET
        if "cancel" in na:
            return render(request,'polls/login.html')
        
        name=na['who']
        pswrd=na['pass']
        try:
            obj=table.objects.get(user_name=name)
        except:
            return render(request,'polls/login.html',{'mssg':"invalid password or username"})
            
        if obj.password == pswrd:
            return render(request,'polls/buyerbuy.html')
        else:
            return render(request,'polls/login.html',{'mssg':"invalid password or username"})
    else:
        return render(request,'polls/login.html')

def buyAndSell(request):
    #print("hello")
    return render(request,'polls/buyAndSell.html')

#def inAction(request):
#    if request.method=='GET':
        
# we can pass object 
# like if the obj=table() return render(request,'polls/buy..',{'user':obj})
# we can send multiple users like users=[user1,user2,...] by replacing {'user': users}

#def send_email(request):
    #subject = request.POST.get('subject', '')
    #message = request.POST.get('message', '')
    #from_email = request.POST.get('from_email', '')
#    subject='hello this mail system is working'
#    message='sent fromm django'
#    from_email='varunakrishna1@gmail.com' 
#    if subject and message and from_email:
#        try:
#            send_mail(subject, message, from_email, ['vikram.g19@iiits.in'],fail_silently=False)
#        except BadHeaderError:
#            return HttpResponse('Invalid header found.')
#        return HttpResponseRedirect('/contact/thanks/')
#    else:
#        # In reality we'd use a form class
#        # to get proper validation errors.
#        return HttpResponse('Make sure all fields are entered and valid.')

#we can alos use  send_mass_mail()  to send mass mails in the aboove also can sen we need to add recepient at reciepent(to) [] list 

def send_email(request):
    username = "varunakrishna1@gmail.com"
    password = "9494868523"
    smtp_server = "smtp.gmail.com:587"
    email_from = "varunakrishna1@gmail.com"
    email_to = "vikram.g19@iiits.in"
    email_body =" mail sent from django checking"
    
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password,initial_response_ok=True)
    server.sendmail(email_from, email_to, email_body)
    server.quit()
    return render(request,'polls/succsesful.html')

def buy(request):
    if request.GET:
        na=request.GET
        food=na['crop']
        obj=seller.objects.filter(crop_name=food)
        o=[]
        for i in obj:
            a=seller.objects.get(user_name=i)
            o.append(a)
        obj=seller.objects.order_by().values('crop_name').distinct()
        return render(request,'polls/buyer.html',{'obj':o,'item':obj})
    else:
        obj=seller.objects.order_by().values('crop_name').distinct()
        return render(request,'polls/buyer.html',{'item':obj})

it="none"
def buyfarm(request):
    if request.GET:
        na=request.GET
        obj=corporate.objects.order_by().values('good_name').distinct()
        #it="crop"
        if 'crop' in na:
            food=na['crop']
            print(food) 
            global it
            it=food
            print(it)
            obj=corporate.objects.filter(good_name=food)
            o=[]
            for i in obj:
                a=corporate.objects.get(company=i)
                o.append(a)
            obj=corporate.objects.order_by().values('good_name').distinct()
            return render(request,'polls/buyfarm.html',{'obj':o,'item':obj,'crop_nm':food})
        else:
            if 'seller' not in na  or 'city' not in na or 'phn' not in na:
                return render(request,'polls/buyfarm.html',{'item':obj,'mssg':"enter the details"})   
            sell=na['seller']
            name=na['who']
            city=na['city']
            phn=na['phn']
            email=na['email']
            #global it
            print(it)
            #print(na['cr'])
            #it=na['cr']
            #it="item"
            if len(sell)==0 or len(city)==0 or len(phn)!=10:
                return render(request,'polls/buyfarm.html',{'item':obj,'mssg':"enter the details"})
            if 'cart' in na:
               
                c=cart(name=name,item=it,seller_name=sell)
                c.save()
                return render(request,'polls/buyfarm.html',{'item':obj,'mssg':"added to cart"})
            return render(request,'polls/buyfarm.html',{'item':obj,'mssg':"succesful delivery will be there at your home"})
    else:
        obj=corporate.objects.order_by().values('good_name').distinct()
        #print(obj)
        return render(request,'polls/buyfarm.html',{'item':obj})

def sell(request):
    if request.GET:
        na=request.GET
        if "cancel" in na:
            return render(request,'polls/seller.html')
        name=na['nam']
        ident=na['ident']
        crop=na['crop']
        price=na['price']
        max_kg=na['max']
        img=na['img']
        if len(name)==0 or len(ident)==0 or max_kg==0 or len(crop)==0 or len(price)==0 or len(img)==0:
            return render(request,'polls/seller.html',{'mssg':"enter the details"})
        try:
            obj=verif.objects.get(user_name=name)
        except:
            return render(request,'polls/seller.html',{'mssg':"invalid farmer id"})

        if obj.user_id==ident:
            s=seller(user_name=name,crop_name=crop,price_per_kg=price,photo=img,max_kg=max_kg)
            s.save()
            return render(request,'polls/succsesful.html')
        else:
            return render(request,'polls/seller.html',{'mssg':"invalid farmer id"})        
    else:   
        return render(request,'polls/seller.html')



# please add cancel functionality   
def forgtpswrdfarm(request):
    if request.GET:
        na=request.GET
        if "cancel" in na:
            return render(request,'polls/forgtpswrdfarm.html')
        name=na['who']
        pswrd=na['pass']
        phn=na['phn']
        repass=na['repass']
        if len(name)==0 or len(pswrd)==0 or len(phn)==0 or len(repass)==0 :
            return render(request,'polls/forgtpswrdfarm.html',{'mssg':"enter the details"})
        try:
            obj=farmer.objects.get(user_name=name)
        except:
            return render(request,'polls/forgtpswrdfarm.html',{'mssg':"invalid user name"})

        if obj.phn==phn:
            if pswrd==repass:
                obj.password=pswrd
                obj.save()
                return HttpResponseRedirect('/polls/loginfarm/')
                # render(request,'polls/loginfarm.html',{'mssg':"password changed succesfully"})
            else:
                 return render(request,'polls/forgtpswrdfarm.html',{'mssg':"re enter password should be same as new password"})

        else:
            return render(request,'polls/forgtpswrdfarm.html',{'mssg':"phone number not matched"})
    else:
        return render(request,'polls/forgtpswrdfarm.html')


def forgtpswrd(request):
    if request.GET:
        na=request.GET
        if "cancel" in na:
            return render(request,'polls/forgtpswrd.html')
        name=na['who']
        pswrd=na['pass']
        phn=na['phn']
        repass=na['repass']
        if len(name)==0 or len(pswrd)==0 or len(phn)==0 or len(repass)==0 :
            return render(request,'polls/forgtpswrd.html',{'mssg':"enter the details"})
        try:
            obj=table.objects.get(user_name=name)
        except:
            return render(request,'polls/forgtpswrd.html',{'mssg':"invalid user name"})

        if obj.phn==phn:
            if pswrd==repass:
                obj.password=pswrd
                obj.save()
                return HttpResponseRedirect('/polls/login/')
                # render(request,'polls/login.html',{'mssg':"password changed succesfully"})
            else:
                 return render(request,'polls/forgtpswrd.html',{'mssg':"re enter password should be same as new password"})

        else:
            return render(request,'polls/forgtpswrd.html',{'mssg':"phone number not matched"})
    else:
        return render(request,'polls/forgtpswrd.html')


## after farmer register add a verification page
## in verification page check with data base verif table



### right now i am at sign up page and nned to change signup page db connections something like that
## and need to do forgot passwrd page
def gallery(request):
    obj = seller.objects.get(user_name="Harapriya Pal") 
    #obj = seller.objects.get(user_name="Hari Samal") 
    #obj = seller.objects.get(user_name="Jina Malik")
    #obj = seller.objects.get(user_name="Gourahari Pati")
    print(obj.photo.url)
    return render(request,'polls/gallery.html',{"img":obj})
    #{"img":obj.photo}
###see the picture how to store and how to retrieve

#def showimage(request):
#    lastimage= seller.objects.last()
#    photo= lastimage.photo
#    form= ImageForm(request.POST or None, request.FILES or None)
#    if form.is_valid():
#        form.save()
#    context={'photo': photo,
#              'form': form
#            }
#    return render(request, 'polls/gallery.html', context)

def home(request):
    return render(request,'polls/home.html')



def checkcart(request):
    print(nm)
    #global nm
    #nm="varuna krishna"
    obj=cart.objects.filter(name=nm)
    o=[]
    print(obj,o)       

    for i in obj:
        a=cart.objects.get(name=i)
        o.append(a)
    #obj=cart.objects.order_by().values('item').distinct()
    print(obj,o)       
    for i in o:
        print(i.item)
    return render(request,'polls/choutcart.html',{'name':nm,'obj':o})

#def hm(request):
#    if request.GET:
#        na=request.GET
#        name=na['who']
#        roll=na['roll']
#        br=na['branch']
#        cl=na['clg']
#        s1=na['s1']
#        s2=na['s2']
#        s3=na['s3']
#        s4=na['s4']
#        s5=na['s5']
#        t=int(s1)+int(s2)+int(s3)+int(s4)+int(s5)
#        p=t/5
#        return render(request,'polls/RESult.html',{"n":name,"r":roll,"br":br,"cl":cl,"s1":s1,"s2":s2,"s3":s3,"s4":s4,"s5":s5,"t":t,"p":p})
#    else:
#        return render(request,'polls/HOME1.html')    