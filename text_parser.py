#Basic function to parse OBJ file data into list of points
def obj_parser(filename):
    f=open(filename,'r')
    a=f.readline()
    vertexs=[]
    sd=0
    while(True):
        if a[0:2]=='v ':
            a=a.replace("v ","")
            while a[0]==" ":
                a=a[1:len(a)]
            w=a.split(" ")
            vertexs.append([float(w[0]),float(w[1]),float(w[2])])
            sd=1
        elif sd==1:
            break
        a=f.readline()
    return vertexs