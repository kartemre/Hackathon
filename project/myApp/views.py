from django.shortcuts import render, redirect
from .models import User, WaterUsage, Award
from django.contrib.auth.hashers import make_password, check_password

def home(request):
    context = {
        'incentive_awards': Award.objects.filter(is_recent=True, category='incentive'),
        'general_awards': Award.objects.filter(is_recent=True, category='general'),
        'last_month_winners': Award.objects.filter(is_recent=False),
    }
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        tc = request.POST.get('tc')
        password = request.POST.get('password')
        
        user = User.objects.filter(tc=tc).first()
        if user and check_password(password, user.password):
            request.session['authenticated'] = True
            request.session['user_id'] = user.id
            return redirect('auth_home')
        else:
            return render(request, 'login.html', {'error': 'TC Kimlik numarası veya şifre yanlış.'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        tc = request.POST.get('tc')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        errors = []
        if not first_name.isalpha():
            errors.append("Ad kısmı sadece harf içerebilir.")
        if not last_name.isalpha():
            errors.append("Soyad kısmı sadece harf içerebilir.")
        if not tc.isdigit() or len(tc) != 11:
            errors.append("TC Kimlik numarası 11 haneli olmalı ve sadece rakam içermelidir.")
        if not phone.isdigit() or len(phone) != 11:
            errors.append("Telefon numarası 11 haneli olmalı ve sadece rakam içermelidir.")
        if not email or "@" not in email or "." not in email:
            errors.append("Geçerli bir email adresi giriniz.")

        if User.objects.filter(tc=tc).exists():
            errors.append("Bu TC Kimlik Numarası ile daha önce kayıt olunmuş.")
        if User.objects.filter(email=email).exists():
            errors.append("Bu email adresi ile daha önce kayıt olunmuş.")

        if errors:
            return render(request, 'register.html', {'errors': errors})

        user = User(
            first_name=first_name,
            last_name=last_name,
            tc=tc,
            email=email,
            password=make_password(password),
            phone=phone
        )
        user.save()

        return redirect('login')

    return render(request, 'register.html')

def auth_home(request):
    if not request.session.get('authenticated', False):
        return redirect('login')
    
    current_month = WaterUsage.objects.order_by('-billing_year', '-billing_month').first()
    if current_month:
        current_year = current_month.billing_year
        current_month = current_month.billing_month
        incentive_awards = Award.objects.filter(is_recent=True, category='incentive', month=current_month, year=current_year)
        general_awards = Award.objects.filter(is_recent=True, category='general', month=current_month, year=current_year)
    else:
        incentive_awards = []
        general_awards = []

    last_month_winners = Award.objects.filter(is_recent=False).order_by('-year', '-month')

    context = {
        'incentive_awards': Award.objects.filter(is_recent=True, category='incentive'),
        'general_awards': Award.objects.filter(is_recent=True, category='general'),
        'last_month_winners': Award.objects.filter(is_recent=False),
    }
    return render(request, 'auth_home.html', context)


def profile(request):
    if not request.session.get('authenticated', False):
        return redirect('login')
    
    user = User.objects.get(id=request.session['user_id'])
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        
        errors = []
        if not first_name.isalpha():
            errors.append("Ad kısmı sadece harf içerebilir.")
        if not last_name.isalpha():
            errors.append("Soyad kısmı sadece harf içerebilir.")
        if not phone.isdigit() or len(phone) != 11:
            errors.append("Telefon numarası 11 haneli olmalı ve sadece rakam içermelidir.")
        if not email or "@" not in email or "." not in email:
            errors.append("Geçerli bir email adresi giriniz.")

        if errors:
            return render(request, 'profile.html', {'errors': errors, 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone})

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        if password:
            user.password = make_password(password)
        user.save()

        return redirect('auth_home')

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
    }

    return render(request, 'profile.html', context)

def logout(request):
    request.session['authenticated'] = False
    return redirect('home')


def tesvik(request):
    if not request.session.get('authenticated', False):
        return redirect('login')

    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        user_id = request.session.get('user_id')
        fatura = WaterUsage.objects.filter(barcode=barcode).first()

        if fatura:
            if fatura.user_id == user_id:
                if fatura.water_used <= 25:
                    tesvik_miktari = fatura.amount_paid * 0.20
                    mesaj = f"Tebrikler! Teşvik almaya hak kazandınız. Kullanılan su miktarı: {fatura.water_used} m³. Ödemeniz gereken miktar: {fatura.amount_paid} TL. Teşvik miktarınız: {tesvik_miktari} TL."
                else:
                    mesaj = f"Kullanılan su miktarı: {fatura.water_used} m³. Teşvik almaya hak kazanamadınız. Teşvik almak için 25 m³ veya daha az su tüketmelisiniz."
            else:
                mesaj = "Girilen barkod numarasına ait fatura başka bir kullanıcıya ait."
        else:
            mesaj = "Girilen barkod numarasına ait fatura bulunamadı."

        return render(request, 'tesvik.html', {'mesaj': mesaj})

    return render(request, 'tesvik.html')

def forget(request):
    if request.method == 'POST':
        tc = request.POST.get('tc')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        new_password = request.POST.get('new_password')
        
        user = User.objects.filter(tc=tc, email=email, phone=phone).first()
        
        if user:
            user.password = make_password(new_password)
            user.save()
            mesaj = "Şifreniz başarıyla güncellenmiştir. Yeni şifrenizle giriş yapabilirsiniz."
        else:
            mesaj = "Girdiğiniz bilgiler doğru değil. Lütfen tekrar deneyin."
        
        return render(request, 'forget.html', {'mesaj': mesaj})

    return render(request, 'forget.html')