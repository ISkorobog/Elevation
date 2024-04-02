from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot
from matplotlib import cm
import requests,json
import tkinter as tk
import random
import os 

apikey=""
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.z=0



def on_submit():
    x=float(entry2.get())
    y=float(entry.get()) 
    d=float(entryd.get())
    xl=x-d/2
    yl=y+d/2
    ran=int(entryr.get())
    points=[]
    for i in range(ran):
        for j in range(ran):
            points.append(Point(round(xl+i*d/ran,6),round(yl-j*d/ran,6)))
    reqnum=(ran*ran)//512+1
    for t in range(reqnum):
        serviceURL="https://maps.googleapis.com/maps/api/elevation/json?locations="
        l=t*512
        r=l+512
        if(r>ran*ran):
            r=ran*ran
        for i in range(l,r-1):
            serviceURL=serviceURL+str(points[i].y)+","+str(points[i].x)+"|" 
        serviceURL=serviceURL+str(points[r-1].y)+","+str(points[r-1].x)+"&key="+apikey
        r=requests.get(serviceURL)
        y=json.loads(r.text)
        k=0
        for result in y["results"]:
            elev=result["elevation"]
            points[l+k].z=elev
            k=k+1
    mi=1000000
    ma=-1000000
    for p in points:
        if(mi>p.z):
            mi=p.z
        if(ma<p.z):
            ma=p.z
    img=np.zeros((ran,ran))
    if(ma<mi+500):
        ma=mi+500
    k=0
    for i in range(ran*ran):
        img[i//ran,i%ran]=(points[i].z-mi)/(ma-mi)
    matplotlib.pyplot.imsave("map\\"+entryn.get()+".png", img,cmap='gray')
    x, y = np.meshgrid(range(img.shape[0]), range(img.shape[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, img/10,cmap=cm.winter)
    ax.set_box_aspect((1,1,0.2))
    plt.title('z as 3d height map')
    plt.show()




def on_submit2():
    os.mkdir("maps\\"+entryn.get()) 
    for tt in range(int(entryk.get())):
        x=30*random.random()
        y=49+random.random()*3
        d=float(entryd2.get())
        xl=x-d/2
        yl=y+d/2
        ran=int(entryr.get())
        points=[]
        for i in range(ran):
            for j in range(ran):
                points.append(Point(round(xl+i*d/ran,6),round(yl-j*d/ran,6)))
        reqnum=(ran*ran)//512+1
        for t in range(reqnum):
            serviceURL="https://maps.googleapis.com/maps/api/elevation/json?locations="
            l=t*512
            r=l+512
            if(r>ran*ran):
                r=ran*ran
            for i in range(l,r-1):
                serviceURL=serviceURL+str(points[i].y)+","+str(points[i].x)+"|" 
            serviceURL=serviceURL+str(points[r-1].y)+","+str(points[r-1].x)+"&key="+apikey
            r=requests.get(serviceURL)
            y=json.loads(r.text)
            k=0
            for result in y["results"]:
                elev=result["elevation"]
                points[l+k].z=elev
                k=k+1
        mi=1000000
        ma=-1000000
        for p in points:
            if(mi>p.z):
                mi=p.z
            if(ma<p.z):
                ma=p.z
        img=np.zeros((ran,ran))
        if(ma<mi+500):
            ma=mi+500
        k=0
        for i in range(ran*ran):
            img[i//ran,i%ran]=(points[i].z-mi)/(ma-mi)
        matplotlib.pyplot.imsave("maps\\"+entryn.get()+"\\"+entryn.get()+str(tt)+".png", img,cmap='gray')
        

app = tk.Tk()
app.title("Python Desktop App")
app.geometry("500x300")

labelr=tk.Label(app,text="Введіть розмір карти висот:")
labelr.place(x=190,y=10)
entryr=tk.Entry(app)
entryr.place(x=200,y=30)
labeln = tk.Label(app, text="Введіть назву карти:")
labeln.place(x=200,y=50)
entryn = tk.Entry(app)
entryn.place(x=200,y=70)
label = tk.Label(app, text="Введіть широту центру:")
label.place(x=100,y=90)
entry = tk.Entry(app)
entry.place(x=100,y=110)
label2 = tk.Label(app, text="Введіть довготу центру:")
label2.place(x=100,y=130)
entry2 = tk.Entry(app)
entry2.place(x=100,y=150)
labeld = tk.Label(app, text="Введіть радіус карти:")
labeld.place(x=100,y=170)
entryd = tk.Entry(app)
entryd.place(x=100,y=190)
submit_button = tk.Button(app, text="Отримати карту", command=on_submit)
submit_button.place(x=100,y=210)
labelk = tk.Label(app, text="Введіть кількість карт:")
labelk.place(x=300,y=90)
entryk = tk.Entry(app)
entryk.place(x=300,y=110)
labeld2 = tk.Label(app, text="Введіть радіус карти:")
labeld2.place(x=300,y=130)
entryd2 = tk.Entry(app)
entryd2.place(x=300,y=150)
submit_button2 = tk.Button(app, text="Отримати карти", command=on_submit2)
submit_button2.place(x=300,y=170)

app.mainloop()
