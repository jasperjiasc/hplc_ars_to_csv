import numpy as np
import pandas as pd
import os

def findstdFile(): #find std file to get full AA list
        for f in os.listdir(os.getcwd()): # iterate file in current dir
            if f.endswith(".ars"):
                infile = open(f).read()
                if 'std'in infile:
                    return f

def getstdList(f): #create AA list from std file
    inf = open(f,'rU').readlines() #rU support \r \n \r\n
    count = 0
    temp = 0
    #print(inf[47])
    #print('start')
    for lines in inf:
        if "Amount (nmol/ml)" in lines: # find the line starting the AAs
            #print("found A")
            temp = count
        if "Report Method:  HPLC Report" in lines: # delete unuseful info
            inf[count] = lines.replace('"Report Method:  HPLC Report"','')
        if '"Printed:"	"Page: ' in lines: #delete unsuseful line
            inf.remove(lines)
            count -=1
        count += 1
    #print("done")

    if inf[temp+2].find('"1"') == 0:
        inf = inf[temp+2:] #truncate the file, only keep parts after "amount "
        n = 1
        for lines in inf: # further modify each line
            ind = lines.find('"{}"\t'.format(n))
            if ind >=0:
                if ind != 0:
                    inf[n-1]=lines[ind:] #let each line starting with 'n'
            inf[n - 1] = inf[n-1].replace('"', '').replace('\t', ',').replace('\n','').split(",")
            n+=1

    inf = np.array(inf)[:,[1]]
    inf = pd.DataFrame(inf)
    AAmw = [132.1, 147.1, 132.1, 105.1, 146.2, 155.2, 75.1, 119.1, 121.1, 132.1, 89.1, 125.2, 89.1, 181.2, 204.2, 149.2, 117.1, 165.2, 131.2, 131.2, 132.2, 146.2]
    inf['g/mol'] = AAmw
    inf = inf.rename(columns = {0:'AA'})
    inf = inf[['g/mol','AA']]
    #print (inf)
    return inf

def getSmpValue(list,f): #get sample AA value
    inf = open(f,'rU').readlines()
    #find sample name
    splline = inf[2].replace('"', '')
    i = splline.find('\t')
    splName = splline[0:i]
    #print (splName.find('water'or 'h2o'or'H2O'))
    if splName.find('water')>=0 or splName.find('std') >=0: #skip water and second std in the file
        print 'here1'
        return list
    #print(splName)
    count = 0
    temp = 0

    # print(count)
    for lines in inf:
        #print lines
        if "Amount (nmol/ml)" in lines:
            temp = count
        if "Report Method:  HPLC Report" in lines:
            inf[count] = lines.replace('"Report Method:  HPLC Report"', '')
        if '"Printed:"	"Page: ' in lines:
            inf.remove(lines)
            count -= 1
        count += 1
    print("done")
    #for line in inf:
    #    print inf

    if inf[temp + 2].find('"1"') == 0:
        inf = inf[temp + 2:]
        for lines in inf:
            if len(lines) < 10:
                inf.remove(lines)
        n = 1
        for lines in inf:
            ind = lines.find('"{}"\t'.format(n))
            if ind >= 0:
                #if ind != 0:
                    inf[n - 1] = lines[ind:]
            inf[n - 1] = inf[n - 1].replace('"', '').replace('\t', ',').replace('\n', '').split(",")
            n += 1
    inf = np.array(inf)[:,[1,4]]
    #print  inf
    inf = pd.DataFrame(inf)
    #print inf
    inf = inf.rename(columns={0: 'AA', 1: splName})
    list = pd.merge(list,inf, on = "AA", how= "outer")#merge AA list from std with AA value gotten from samples
    return list

if __name__ == "__main__":
    f = findstdFile()
    #print(f)
    AAlist = getstdList(f)
    for fls in os.listdir(os.getcwd()):
        if fls.endswith(".ars") and fls != f:
            #print fls
            AAlist = getSmpValue(AAlist, fls)
    AAlist = AAlist.T
    AAlist.to_csv('AAresult.csv', index=True, header=True)
    #print(AAlist)

