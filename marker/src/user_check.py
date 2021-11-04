import pandas as pd
import cv2
import copy
from tkinter import *
from tkinter.ttk import Combobox
import numpy as np
from PIL import ImageTk
from PIL import Image
from threading import Thread
from time import sleep
import os

class User_check:
    def __init__(self,img_path,data_frame,scale_percent=0.50):
        self.img_path=img_path
        self.img = cv2.imread(img_path)
        self.base_image=cv2.imread(img_path)
        self.data_frame = data_frame
        self.scale_percent=scale_percent
        root= Tk()
        self.scale_percent = (root.winfo_screenheight()-50)/self.img.shape[0]
        root.destroy()
        self.width = int(self.img.shape[1] * self.scale_percent)
        self.height = int(self.img.shape[0] * self.scale_percent)
        self.reactangles=[[(int(self.data_frame.x1[i]*self.scale_percent),int(self.data_frame.y1[i]*self.scale_percent)),
                            (int(self.data_frame.x2[i]*self.scale_percent),int(self.data_frame.y2[i]*self.scale_percent)),
                            self.data_frame['class'][i].split('.')[-1],""] for i in range (0,self.data_frame.shape[0])]
        self.dsize = (self.width, self.height)
        self.img = cv2.resize(self.img, self.dsize)
        self.base_image = cv2.resize(self.base_image, self.dsize)
        self.ix = -1
        self.iy = -1
        self.drawing = False
        self.Key=-1
        self.text=''
        self.Background=0
        self.general_run=False
        self.set_type_run=False
        self.selected = []
        self.type=""

    def run(self):
        Winname = "KnowCode 18:39-15-10-2020"
        self.rebuild_image()
        cv2.namedWindow(winname= Winname)
        cv2.setMouseCallback(Winname, self.draw_reactangle)
        while True:
            
            cv2.imshow(Winname, self.img)
            sleep(0.03)
            key = cv2.waitKey(10)
            if key== ord("g"):
                self.general_run=True
                Thread(target = self.general_info,args=[]).start()
                sleep(0.1)
            if key>-1:
                self.Key=key
            if key == 27:
                break
            if key == ord('l'):
                self.delete()
                if not os.path.isfile(self.img_path):
                    break

        cv2.destroyAllWindows()
        
        self.reactangles.sort(key=self.area,reverse=True)
        
        if os.path.isfile(self.img_path):
            return self.reactangles,self.width,self.height,self.scale_percent,self.Background
        return 0,0,0,0,0
    def area(self,rec):
        xi,yi =rec[0]
        xf,yf =rec[1]
        W = xf-xi
        H = yf-yi
        return W*H
    def update_dots(self,rec):
        xi,yi =rec[0]
        xf,yf =rec[1]
        p1= (xi if xi<xf else xf,yi if yi<yf else yf)
        p2= (xf if xi<xf else xi,yf if yi<yf else yi)
        new = [p1,p2,rec[2],rec[3]]
        return new

    def general_changes(self,general,new_infos):
        
        self.Background = new_infos[0]
        new_infos[1]=new_infos[1]/100
        self.width = int((self.width/self.scale_percent)*new_infos[1])
        self.height =int((self.height/self.scale_percent)*new_infos[1])
        for i in range(len(self.reactangles)):
            p1=self.reactangles[i][0]
            p2=self.reactangles[i][1]
            p1=(int((p1[0]/self.scale_percent)*new_infos[1]),int((p1[1]/self.scale_percent)*new_infos[1]))
            p2=(int((p2[0]/self.scale_percent)*new_infos[1]),int((p2[1]/self.scale_percent)*new_infos[1]))
            self.reactangles[i][0]= p1
            self.reactangles[i][1]= p2
            
            
        self.scale_percent = new_infos[1]

        self.dsize = (self.width, self.height)
        self.rebuild_image()
        # self.general_run=False
    def general_set_type(self,component,Id):
        self.set_set_type_run(True)
        self.selected.append(Id)
        Thread(target = self.set_type(component,Id),args=[]).start()
        
    def set_general_run(self,general_run=False):
        self.general_run=general_run
    def psleep(self):
        
        sleep(0.03)

    def win_run(self,run):
        if run == "general":
            return self.general_run
        return self.set_type_run
    def win_loop(self,root,p,run,Id=-1,Action = ...):
        root.protocol("WM_DELETE_WINDOW", ...)
        while self.win_run(run):
            self.rebuild_image()
            root.update()
            root.after(50,self.psleep())
        root.quit()
        root.destroy()
        if Id>-1:
            self.selected.remove(Id)
        if run == "general" and len(self.selected)>0:
            self.selected.pop(0)
        self.rebuild_image()
    def general_visual(self,components):
        if len(components['values'])!=len(self.reactangles):
            print("update")
            self.selected.remove(components.current())
            components.set("")
            component_list = []
            for c in self.reactangles:
                comp = f"X:{c[0][0]},Y:{c[0][1]}, {c[2]}"
                component_list.append(comp)
            components['values'] = component_list
        elif not components.current() in self.selected and components.current()>=0:
            
            if len(self.selected)>0:
                self.selected.pop()
            self.selected.append(components.current())
        self.rebuild_image()
        # components["old"]=components.current()
    def general_info(self,temp=0):
        general = Tk()
        L1=Label(general,text="Background")
        L1.grid(row=0)
        # L1.after(100,self.teste("General"))
        
        Background= Entry(general, bd=5)
        Label(general,text="img size %").grid(row=1)
        Resize= Entry(general, bd=5)

        if self.Background == "":
            self.Background=self.unique_count_app(self.img)
        
        if temp!=0:
            Background.insert(0,temp[0])
            Resize.insert(0,temp[1])
        else:
            Background.insert(0,self.Background)
            Resize.insert(0,str(self.scale_percent*100))

        Background.grid(row=0, column=1)
        Resize.grid(row=1, column=1)

        Label(general,text="component").grid(row=2)
        component_list = []
        for c in self.reactangles:
            comp = f"X:{c[0][0]},Y:{c[0][1]}, {c[2]}"
            component_list.append(comp)
        components =Combobox(general,values=component_list)
        components.set("")
        components.bind("<FocusIn>",  lambda event: self.general_visual(components))
        components.grid(row=2, column=1)

        Select = Button(general, text="Select", width=10,height=1, command=lambda :self.general_set_type(self.reactangles[components.current()],components.current()))

        Select.grid(row=3, column=1)

        Save = Button(general, text="SAVE", width=15,height=2, command=lambda : self.general_changes(general,
                        [Background.get(), float(Resize.get())]))
        Save.grid(row=5, column=1)

        Close = Button(general, text="Close", width=15,height=2, command=lambda : self.set_general_run())
        Close.grid(row=5, column=0)
        general.title("General")
        self.win_loop(general,"General","general")
        
        # general.mainloop()
    def func(self,root,new_component,component):
        # print(name)
        
        if new_component!= 0 and new_component[2]:
            
            self.reactangles.append(self.update_dots(new_component))
            self.type=new_component[2]
            self.reactangles.remove(component)
            self.set_set_type_run()
            
        elif new_component== 0:
            self.reactangles.remove(component)
            self.set_set_type_run()
        
        
        self.rebuild_image()
        # cv2.imshow("OpenCV Teste", self.img)
    
    def imgName(self,root,name,component):
        component[3]=name
        self.set_set_type_run()
        print(component)
    def set_set_type_run(self,set_type_run=False):
        self.set_type_run=set_type_run
    def delbt(self,root):
        os.remove(f"./{self.img_path}")
        if os.path.isfile(f"./train/{self.img_path}"):
            os.remove(f"./train/{self.img_path}")
            os.remove(f"./train/{self.img_path[:-4]}.xml")
        if os.path.isfile(f"./{self.img_path[:-4]}.json"):
            os.remove(f"./{self.img_path[:-4]}.json")
        if os.path.isfile(f"./{self.img_path[:-4]}.xml"):
            os.remove(f"./{self.img_path[:-4]}.xml")
        root.destroy()
    def delete(self):
        root = Tk()
        root.title("Delete")
        Delete = Button(root, text="Delete", width=15,height=2, command=lambda : self.delbt(root))
        Delete.grid(row=0, column=0)
        Close = Button(root, text="Close", width=15,height=2, command=lambda : root.destroy())
        Close.grid(row=0, column=1)
        root.mainloop()
    def set_type(self,component,Id):
        root = Tk()
        root.title("component")
        mylist =    ["carimbo_med",
                    "assinatura_med"]

        xi,yi =component[0]
        xf,yf =component[1]
        W = int(xf-xi)
        H = int(yf-yi)
        Name= Entry(root, bd=5)
        Name.insert(0,component[3])
        
        x1= Entry(root, bd=5)
        x1.insert(0,round(xi/self.scale_percent,2))

        y1= Entry(root, bd=5)
        y1.insert(0,round(yi/self.scale_percent,2))

        Width= Entry(root, bd=5)
        Width.insert(0,round(W/self.scale_percent,2))

        Height= Entry(root, bd=5)
        Height.insert(0,round(H/self.scale_percent,2))
        
        Label(root,text="Type").grid(row=0)
        
        Type =Combobox(root,values=mylist,height=len(mylist))
        Type.set(component[2] if component[2]!="" else self.type)
        Type.grid(row=0, column=1)
        # Type.configure(Height)
        Label(root,text="img Name").grid(row=1)
        
        Label(root,text="position X").grid(row=2)
        Label(root,text="position Y").grid(row=3)
        Label(root,text="Width").grid(row=4)
        Label(root,text="Height").grid(row=5)
        
        
        Name.grid(row=1, column=1)
        x1.grid(row=2, column=1)
        y1.grid(row=3, column=1)
        Width.grid(row=4, column=1)
        Height.grid(row=5, column=1)
        

        Save = Button(root, text="SAVE", width=15,height=2, command=lambda : self.func(root,
                        [(int(float(x1.get())*self.scale_percent),int(float(y1.get())*self.scale_percent)),
                        (int((float(x1.get())+float(Width.get()))*self.scale_percent),int((float(y1.get())+float(Height.get()))*self.scale_percent)),
                        Type.get(),
                        Name.get()],component) )
        Save.grid(row=6, column=1)

        Delete = Button(root, text="Delete", width=15,height=2, command=lambda : self.func(root,0,component))
        Delete.grid(row=6, column=0)

        self.win_loop(root,"components","components",Id)
        
        

    def draw(self,image,p1,p2,text,select=False):  # desenha retangulo com marcações
        Color = (0,255,255)
        Thickness = 1
        if select:
            Color = (255,255,0)
            Thickness = 2
        cv2.rectangle(image, pt1=(p1), pt2=(p2),color=Color,thickness=Thickness)
        cv2.circle(image,p1,5,(0,255,0),cv2.FILLED)
        cv2.circle(image,p2,5,(0,255,0),cv2.FILLED)
        p= p1 if p1[0]<p2[0] else p2
        cv2.putText(image,text,(p[0]+2,p[1]+16),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200, 0, 0),1,cv2.LINE_AA)
        
    def rebuild_image(self): # re cria imagem com retagulos que não serão modificados
        self.base_image = cv2.imread(self.img_path)
        self.base_image = cv2.resize(self.base_image, self.dsize)
        for i in range(len(self.reactangles)):
            select = False
            if i in self.selected:
                select=True
            r = self.reactangles[i]
            self.draw(self.base_image,r[0],r[1],r[2],select)
        self.img=self.base_image

    def get_rectangle(self,x,y): # busca retangulo 
        # print(len(self.reactangles))
        Id=0
        R=[]
        for i in range(len(self.reactangles)):
            r=self.reactangles[i]
            xi,yi=r[0]
            xf,yf=r[1]
            
            if ((xi-x)<6 and (xi-x)>-6) and ((yi-y)<6 and (yi-y)>-6):
                self.reactangles.remove(r)
                # print(len(self.reactangles))
                return xf,yf,r[2]
            elif ((x-xf)<6 and (x-xf)>-6) and ((y-yf)<6 and (y-yf)>-6):
                self.reactangles.remove(r)
                # print(len(self.reactangles))
                return xi,yi,r[2]
            elif ((x<xf and x>xi)and(y>yi and y<yf)) or((x>xf and x<xi)and(y<yi and y>yf)):
                
                if len(R)==0:
                    Id=i
                    R=r
                else:
                    xei,yei=R[0]
                    xef,yef=R[1]
                    if(xf<xef and xi>xei and yf<yef and yi>yei) or (xf>xef and xi<xei and yf>yef and yi<yei):
                        Id=i
                        R=r
        if len(R)>0:        
            self.general_set_type(R,Id) 
        return  -1,-1,''

    def draw_reactangle(self,event, x, y, flags, param):
        # cria retangulos
        if event == cv2.EVENT_LBUTTONDOWN and self.Key == ord('d'):
            self.drawing = True
            self.ix = x
            self.iy = y
            self.text=''

        elif event == cv2.EVENT_LBUTTONUP and (self.Key == ord('d') or  self.Key == ord('r')) :
            self.drawing = False
            self.draw(self.base_image,(self.ix,self.iy),(x,y),self.text,self.drawing)
            self.img = self.base_image
            self.reactangles.append(self.update_dots([(self.ix,self.iy),(x, y),self.text,""]))
            if self.text=='':
                self.general_set_type(self.reactangles[-1],len(self.reactangles)-1)
                
            # print(self.reactangles)
        # redimenciona retangulos
        elif event == cv2.EVENT_LBUTTONDOWN and (self.Key == ord('r')or self.Key == ord('t')):
            
            self.ix,self.iy,self.text = self.get_rectangle(x,y)
            if self.ix>0:
                self.rebuild_image()
                self.drawing = True

        elif event == cv2.EVENT_LBUTTONUP  and self.Key == ord('t'):
            if self.drawing == True:
                self.drawing = False
                self.draw(self.base_image,(self.ix,self.iy),(x,y),self.text,self.drawing)
                self.img = self.base_image
                self.reactangles.append(self.update_dots([(self.ix,self.iy),(x, y),self.text,""]))
                # print(self.reactangles)
        # movendo retangulo junto com o movimento do mouse
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                img2 = copy.copy(self.base_image)
                self.draw(img2,(self.ix,self.iy),(x,y),self.text,self.drawing)
                self.img = img2
