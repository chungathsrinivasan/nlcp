# -*- coding: utf-8 -*-
"""
Created on Tue November 16 23:07:48 2021

@author: LAKSHMY
"""


def eigenvalue(seq):
    sublist1=[[]]
    sublist2=[[]]
    n=len(seq)
    for i in range(n): 
        for j in range(i,n): 
            sub = seq[i:j+1] 
            sublist1.append(sub) 
    #print(sublist1)
    for i in range(n-1): 
        for j in range(i,n-1): 
            sub = seq[i:j+1] 
            sublist2.append(sub) 
    #print(sublist2)
    out = [i for i in sublist1 if not i in sublist2]
    #print(out)
    #print(len(out))
    return(len(out))


def evprofile (seq):
    prof=[]
    for i in range(1,len(seq)):
        temp=seq[0:i]
        prof=prof+[eigenvalue(temp)]
    return(prof)  

def Reverse(lst): 
    return [ele for ele in reversed(lst)]


def dis(ct,h):
    count=0
    for i in range(len(h)):
        le=len(h[i])
        if ct[0:le]==h[i]:
            count=count+1
    count=count%2        
    return(count)        
        
            
def nlcp(y):
    mm=[]
    k=0
    m=0
    mm=mm+[m] 
    h=[]
    N=len(y)
    for n in range(1,N):
        #print('n',n)
        ct=Reverse(y[n-m:n])
        #print('ct',ct)
        if len(ct)==0:
            d=y[n]-y[0]
        else:
            d=y[n]-dis(ct,h)
        #print('d',d)
        if d!=0:
            if m==0:
                k=n
                m=n
            elif k<=0:
                yn=y[0:n]
                t=eigenvalue(yn)
                if t<n+1-m:
                    k=n+1-t-m
                    m=n+1-t
            else:
               k=k-1
            f=Reverse(y[n-m:n])
            
            #print('f',f)
            h=h+[f]
            #print ('h',h)
        else:
             k=k-1
        mm=mm+[m] 
        #print ('k',k)
        #print ('m',m)
        #print('.................................')
    return(mm,h) 



import numpy
import copy
def berlekamp_massey_algorithm(block_data):
    n = len(block_data)
    c = numpy.zeros(n)
    b = numpy.zeros(n)
    c[0], b[0] = 1, 1
    l, m, i = 0, -1, 0
    int_data = [int(el) for el in block_data]
    while i < n:
        v = int_data[(i - l):i]
        v = v[::-1]
        cc = c[1:l + 1]
        d = (int_data[i] + numpy.dot(v, cc)) % 2
        if d == 1:
            temp = copy.copy(c)
            p = numpy.zeros(n)
            for j in range(0, l):
                if b[j] == 1:
                    p[j + i - m] = 1
            c = (c + p) % 2
            if l <= 0.5 * i:
                l = i + 1 - l
                m = i
                b = temp
        i += 1
    return (l)
def lcprofile(seq):
    profile=[]
    for i in range(0,len(seq)):
        seq1=seq[0:i+1]
        profile.append(berlekamp_massey_algorithm(seq1))
    return(profile)    


def jumpseq(b):
    jmp=[]
    jmp.append(0)
    #print(b)
    for i in range(len(b)-1):
        diff=b[i+1]-b[i]
        if(diff==0):
            jmp.append(0)
        else:
            jmp.append(1)
    return(jmp)
def jumphight(b):
    ht=[]
    ht.append(0)
    for i in range(len(b)-1):
        h=b[i+1]-b[i]
        ht.append(h)
    return(ht)
inputpath="F:/nlcp/"   #change input path here
fp=open(inputpath+"Streamespresso.txt")  #change file name based on ciphers
str1=fp.read()
#print(type(str1))
nlcpall=[]
evall=[]
lcall=[]
jnlcpall=[]
jevall=[]
jlcall=[]
hall=[]
juhtnlc=[]
for i in range(10): #change here for number of samples to be tested
    key=str1[256*i:256*(i+1)]
    b=[int(a) for a in key]
    print(b)
    temp0=nlcp(b)
    temp1=temp0[0]
    jmptemp1=jumpseq(temp1)
    jhntemp=jumphight(temp1)
    htemp=temp0[1]
    temp2=evprofile(b)
    jmptemp2=jumpseq(temp2)
    temp3=lcprofile(b)
    jmptemp3=jumpseq(temp3)
    nlcpall.append(temp1)
    evall.append(temp2)
    lcall.append(temp3)
    jnlcpall.append(jmptemp1)
    jevall.append(jmptemp2)
    jlcall.append(jmptemp3)
    hall.append(htemp)
    juhtnlc.append(jhntemp)
    print(i)
    
import pandas as pd
df1 = pd.DataFrame(nlcpall)
df2 = pd.DataFrame(evall)
df3 = pd.DataFrame(lcall)
df4 = pd.DataFrame(jnlcpall)
df5 = pd.DataFrame(jevall)
df6 = pd.DataFrame(jlcall)
df7 = pd.DataFrame(hall)
df8 = pd.DataFrame(juhtnlc)
writer = pd.ExcelWriter(inputpath+'Streamespresso.xlsx', engine='xlsxwriter') # change outputfilename based on cipher
df1.to_excel(writer, sheet_name='Non-Linear Profile')
df4.to_excel(writer, sheet_name='Jump in Non-Linear Profile')
df2.to_excel(writer, sheet_name='Eigen value Profile')
df5.to_excel(writer, sheet_name='Jump in Eigen value Profile')
df3.to_excel(writer, sheet_name='Linear Profile')
df6.to_excel(writer, sheet_name='Jump in Linear Profile')
df7.to_excel(writer, sheet_name='feedback function')
df8.to_excel(writer, sheet_name='hight in jump of nlc')
writer.save()