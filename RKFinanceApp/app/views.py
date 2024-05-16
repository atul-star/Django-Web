from .models import Contact
from django.shortcuts import render, redirect
from .forms import ContactForm

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
        breakpoint()
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
