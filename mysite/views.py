
from django.http import HttpResponse
from django.shortcuts import render
import re

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


def analyze(request):
    removepanc=request.POST.get("removepanc","off")
    countword=request.POST.get("countword","off")
    countchar=request.POST.get("countchar","off")
    extraspace=request.POST.get('xtraspace','off')
    xreplace=request.POST.get('xreplace','off')
    formate=request.POST.get("formate","5")
    djtext=request.POST.get("text","default")
    newchar=request.POST.get('newchar','default')
    oldchar=request.POST.get('oldchar','default')
    st=djtext.strip()
    if st!='':
        if xreplace=='on' or removepanc=='on'or countword=='on'or extraspace=='on' or countchar=='on' or formate=='0' or formate=='1' or formate=='2':
            cchar=0
            word=0
            class mydics(dict):
                def __init__(self): 
                    self = dict()
                def add(self, key, value): 
                    self[key] = value
            param=mydics()
            analyzed=''
            if removepanc=='on':
                punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                for char in djtext:
                    if char not in punctuations:
                        analyzed+=char
            else:
                analyzed=djtext
            
            if extraspace=='on':
                extra=''
                for index,char in enumerate(analyzed):
                    if not(analyzed[index]==" " and analyzed[index+1]==" "):
                        extra=extra+char
                analyzed=extra
                        
            if xreplace=='on':
                analyzed=analyzed.replace(oldchar,newchar)

            if countchar=='on':
                for char in analyzed:
                    cchar+=1
                param.add('countchar',f'Total Character in Analyzed Paragraph: {cchar}')
            if countword=='on':
                word=len(re.findall(r'\w+',analyzed))
                param.add('countword',f'Total Word in Analyzed Paragraph: {word}')
            if formate=='0':
                analyzed=analyzed.upper()
            if formate=='1':
                analyzed=analyzed.lower()
            if formate=='2':
                analyzed=analyzed.title()
            param.add('analyzed_text',analyzed)
            if analyzed=='':
                param={'message':'Result: Your Analyzed text is Empty'}
                return render(request,'index.html',param)
            return render(request,'analyze.html',param)
        else:
            param={'message':'Error: Please check atleast on option from given below'}
            return render(request,'index.html',param)
    else:
        param={'message':'Error: Enter valid paragraph'}
        return render(request,'index.html',param)

        