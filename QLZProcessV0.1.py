import os
import re
import sys
#==========================================================
def  processFile(filedir):
    pstr=readFile(filedir)
    string=process(pstr)
    addr=filedir[0:19]+"Result"+filedir[filedir.rfind("\\"):]
    addr=addr.replace('html','txt')
    writeFile(addr,string)
    print("===%s"%(addr))

def  readFile(filedir):
    pstr=''
    with open(filedir, "r", encoding='utf-8') as f :
        pstr = f.read()
    return pstr

def writeFile(filedir,string):
    path = filedir[0:filedir.rfind("\\")]
    path = path[0:path.rfind("\\")]
    if not os.path.exists(path):
        os.makedirs(path) 
    with open(filedir, "w+", encoding='utf-8') as f:
        f.write(string)
        
#============================================
def  process(pstr):    

    pstr = getBetween(pstr,'<div class="middle clearfix">','<div class="page_box">','10')
    lis=pstr.split('<h3 class="title2">')
    string=''
    for i in range(len(lis)):
        if lis[i].find('<p style="line-height:')!=-1:
            
            lis[i]=lis[i].replace(' ','')#u0020
            lis[i]=re.sub(r'<br><br>.{1,20}<br>','\n\n',lis[i])
            lis[i]=re.sub(r'<br>　　　','',lis[i])
            lis[i]=lis[i].replace('<br>　　','\n\n')
            lis[i]=lis[i].replace('<br>','\n\n') 
            lis[i]=lis[i].replace('</p>','\n')
            lis[i]=re.sub(r'<pstyle="line-height:200%;">.{0,15}\n','',lis[i])
            lis[i]=re.sub(r'<pstyle="line-height:200%;">','',lis[i])
            lis[i]=re.sub(r'<!--.+-->','',lis[i])
            lis[i]=re.sub(r'\[.{3,10}\]','⛔',lis[i])#組字式    [(膘-示+土)+瓦][麩-夫+廣][疊*毛] 
            lis[i]=re.sub(r'\n?.+h3>','',lis[i])
            lis[i]=lis[i].replace('　','') #u3000
            lis[i]=lis[i].replace('	','') #u0009

            ts=lis[i][0:min(2000,len(lis[i]))]
            if ts.count('，')+ts.count('？')+ts.count('：')+ts.count('“')==0:
                lis[i]=''

            string+=lis[i]
    while(string.find('\n\n\n')!=-1):
        string=string.replace('\n\n\n','\n\n')
    string=string.lstrip('\n').rstrip('\n')
    # lsp=string.split('\n\n')
    # for i in range(0,len(lsp)):        
    #     if (lsp[i].endswith('。') or lsp[i].endswith('？') or lsp[i].endswith('！') or lsp[i].endswith('”') or lsp[i].endswith('’')) ==False:
    #         lsp[i]=''

    # string='\n\n'.join(lsp)
    # while(string.find('\n\n\n')!=-1):
    #     string=string.replace('\n\n\n','\n\n')
    string=string.lstrip('\n').rstrip('\n')
    return string   

def getBetween(string,start,end,mode='10'):
    #mode ={00-前無後無,10=前有后無,11=前有後有}
    if mode == '00':
        s=string.find(start)+len(start)
        e=string.find(end)
        string=string[s:e]
    elif mode =='10':
        s=string.find(start)
        e=string.find(end)
        string=string[s:e]
    elif mode=='11':
        s=string.find(start)
        e=string.find(end)+len(end)
        string=string[s:e]
    else:
        pass
    return string

#==========================================================
if __name__ == '__main__':
    if len(sys.argv)>1 :
        path=sys.argv[1]
    else :        
        print ("---$:usage: cbetaDataProcess.py dirname.")
        sys.exit(1)
        # path='H:/WORKSPACE/QLZ_s/QLZ'
    print ("--------$:building file lists...")
    fileList = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if file.endswith('.html'):
                 fileList.append(os.path.join(dirpath, file))
    amax=len(fileList)
    for i in range(0,amax):
        print("%3d/%s---$:   %s"%(i+1,amax,fileList[i]))
        processFile(fileList[i])        
        # break#-----------------------------------
    print ("--------$:file lists built.")
#==========================================================
