#!/usr/local/bin/python3
import os
import sys
import csv
from optparse import OptionParser  

"""
1、每次采集时，每个传感器内的数据条数最小为100条，也即上面的图中对应的行数最小为100行
4、提供过来的数据表的格式： 12个传感器的数据最终汇聚成一个数据表，样例如附件的形式，
		1、表列的名称为如下，37个列名：
Time_Acc', 'Acc_x', 'Acc_y', 'Acc_z’, 'Time_Gra', 'Gra_x', 'Gra_y’, 'Gra_z’, 'Time_Gyr', 'Gyr_x', 'Gyr_y', 'Gyr_z’, 'Time_Light', 'Light','Time_LAcc', 'LAcc_x', 'LAcc_y', 'LAcc_z', 'Time_Mag', 'Mag_x', 'Mag_y','Mag_z', 'Time_Pres', 'Pres', 'Time_Prox', 'Prox’, 'Time_ReHum','ReHum', 'Time_Rov', 'Rov_w', 'Rov_x', 'Rov_y', 'Rov_z', 'Time_SteCou','SteCou', 'Time_TSD', 'TSD_value', 'id’,
	 2、其中 id列表示的是每次采集数据的标识，即同一次采集下id值一致，每次采集id值加1，
	 3、其余列为传感器的数据内容  

"""
"""
stop 0 , sport 1 

"""
FILELEN = 12 #( DS_Store +12files)

headers=['Time_Acc', 'Acc_x', 'Acc_y','Acc_z','Time_Gra', 'Gra_x', 'Gra_y', 'Gra_z', 'Time_Gyr', 'Gyr_x', 'Gyr_y', 'Gyr_z', 'Time_Light', 'Light','Time_LAcc', 'LAcc_x', 'LAcc_y', 'LAcc_z', 'Time_Mag', 'Mag_x', 'Mag_y','Mag_z', 'Time_Pres', 'Pres', 'Time_Prox', 'Prox','Time_ReHum','ReHum', 'Time_Rov', 'Rov_w', 'Rov_x', 'Rov_y', 'Rov_z', 'Time_SteCou','SteCou', 'Time_TSD', 'TSD_value','id','scenario','behavior','class']
csvw=None

fdaccd=None
fdgrad=None 
fdgyrd=None
fdlightd=None
fdlineard=None
fdmagd=None
fdpred=None 
fdproxid=None
fdrelad=None
fdrotad=None
fdstepd=None
fdtyped=None

filemaxline=0

scenario=0
behavior=0
csvclass=0
csvid=0

def dealacc(datasrc,index):
    if index > fdaccd[1]-1:
        datasrc['Time_Acc'] = 0
        datasrc['Acc_x'] = 0 
        datasrc['Acc_y'] = 0
        datasrc['Acc_z'] = 0
        #error
    else :
        data = fdaccd[0][index].replace('\n','').split('|')
        datasrc['Time_Acc'] = float(data[0])
        datasrc['Acc_x'] = float(data[1])
        datasrc['Acc_y'] = float(data[2])
        datasrc['Acc_z'] = float(data[3])
def dealgra(datasrc,index):
    if index > fdgrad[1]-1:
        datasrc['Time_Gra'] = 0
        datasrc['Gra_x'] = 0 
        datasrc['Gra_y'] = 0
        datasrc['Gra_z'] = 0
        #error
    else :
        data = fdgrad[0][index].replace('\n','').split('|')
        datasrc['Time_Gra'] = float(data[0])
        datasrc['Gra_x'] = float(data[1])
        datasrc['Gra_y'] = float(data[2])
        datasrc['Gra_z'] = float(data[3])
def dealgyr(datasrc,index):
    if index > fdgyrd[1]-1:
        datasrc['Time_Gyr'] = 0
        datasrc['Gyr_x'] = 0 
        datasrc['Gyr_y'] = 0
        datasrc['Gyr_z'] = 0
    else :
        data = fdgyrd[0][index].replace('\n','').split('|')
        datasrc['Time_Gyr'] = float(data[0])
        datasrc['Gyr_x'] = float(data[1])
        datasrc['Gyr_y'] = float(data[2])
        datasrc['Gyr_z'] = float(data[3])
def deallight(datasrc,index):
    if index > fdlightd[1]-1:
        datasrc['Time_Light'] = 0
        datasrc['Light'] = 0 
    else :
        data = fdlightd[0][index].replace('\n','').split('|')
        datasrc['Time_Light'] = float(data[0])
        datasrc['Light'] = float(data[1])
def deallinear(datasrc,index):
    if index > fdlineard[1]-1:
        datasrc['Time_LAcc'] = 0
        datasrc['LAcc_x'] = 0
        datasrc['LAcc_y'] = 0
        datasrc['LAcc_z'] = 0
    else :
        data = fdlineard[0][index].replace('\n','').split('|')
        datasrc['Time_LAcc'] = float(data[0])
        datasrc['LAcc_x'] = float(data[1])
        datasrc['LAcc_y'] = float(data[2])
        datasrc['LAcc_z'] = float(data[3])
def dealmag(datasrc,index):
    if index > fdmagd[1]-1:
        datasrc['Time_Mag'] = 0
        datasrc['Mag_x'] = 0 
        datasrc['Mag_y'] = 0
        datasrc['Mag_z'] = 0
        #error
    else :
        data = fdmagd[0][index].replace('\n','').split('|')
        datasrc['Time_Mag'] = float(data[0])
        datasrc['Mag_x'] = float(data[1])
        datasrc['Mag_y'] = float(data[2])
        datasrc['Mag_z'] = float(data[3])
def dealpre(datasrc,index):
    if index > fdpred[1]-1:
        datasrc['Time_Pres'] = 0
        datasrc['Pres'] = 0 
    else :
        data = fdpred[0][index].replace('\n','').split('|')
        datasrc['Time_Pres'] = float(data[0])
        datasrc['Pres'] = float(data[1])
def dealproxi(datasrc,index):
    if index > fdproxid[1]-1:
        datasrc['Time_Prox'] = 0
        datasrc['Prox'] = 0 
    else :
        data = fdproxid[0][index].replace('\n','').split('|')
        datasrc['Time_Prox'] = float(data[0])
        datasrc['Prox'] = float(data[1])
def dealrela(datasrc,index):
    if index > fdrelad[1]-1:
        datasrc['Time_ReHum'] = 0
        datasrc['ReHum'] = 0 
    else :
        data = fdrelad[0][index].replace('\n','').split('|')
        datasrc['Time_ReHum'] = float(data[0])
        datasrc['ReHum'] = float(data[1])
def dealrota(datasrc,index):
    if index > fdrotad[1]-1:
        datasrc['Time_Rov'] = 0
        datasrc['Rov_w'] = 0
        datasrc['Rov_x'] = 0 
        datasrc['Rov_y'] = 0
        datasrc['Rov_z'] = 0
    else :
        data = fdrotad[0][index].replace('\n','').split('|')
        datasrc['Time_Rov'] = float(data[0])
        datasrc['Rov_w'] = float(data[1])
        datasrc['Rov_x'] = float(data[2])
        datasrc['Rov_y'] = float(data[3])
        datasrc['Rov_z'] = float(data[4])
def dealstep(datasrc,index):
    if index > fdstepd[1]-1:
        datasrc['Time_SteCou'] = 0
        datasrc['SteCou'] = 0 
    else :
        data = fdstepd[0][index].replace('\n','').split('|')
        datasrc['Time_SteCou'] = float(data[0])
        datasrc['SteCou'] =int(data[1])
def dealtype(datasrc,index):
    if index > fdtyped[1]-1:
        datasrc['Time_TSD'] = 0
        datasrc['TSD_value'] = 0 
    else :
        data = fdtyped[0][index].replace('\n','').split('|')
        datasrc['Time_TSD'] = float(data[0])
        datasrc['TSD_value'] = float(data[1])

def getSceAndBeType(scenario , behavior):
    if scenario == 'stop':
        scenario_value = 0
    else:
        scenario_value = 1

    if behavior== 'none':
        behavie_value = 0
    elif behavior == 'click':
        behavie_value = 1
    else:
        behavie_value = 2
    return (scenario_value,behavie_value)

def getclass(scenario ,behavior):
    if scenario == 0 and behavior ==0 :
        return 0
    if scenario == 0 and behavior ==1 :
        return 1
    if scenario == 0 and behavior ==2 :
        return 2
    if scenario == 1 and behavior ==0 :
        return 3
    if scenario == 1 and behavior ==1 :
        return 4
    if scenario == 1 and behavior ==2 :
        return 5

def openfiles(files,root):
    global fdaccd,fdgrad,fdgyrd,fdlightd,fdlineard,fdmagd,fdpred,fdproxid,fdrelad,fdrotad,fdstepd,fdtyped,filemaxline
    datalen =0 
    for file in files:
        file = os.path.join(root,file)
        if 'ACCELEROMETER' in file:
            fdacc=open(file,'r')
            fdaccd = fdacc.readlines()
            lens = len(fdaccd) 
            if lens > datalen :
                datalen = lens
            fdaccd=[fdaccd,lens]
            fdacc.close()                 
        elif 'GRAVITY' in file :
            fdgra=open(file,'r')
            fdgrad= fdgra.readlines()
            lens = len(fdgrad) 
            if lens > datalen :
                datalen = lens  
            fdgrad=[fdgrad,lens]
            fdgra.close()   
        elif 'GYRO' in file :
            fdgyr=open(file,'r')
            fdgyrd = fdgyr.readlines()
            lens = len(fdgyrd) 
            if lens > datalen :
                datalen = lens  
            fdgyrd=[fdgyrd,lens]
            fdgyr.close()         
        elif 'LIGHT' in file :
            fdlight=open(file,'r')
            fdlightd = fdlight.readlines()
            lens = len(fdlightd) 
            if lens > datalen :
                datalen = lens 
            fdlightd=[fdlightd,lens] 
            fdlight.close()   
        elif 'LINEAR_ACC' in file :
            fdlinear=open(file,'r')
            fdlineard = fdlinear.readlines()
            lens = len(fdlineard) 
            if lens > datalen :
                datalen = lens  
            fdlineard=[fdlineard,lens]
            fdlinear.close()   
        elif 'MAGNE' in file :
            fdmag=open(file,'r')
            fdmagd = fdmag.readlines()
            lens = len(fdmagd) 
            if lens > datalen :
                datalen = lens  
            fdmagd=[fdmagd,lens]
            fdmag.close()   
        elif 'PRESSURE' in file :
            fdpre=open(file,'r')
            fdpred = fdpre.readlines()
            lens = len(fdpred) 
            if lens > datalen :
                datalen = lens  
            fdpred=[fdpred,lens]
            fdpre.close() 
        elif 'PROXIMITY' in file :
            fdproxi=open(file,'r')
            fdproxid = fdproxi.readlines()
            lens = len(fdproxid) 
            if lens > datalen :
                datalen = lens  
            fdproxid=[fdproxid,lens]
            fdproxi.close()
        elif 'RELATIVE' in file :
            fdrela=open(file,'r')
            fdrelad = fdrela.readlines()
            lens = len(fdrelad) 
            if lens > datalen :
                datalen = lens  
            fdrelad=[fdrelad,lens]
            fdrela.close()
        elif 'ROTATION' in file :
            fdrota=open(file,'r')
            fdrotad = fdrota.readlines()
            lens = len(fdrotad) 
            if lens > datalen :
                datalen = lens 
            fdrotad=[fdrotad,lens]
            fdrota.close()
        elif 'STEP' in file :
            fdstep=open(file,'r') 
            fdstepd = fdstep.readlines()
            lens = len(fdstepd) 
            if lens > datalen :
                datalen = lens  
            fdstepd=[fdstepd,lens]
            fdstep.close()
        else :
            fdtype=open(file,'r')
            fdtyped = fdtype.readlines()
            lens = len(fdtyped) 
            if lens > datalen :
                datalen = lens 
            fdtyped=[fdtyped,lens]
            fdtype.close() 
    print('data max len is '+str(datalen))
    filemaxline = datalen

def dealdir(path):
    datasrc ={}
    datacount = 0
    print('deal path'+path)
    files = os.listdir(path)
    files.remove('.DS_Store')
    sce ,beh=files[0].split('_')[:2]
    global scenario,behavior,csvclass,csvid
    scenario,behavior = getSceAndBeType(sce,beh)
    csvclass=getclass(scenario,behavior)
    assert(len(files) == FILELEN)
    openfiles(files,path)
    datasrc['id']= csvid
    datasrc['class']=csvclass
    datasrc['scenario']=scenario
    datasrc['behavior']=behavior
    ### read 
    dataline = 0 
    while dataline < filemaxline :
        dealacc(datasrc , dataline)
        dealgra(datasrc,dataline)
        dealgyr(datasrc,dataline)
        deallight(datasrc,dataline)
        deallinear(datasrc,dataline)
        dealmag(datasrc,dataline)
        dealpre(datasrc,dataline)
        dealproxi(datasrc,dataline)
        dealrela(datasrc,dataline)
        dealrota(datasrc,dataline)
        dealstep(datasrc,dataline)
        dealtype(datasrc,dataline)
        csvw.writerow(datasrc)
        dataline+=1
    ### write row 

    ###

    csvid += 1
    #print(csvid)



def main():
    parser =OptionParser()
    parser.add_option("-d","--dir", dest="dir",help="data directory")
    parser.add_option("-o" , "--output",dest="output", help="output file ")
    (options,args)=parser.parse_args()
    if options.dir is None or options.output is None:
        print("error args")
        exit(-1)
    print("start generate csv")
    root=options.dir
    print("root is", options.dir)
    global csvw
    outfd = open(options.output,'w',newline='', encoding='utf-8') 
    csvw = csv.DictWriter(outfd,fieldnames=headers)
    csvw.writeheader()
    dirlist = os.listdir(options.dir)
    for dir in dirlist:
        path=os.path.join(root,dir)
        if os.path.isdir(path):
            dealdir(path)
    outfd.close()


if __name__ == '__main__':
    main()


