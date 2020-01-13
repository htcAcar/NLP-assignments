import os
import re
import math
import random
import operator

all_files = os.listdir("data/")   # imagine you're one directory above test dir
#  print(all_files)

hamilton_files=["9.txt","47.txt","7.txt","8.txt","13.txt","15.txt","16.txt","17.txt","21.txt","22.txt","23.txt","24.txt","25.txt","26.txt","27.txt","28.txt","29.txt"]
madison_files=["10.txt","14.txt","37.txt","38.txt","39.txt","40.txt","41.txt","42.txt","43.txt","44.txt","45.txt","46.txt"]
test_files=["9.txt","11.txt","12.txt","47.txt","48.txt","58.txt"]
unknown=["49.txt","50.txt","51.txt","52.txt","53.txt","54.txt","55.txt","56.txt","57.txt","62.txt","63.txt"]

uni_hamilton={}
uni_madison={}
bi_hamilton={}
bi_madison={}
tri_hamilton={}
tri_madison={}

uni_hamilton_l=[]
uni_madison_l=[]
bi_hamilton_l=[]
bi_madison_l=[]
tri_hamilton_l=[]
tri_madison_l=[]


uni_hamilton_fre={}
bi_hamilton_fre={}
tri_hamilton_fre={}
uni_madison_fre={}
bi_madison_fre={}
tri_madison_fre={}


cum_bi_hamilton={}
cum_tri_hamilton={}
cum_uni_madison={}
cum_bi_madison={}
cum_tri_madison={}

uni_ham_forBi={}
uni_mad_forBi={}

hamilton_list=[]
madison_list=[]

def addToDict(word,dict):
    if word not in dict:
        dict[word] = 1
    else:
        dict[word] += 1

def printDict(dict):
    for key in dict.keys():
        print(key, "->", dict[key], "   ")

def find_frequency(dict,fre_dict):
     sum=0
     for key in dict.keys():
         sum+=dict[key]
     for key in dict.keys():
         fre_dict[key]=(dict[key])/(sum)
     return fre_dict

def find_probablty(uni_dict_fre):
    sum=0
    for key in uni_dict_fre:
       sum+=math.log(uni_dict_fre[key])
    return sum

def addTriAndBi(list,biDict,TriDict):
    for h in range(0, len(list) - 1):
        str1 = list[h] + " " + list[h + 1]
        if h==0:
            str2="<s> "+list[h] + " " + list[h + 1]
        else:
            str2 = list[h-1] + " " + list[h ] + " " + list[h + 1]
        #print(str1)
        #print(str2)
        addToDict(str1, biDict)
        addToDict(str2, TriDict)


def uni_file(uni_dict_fre,uni_list):
    cum_uni_dict = {}
    sum = 0
    sorted_d = sorted(uni_dict_fre.items(), key=operator.itemgetter(1))
    # print(sorted_d)
    for key in sorted_d:
        sum += key[1]
        cum_uni_dict[key[0]] = sum
    sorted_d = sorted(cum_uni_dict.items(), key=operator.itemgetter(1))
    # print(sorted_d)

    for k in range(0, 30):
        random_num = random.uniform(0, 1)
        for i in range(0, len(sorted_d)):
            if i == 0 and random_num <= sorted_d[0][1]:
                word=sorted_d[0][0]
                uni_list.append(word)
                print(word," ",end=" ")
                break
            else:
                if random_num <= sorted_d[i][1] and random_num > sorted_d[i - 1][1]:
                    word = sorted_d[i][0]
                    uni_list.append(word)
                    print(word," ",end=" ")
                    break
                elif random_num > sorted_d[i][1] and random_num <= sorted_d[i + 1][1]:
                    word = sorted_d[i+1][0]
                    uni_list.append(word)
                    print(word," ",end=" ")
                    break

        if (sorted_d[0][0] == ".") or (sorted_d[i][0] == ".") or (sorted_d[i + 1][0] == "."):
            break
        # print(random_num)

def bi_file(start,bi_dict_fre,word_number,bi_list):
    sub_dict={}
    for key in bi_dict_fre.keys():
        f=key.split(" ")[0]
        s=key.split(" ")[1]
        if f==start:
            sub_dict[key]=bi_dict_fre[key]
    sorted_d= sorted(sub_dict.items(), key=operator.itemgetter(1))
    # print(sorted_d)
    sum=0
    for key in sorted_d:
        sum += key[1]
        sub_dict[key[0]] = sum
    sorted_d = sorted(sub_dict.items(), key=operator.itemgetter(1))
    # print(sorted_d)

    random_num = random.uniform(0, 1)
    # print("random:",random_num)

    for i in range(0, len(sorted_d)):
         if (sorted_d[0][0].split(" ")[1] == "</s>") or (sorted_d[i][0].split(" ")[1] == "</s>") or sorted_d==[] or (word_number==31):
            # print(".")
            break
         elif i == 0 and random_num <= sorted_d[0][1]:
            word=sorted_d[0][0].split(" ")[1]
            bi_list.append(word)
            print(word," ",end =" ")
            word_number+=1
            bi_file(sorted_d[0][0].split(" ")[1], bi_dict_fre,word_number,bi_list)
            break
         elif random_num <= sorted_d[i][1] and random_num > sorted_d[i - 1][1]:
            word = sorted_d[i][0].split(" ")[1]
            bi_list.append(word)
            print(word," ", end=" ")
            word_number+=1
            bi_file(sorted_d[i][0].split(" ")[1], bi_dict_fre,word_number,bi_list)
            break

def tri_file(start,tri_dict_fre,word_number,tri_list):
    sub_dict={}
    for key in tri_dict_fre.keys():
        f=key.split(" ")[0]+" "+key.split(" ")[1]
        s=key.split(" ")[2]
        if f==start:
            sub_dict[key]=tri_dict_fre[key]
    sorted_d= sorted(sub_dict.items(), key=operator.itemgetter(1))
    sum=0
    for key in sorted_d:
        sum += key[1]
        sub_dict[key[0]] = sum
    sorted_d = sorted(sub_dict.items(), key=operator.itemgetter(1))

    random_num = random.uniform(0, 1)

    for i in range(0, len(sorted_d)):
         if (sorted_d[0][0].split(" ")[2] == "</s>") or (sorted_d[i][0].split(" ")[2] == "</s>") or sorted_d==[] or (word_number==31):
            # print(".")
            break
         elif i == 0 and random_num <= sorted_d[0][1]:
            word=sorted_d[0][0].split(" ")[2]
            tri_list.append(word)
            print(word," ",end =" ")
            word_number+=1
            tri_file(sorted_d[0][0].split(" ")[1]+" "+sorted_d[0][0].split(" ")[2], tri_dict_fre,word_number,tri_list)
            break
         elif random_num <= sorted_d[i][1] and random_num > sorted_d[i - 1][1]:
            word = sorted_d[i][0].split(" ")[2]
            tri_list.append(word)
            print(word," ", end=" ")
            word_number+=1
            bi_file(sorted_d[i][0].split(" ")[1]+" "+sorted_d[i][0].split(" ")[2], tri_dict_fre,word_number,tri_list)
            break


sign=["#","+","$","^","%","&","{","}","[","]","*","?","!",":",",",";","-","_","."]

for file in all_files:
     # read_first_line("data/"+file)
     with open("data/"+file) as fp:
         line1=fp.readline()
         line2=fp.readline()
         #line2 = line2.rstrip('\r\n*,!?: ')
         line1=line1.rstrip('\r\n*,!?: ')
         #print("aouthor: " + line1 + "file:" + file)

         line2 = line2.lower()
         s = list(line2)
         if(s[len(line2)-1]=="."):
           s[len(line2)-1]=' '
         line2=''.join(s)
         line2="<s> "+line2+" </s>"#cümle bası ve sonu belirlendi


         for i in range(0, len(line2)):#cümle icindeki noktanın ve diğer işaretlerin tanımı yapıldı
             if line2[i] in sign:
                 if line2[i]==".":
                     line2 = line2.replace(line2[i], " </s> <s> ")
                 else:
                     line2=line2.replace(line2[i]," "+line2[i]+" ")

         content = line2.split()

         #SaYILAR TUTULUYOR
         if file in hamilton_files:
            for word in content:
                hamilton_list.append(word)
                addToDict(word, uni_ham_forBi)
                if word !="<s>" and word!="</s>":
                    addToDict(word,uni_hamilton)
            addTriAndBi(hamilton_list,bi_hamilton,tri_hamilton)
            hamilton_list.clear()

         if file in madison_files:
             for word in content:
                 madison_list.append(word)
                 addToDict(word,uni_mad_forBi)
                 if word != "<s>" and word != "</s>":
                    addToDict(word, uni_madison)
             addTriAndBi(madison_list, bi_madison, tri_madison)
             madison_list.clear()



#FOR TASK1
#Find unigram dictionary frequency
uni_hamilton_fre=find_frequency(uni_hamilton,uni_hamilton_fre)
uni_madison_fre=find_frequency(uni_madison,uni_madison_fre)

#Find Bigram Dictionary Frequency
for key in bi_hamilton.keys():
    t=key.split(" ")[0]
    bi_hamilton_fre[key]=(bi_hamilton[key])/(uni_ham_forBi[t])
for key in bi_madison.keys():
    t=key.split(" ")[0]
    bi_madison_fre[key]=(bi_madison[key])/(uni_mad_forBi[t])


#Find Trigram Dictionary Frequency
subtri_dict={}
for k in tri_hamilton.keys():
    w=k.split(" ")[0]+" "+k.split(" ")[1]
    addToDict(w,subtri_dict)
for key in tri_hamilton.keys():
    t = key.split(" ")[0] + " " + key.split(" ")[1]
    tri_hamilton_fre[key] = (tri_hamilton[key]) / (subtri_dict[t])
msubtri_dict={}
for k in tri_madison.keys():
    w=k.split(" ")[0]+" "+k.split(" ")[1]
    addToDict(w,msubtri_dict)
for key in tri_madison.keys():
    t = key.split(" ")[0] + " " + key.split(" ")[1]
    tri_madison_fre[key] = (tri_madison[key]) / (msubtri_dict[t])


#FOR TASK2
uni_file(uni_hamilton_fre,uni_hamilton_l)
print("\n------------------------------\n")
bi_file("<s>",bi_hamilton_fre,0,bi_hamilton_l)
# print("bi:",bi_hamilton_l)
print("\n------------------------------\n")
tri_file("<s> <s>",tri_hamilton_fre,0,tri_hamilton_l)
# print("tri:",tri_hamilton_l)
print("\n------------------------------\n")
uni_file(uni_madison_fre,uni_madison_l)
print("\n------------------------------\n")
bi_file("<s>",bi_madison_fre,0,bi_madison_l)
print("\n------------------------------\n")
tri_file("<s> <s>",tri_madison_fre,0,tri_madison_l)
print("\n------------------------------\n")


uni_hamilton_n={}
uni_madison_n={}
bi_hamilton_n={}
bi_madison_n={}
tri_hamilton_n={}
tri_madison_n={}

for w in uni_hamilton_l:
    addToDict(w,uni_hamilton_n)
uni_hamilton_fre=find_frequency(uni_hamilton_n,uni_hamilton_fre)
# printDict(uni_hamilton_fre)
print("for uni_hamilton file: ",find_probablty(uni_hamilton_fre))
for w in uni_madison_l:
    addToDict(w,uni_madison_n)
uni_madison_fre=find_frequency(uni_madison_n,uni_madison_fre)
print("for uni_madison file: ",find_probablty(uni_madison_fre))



addTriAndBi(bi_hamilton_l,bi_hamilton_n,tri_hamilton_n)
# printDict(bi_hamilton_n)
for key in bi_hamilton_n.keys():
    t=key.split(" ")[0]
    bi_hamilton_fre[key]=(bi_hamilton_n[key])/(uni_hamilton_fre[t])
# printDict(bi_hamilton_fre)
print("for bi_hamilton file: ",find_probablty(bi_hamilton_fre))


addTriAndBi(bi_madison_l,bi_madison_n,tri_madison_n)
for key in bi_madison_n.keys():
    t=key.split(" ")[0]
    bi_madison_fre[key]=(bi_madison[key])/(uni_madison_fre[t])
# printDict(bi_madison_fre)
print("for bi_madison file: ",find_probablty(bi_madison_fre))


addTriAndBi(tri_hamilton_l, bi_hamilton_n, tri_hamilton_n)
subtri_dict={}
for k in tri_hamilton_n.keys():
    w=k.split(" ")[0]+" "+k.split(" ")[1]
    addToDict(w,subtri_dict)
for key in tri_hamilton_n.keys():
    t = key.split(" ")[0] + " " + key.split(" ")[1]
    tri_hamilton_fre[key] = (tri_hamilton_n[key]) / (subtri_dict[t])
# printDict(tri_hamilton_fre)
print("for tri_hamilton file: ",find_probablty(tri_hamilton_fre))


addTriAndBi(tri_madison_l,bi_madison_n,tri_madison_n)
msubtri_dict={}
for k in tri_madison.keys():
    w=k.split(" ")[0]+" "+k.split(" ")[1]
    addToDict(w,msubtri_dict)
for key in tri_madison.keys():
    t = key.split(" ")[0] + " " + key.split(" ")[1]
    tri_madison_fre[key] = (tri_madison[key]) / (msubtri_dict[t])
print("for tri_madison file: ",find_probablty(tri_madison_fre))

