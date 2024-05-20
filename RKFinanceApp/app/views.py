from .models import Contact,Feedback
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.http.response import JsonResponse
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')
def contact(request):
    return render(request, 'contact.html')

def save_data(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        if mobile == "":
            mobile = None
        Contact.objects.create(name = name,email = email,mobile = mobile)
        c = Contact.objects.count()
        return render(request, 'home.html',{"msg":"Thank you your data data is saved"})



def contact_form_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            print("successs")
            return redirect('success_page')
        else:
            print("seeeeeler")
    else:
        print("elsee")
        form = ContactForm()
    return render(request, 'home.html')

def success_page(request):
    return render(request, 'home.html')


def feedback(request):
    return render(request , 'feedback.html')

def display_feedback(request):
    return render(request , 'display_feedback.html')

def save_feedback(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('uname')
        email = data.get('email')
        mobile = data.get('phone')
        satisfy = data.get('satisfy')
        msg = data.get('msg')
        is_satisfy = True
        if satisfy == 'no':
            is_satisfy = False
        Feedback.objects.create(name=name, email=email, mobile=mobile,is_satisfy = is_satisfy,
                                feedback = msg)
        return render(request, 'home.html', {"msg": "Thank you your data data is saved"})
    else:
        return render(request, 'feedback.html', {"msg": "Thank you your data data is saved"})


# def get_feedback(request):
#     if request.method=='GET':
#         data = []
#         objs = Feedback.objects.all()
#         for obj in objs:
#              data.append({"name":obj.name,"feedback":obj.feedback})
#         # return render(request,"display_feedback.html",{"data":data})
#         return JsonResponse({"data":data})





def get_feedback(request):
    if request.method == 'GET':
        data = []
        objs = Feedback.objects.all()
        for obj in objs:
            data.append({"name": obj.name, "feedback": obj.feedback})

        response = JsonResponse({"data":data})
        # response['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
        return response
