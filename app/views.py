from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Password
from django.contrib.auth.views import auth_login
import string, random, ast
# Create your views here.


def index (request) :
    return render(request,'index.html')


def register (request) :

    if request.method == 'POST' :
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']


        # generate hash key for user
        letters = [x for x in string.ascii_lowercase ] + [x for x in string.ascii_uppercase ] + [' '] + [x for x in string.printable]
        key = {}



        for i in range(0,len(letters)) :
            letter_code = ''
            for j in range(0,random.randrange(2,100)) : letter_code += f'{random.choice(string.ascii_letters)}'
            key[ letters[i] ] = letter_code

        key[' '] = '99'


        # generate login key


        # create user and enter him to the system
        u = CustomUser.objects.create(
            username = username,
            email = email,
            password = password,
            hash_key = key,
        )
        


        auth_login(request,user=u)
        
        u = CustomUser.objects.get(email=email)
        login_key = f'{list(key.values())[0]}@{u.id}@{list(key.values())[len(key.values()) // 2]}{list(key.values())[len(key.values()) - 2]}'
        u.login_key  = login_key
        u.save()

        
        # write login code
        with open (f'media/users/{u.username}_profile.txt','w') as code :
            code.write(login_key)
        
        code.close()

        return redirect('profile')



    return render(request,'register.html')


def login (request) :

    c = {}

    if request.method == 'POST' :
        code = request.FILES['code']
        
        dec = code.read().decode('utf-8').split('@')

        uuid = dec[1]
        dec.remove(uuid)

        dec = ''.join(map(str,dec))
        
        
        user = CustomUser.objects.filter(id=uuid)

        if user.exists() :

            user_login_key = str(user.first().login_key).split('@')

            user_login_key.remove(uuid)

            user_login_key = ''.join(map(str,user_login_key))

            if user_login_key == dec :
                
                auth_login(request,user=user.first())
                
                return redirect('profile')

            else :
                c['msg'] = 'ملف غير صحيح'
        else :
            c['msg'] = 'ملف غير صحيح'


    return render(request,'login.html',c)




@login_required
def profile(request) :
    

    user = request.user
    hash_key = user.hash_key
    hash_key = ast.literal_eval(hash_key)

    # encrypt password
    if request.method == "POST" :
        
        name = request.POST['name']
        pas = request.POST['password']
        
        encripted_password = ''

        for i in pas:
            encripted_password += hash_key[i] + ' '



        Password.objects.create(
            name = name
            ,user = user
            ,password = encripted_password
            )
        
    
    valid_data = []

    # decrypt password
    passwords = Password.objects.filter(user=request.user).order_by('-id')

    for enc_password in passwords : 

        encripted_word = enc_password.password
        n = enc_password.name
        decrypt_word = ''
        for i in encripted_word.split(' ') :
            for j in range(len(hash_key.values())) : 
                if i == list(hash_key.values())[j] :
                    decrypt_word += f'{list(hash_key.keys())[j]}'  
                    break


    
        valid_data.append({
            'name':n,
            'text':decrypt_word,
            'id':enc_password.id,
        })


    print('_'*20)

    code = f'media/users/{request.user.username}_profile.txt'
    return render(request,'profile.html',{'code':code,'passwords':valid_data})