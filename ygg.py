import sys,time
def split(a:str) -> list[tuple[str]]:
 res=[]
 i=0
 j=""
 while i<len(a):
  if a[i]=='"':
   i+=1
   while i<len(a) and a[i]!='"':
    j+=a[i]
    i+=1
   res.append(("s",j));j=""
  elif a[i].isdigit():
   while i<len(a) and a[i].isdigit():
    j+=a[i]
    i+=1
   if a[i]=="n":
    j=str(int(j)*-1)
   res.append(("i",j));j=""
  elif not a[i] in " \t\r\n":
   while i<len(a) and not a[i] in " \t\r\n":
    j+=a[i]
    i+=1
   res.append(("f",j));j=""
  i+=1
 return res

label={}
stack=[]
si=[]
cflag=0 # 1 - eq; 2 - lt; 3 - gt
# 1 - push
# 2 - pop
# 3 - out; 3.1 - echo
# 4 - flip
# 5 - goto; 5.1 - gote; 5.2 - gotl; 5.3 - gotg; 5.4 - ret
# 6 - cmp
# 7 - label
# 8 - inc; 8.1 - dec
# 9 - copy
# a - add; a.1 - sub; a.2 - mul; a.3 - div

def tobc(src):
 res=[]
 npush=False
 for i in src:
  if i[0]=="s" or i[0]=="i":
   res.extend([10,list(i)] if not npush else [list(i)])
   npush=False
  elif i[0]=="f":
   if i[1]=="pop": res.append(20)
   elif i[1]=="out": res.append(30)
   elif i[1]=="echo": res.append(31)
   elif i[1]=="flip": res.append(40)
   elif i[1]=="goto":
    res.append(50)
    npush=True
   elif i[1]=="gote":
    res.append(51)
    npush=True
   elif i[1]=="gotl":
    res.append(52)
    npush=True
   elif i[1]=="gotg":
    res.append(53)
    npush=True
   elif i[1]=="ret": res.append(54)
   elif i[1]=="cmp": res.append(60)
   elif i[1]=="label":
    res.append(70)
    npush=True
   elif i[1]=="inc": res.append(80)
   elif i[1]=="dec": res.append(81)
   elif i[1]=="copy": res.append(90)
   elif i[1]=="add": res.append(100)
   elif i[1]=="sub": res.append(101)
   elif i[1]=="mul": res.append(102)
   elif i[1]=="div": res.append(103)
   else: res.append(0)
 return res

def _eval(code):
 global cflag,stack,si
 i=0
 while i<len(code):
  print(stack)
  print(label)
# print(code[i])
# print(cflag)
  print(si)
# time.sleep(0.25)
  if code[i]==0:
   print("Invalid instruction")
   return
  elif code[i]==10:
   i+=1
   stack.append(code[i])
  elif code[i]==20:
   try: stack.pop()
   except IndexError:
    print("Cannot Pop")
    return
  elif code[i]==30:
   if len(stack)==0:
    print("No Items Pushed In Stack")
    return
   print(stack.pop()[1],end="")
  elif code[i]==31:
   if len(stack)==0:
    print("No Items Pushed In Stack")
    return
   print(stack.pop()[1])
  elif code[i]==40:
   stack.reverse()
  elif code[i]==50:
   i+=1
   si.append(i)
   if code[i][0]=="i":
    i=int(code[i][1])-2
    cflag=0
   elif code[i][0]=="s":
    i=label[code[i][1]] if code[i][1]!="$" else len(code)-1
    cflag=0
   else:
    print("GT:Not A Number Or Label")
    return
  elif code[i]==51 and cflag==1:
   i+=1
   si.append(i)
   if code[i][0]=="i":
    i=int(code[i][1])-2
   elif code[i][0]=="s":
    i=label[code[i][1]] if code[i][1]!="$" else len(code)-1
   else:
    print("GE:Not A Number Or Label")
    return
  elif code[i]==52 and cflag==2:
   i+=1
   si.appendld(i)
   if code[i][0]=="i":
    i=int(code[i][1])-2
    cflag=0
   elif code[i][0]=="s":
    i=label[code[i][1]] if code[i][1]!="$" else len(code)-1
    cflag=0
   else:
    print("GL:Not A Number Or Label")
    return
  elif code[i]==53 and cflag==3:
   i+=1
   si.append(i)
   if code[i][0]=="i":
    i=int(code[i][1])-2
    cflag=0
   elif code[i][0]=="s":
    i=label[code[i][1]] if code[i][1]!="$" else len(code)-1
    cflag=0
   else:
    print("GG:Not A Number Or Label")
    return
  elif code[i]==54:
   if len(si)>0: i=si.pop()-1
   else:
    print("Cannot Return")
    return
  elif code[i]==60:
   if int(stack[-1][1])==int(stack[-2][1]): cflag=1
   elif int(stack[-1][1])<int(stack[-2][1]): cflag=2
   elif int(stack[-1][1])>int(stack[-2][1]): cflag=3
   else:
    print("Cannot Compare")
    return
  elif code[i]==70:
   i+=1
   if code[i][0]=="s":
    if code[i][1] in ["ip","$"]:
     print("Label Cannot Have %s as A Name" % (code[i][1]))
     return
    label[code[i][1]]=i
   else:
    print("Not A String")
  elif code[i]==80:
   stack[-1][1]=str(int(stack[-1][1])+1)
  elif code[i]==81:
   stack[-1][1]=str(int(stack[-1][1])-1)
  elif code[i]==90:
   stack.append(stack[-1])
  elif code[i]==100:
   stack.append(["i",str(int(stack.pop()[1])+int(stack.pop()[1]))])
  elif code[i]==101:
   stack.append(["i",str(int(stack.pop()[1])-int(stack.pop()[1]))])
  elif code[i]==102:
   stack.append(["i",str(int(stack.pop()[1])*int(stack.pop()[1]))])
  elif code[i]==103:
   stack.append(["i",str(int(int(stack.pop()[1])/int(stack.pop()[1])))])
  i+=1
 return

def main(file):
 fin=open(file,"r")
 src=fin.read()
 code=tobc(split(src))
 print(code)
 _eval(code)
 fin.close()
 return

if __name__=="__main__":
 if len(sys.argv)==1:
  print("No File Found")
  exit(-1)
 main(sys.argv[1])
