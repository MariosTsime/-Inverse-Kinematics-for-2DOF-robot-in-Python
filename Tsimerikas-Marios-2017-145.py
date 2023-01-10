
import tkinter as tk                  #ΓΙΑ SCREEN INFO 
from tkinter import simpledialog
from tkinter import messagebox
import math
from tkinter.constants import E       #ΓΙΑ ΤΡΙΓΟΝΟΜΕΤΡΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ 
from graphics import *                #ΓΙΑ ΓΡΑΦΙΚΑ 
from win32api import GetSystemMetrics #ΓΙΑ ΝΑ ΒΡΩ ΤΙΣ ΔΙΑΣΤΑΣΕΙΣ ΤΗΣ ΟΘΟΝΗΣ 

def InputIntegerFromPopUp(title,message,With_negatives):# ΔΙΑΒΑΖΕΙ ΜΕ ΑΣΦΑΛΕΙΑ ΑΠΟ ΤΟΝ ΧΡΗΣΤΗ ΕΝΑΝ ΑΚΕΡΑΙΟ ΑΡΙΘΜΟ
    while True:

        try:
            ROOT = tk.Tk()
            ROOT.withdraw() # the input dialog
            USER_INP = simpledialog.askstring(title="Είσοδος δεδομένων"+title,prompt=message)
            a = float(USER_INP);
            if (With_negatives==0 and a>0):
              break
            elif (With_negatives==1 & (type(a)==float) ):
                break
            else :
                messagebox.askretrycancel("Input_error","Δεν έδωσες θετικό αριθμό")
            
        except ValueError:
            messagebox.askretrycancel("Input_error",'Παρακαλώ πληκτρολογήστε έναν ακέραιο!')
    return int(a)

def YesOrNo(title,message): #ΠΑΡΑΘΥΡΟ ΔΙΑΛΟΓΟΥ ΜΕ ΝΑΙ ΟΧΙ 

    while True:
        try:
            result = messagebox.askyesno(title, message) 
            if result == True:
                LR=1
            else:
                LR=0
        except WindowsError as win_err:
            messagebox.askretrycancel("Input_error","An error occurred:\n{}".format(win_err))
        if (LR == 0 or LR == 1) == True: break
    return bool(LR)

def createWin(name,title,Width,Height,backcolor,XlowLimit,YlowLimit, XhighLimit,YhighLimit): #ΔΗΜΙΟΥΡΓΙΑ ΠΑΡΑΘΥΡΟΥ
    name=GraphWin(title=title,width=Width,height=Height) 
    name.setCoords(XlowLimit,YlowLimit, XhighLimit,YhighLimit)
    name.setBackground(backcolor)

def linedraw(name,point1,point2,Width,color,win): #ΔΗΜΙΟΥΡΓΊΑ ΓΡΑΜΜΗΣ ΣΤΟ ΠΑΡΑΘΥΡΟ
    name=Line(point1,point2)
    name.setWidth(Width)
    name.setFill(color)
    name.draw(win)

def cirdrw(name,center,radius,Width,outcolor,win): #ΔΗΜΙΟΥΡΓΙΑ ΕΞΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ ΣΤΟ ΠΑΡΆΘΥΡΟ
    name=Circle(center,radius)
    name.setWidth(Width)
    name.setOutline(outcolor)
    name.draw(win)

def cirdrw1(name,center,radius,Width,outcolor,win): #ΔΗΜΙΟΥΡΓΙΑ ΕΣΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ ΣΤΟ ΠΑΡΆΘΥΡΟ
    name=Circle(center,radius)
    name.setWidth(Width)
    name.setFill(outcolor)
    name.setOutline(outcolor)
    name.draw(win)

def text(name,point,size,color,text,win): #ΔΗΜΙΟΥΡΓΙΑ ΚΕΙΜΕΝΟΥ ΣΤΟ ΠΑΡΑΘΥΡΟ
    name=Text(point,text)
    name.setTextColor(color)
    name.setSize(size)
    name.draw(win)

def atan2(X,Y): #ΕΥΡΕΣΗ ΤΗΣ ΓΩΝΙΑΣ ΠΟΥ ΣΧΗΜΑΤΙΖΕΙ ΕΝΑΣ ΡΟΜΠΟΤΙΚΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΟΝ ΑΞΟΝΑ Οx
    if(X>0 and Y>0 ):   
        q=math.atan(Y/X)
    elif(X>0 and Y<0):
        q=math.atan(Y/X) + 2*math.pi
    elif(X<0 and Y>0):
        q=math.atan(Y/X) + math.pi
    elif(X<0 and Y<0):
        q=math.atan(Y/X) + math.pi
    elif(abs(X)==0 and Y>0):
        q=math.pi/2 #90 ΜΟΙΡΕΣ
    elif(abs(X)==0 and Y<0):
        q=3*(math.pi/2) #270 ΜΟΙΡΕΣ
    elif(X>0 and Y==0):
        q=0
    elif(X<0 and Y==0):
        q=math.pi #180 ΜΟΙΡΕΣ
    else:
        print("Κάποιο πρόβλημα στην γωνία")
        q=0  
    return q 

def eyklidia( P1x,P1y,P2x,P2y): #ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΕΥΚΛΕΙΔΙΑΣ ΑΠΟΣΤΑΣΗΣ
    D=math.sqrt( ( P1y-P2y )**2 + ( P1x-P2x )**2 )
    return D

def Move_Check(x1,y1,x0,y0,win): # ΑΝ ΕΙΝΑΙ ΕΦΙΚΤΉ Η ΚΊΝΗΣΗ ΤΟΥ ΒΡΑΧΙΟΝΑ
    linedraw("move_line",Point(x1,y1),Point(x0,y0),2,"pink",win)
    global a
    global b
    if x1==x0: #ΠΕΡΙΠΤΩΣΗ ΟΠΟΥ x0 ΚΑΙ x1 ΕΙΝΑΙ ΣΤΗ ΙΔΙΑ ΕΥΘΕΙΑ (ΣΕΛΙΔΑ 15 PDF)
        if x1>=abs(L_1-L_2): #ΔΕΝ ΔΙΕΡΧΕΤΑΙ ΑΠΟ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ 
            return True
        else:                #ΔΙΕΡΧΕΤΑΙ ΑΠΟ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ
            Sxa=Sxb=x1
            Sya=+math.sqrt( (L_1-L_2)**2 - x1**2 )
            Syb=-math.sqrt( (L_1-L_2)**2 - x1**2 )
        
    else:
        #ΕΞΕΤΑΖΟΥΜΕ ΑΝ Η ΕΥΘΕΙΑ y=αx+b ΜΕΡΟΣ ΤΗΣ ΟΠΟΙΑΣ ΕΙΝΑΙ ΤΟ P0P1 ΕΧΕΙ ΣΗΜΕΙΑ ΤΟΜΗΣ ΜΕ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ
        a=(y1-y0)/(x1-x0) #ΣΗΜΕΙΑ ΕΥΘΕΙΑΣ  y=αx+b, μέρος της οποίας είναι το Ρ0Ρ1
        b=y0-a*x0
        D=4*(a**2)*(b**2)-(4*(a**2)+1)*((b**2)-(L_1-L_2)**2)
        if D<=0 :   #Η ΕΥΘΕΙΑ ΔΕΝ ΤΕΜΝΕΙ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ
            return True 
        elif D>0 :  #Η ΕΥΘΕΙΑ ΙΣΩΣ ΝΑ ΤΕΜΝΕΙ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ (ΣΕΛΙΔΑ 13 PDF)
            #ΤΑ ΔΥΟ ΣΗΜΕΙΑ ΠΟΥ ΤΕΜΝΟΥΝ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ
            Sxa= ( -2*a*b + math.sqrt(D) ) / (2 * ( (a**2) + 1) ) 
            Sxb= ( -2*a*b - math.sqrt(D) ) / (2 * ( (a**2) + 1) ) 

            Sya= a*Sxa + b
            Syb= a*Sxb + b
    #ΥΠΟΛΟΓΙΣΜΟΣ ΑΠΟΣΤΑΣΕΩΝ ΤΟΥ ΕΥΘΥΓΡΑΜΜΟΥ ΤΜΗΜΑΤΟΣ P0P1 ΓΙΑ ΝΑ ΔΙΑΠΙΣΤΩΣΟΥΜΕ ΑΝ ΤΟ ΙΔΙΟ ΤΟ ΤΜΗΜΑ ΤΕΜΝΕΙ ΤΟΝ ΦΑΚΕΛΟ Η Ή ΠΡΟΕΚΤΑΣΗ ΤΟΥ
    D_p1p0=eyklidia(x1,y1,x0,y0)
    D_p1Sa=eyklidia(x1,y1,Sxa,Sya)
    D_p1Sb=eyklidia(x1,y1,Sxb,Syb)
    D_p0Sa=eyklidia(x0,y0,Sxa,Sya)
    D_p0Sb=eyklidia(x0,y0,Sxb,Syb)
    #MIN-MAX 
    Min_Dp1S=min(D_p1Sa,D_p1Sb)
    Min_Dp0S=min(D_p0Sa,D_p0Sb)
    Max_D=max(Min_Dp0S,Min_Dp1S)
    
    if D_p1p0<Max_D:    #Η ΕΥΘΕΙΑ ΔΕΝ ΤΕΜΝΕΙ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ
        return True
    elif D_p1p0>Max_D:  #Η ΕΥΘΕΙΑ ΤΕΜΝΕΙ ΤΟΝ ΕΣΩΤΕΡΙΚΟ ΦΑΚΕΛΟ
        messagebox.showwarning("Warring","Η κινηση δεν ειναι δυνατή,\nεπειδή τέμνει τον εσωτερικό φακελο")
        return False
    else:
        messagebox.showerror("ERROR","ΚΑΤΙ ΠΗΓΕ ΣΤΡΑΒΑ ΣΤΗΝ ΡΟΥΤΙΝΑ \nΕΛΕΝΧΟΥ ΚΙΝΗΣΗΣ")
        return False

def reversesolution(L1,L2,Px,Py,win,off):    
    
    #ΤΟΜΕΑΣ ΕΥΡΕΣΗΣ ΓΩΝΙΩΝ
    
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΤΙΖΕΙ Ο ΔΕΥΤΕΡΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΗΝ ΠΡΟΕΚΤΑΣΗ ΤΟΥ ΠΡΩΤΟΥ (ΑΡΙΣΤΕΡΟΣΤΡΟΦΗ)
    q2a=+math.acos( (Px**2+Py**2-L1**2-L2**2) / (2*L1*L2) )
    Q2a=(q2a*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕΣ
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΤΙΖΕΙ Ο ΔΕΥΤΕΡΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΗΝ ΠΡΟΕΚΤΑΣΗ ΤΟΥ ΠΡΩΤΟΥ (ΔΕΞΙΟΣΤΡΟΦΗ)
    q2b=-math.acos( (Px**2+Py**2-L1**2-L2**2) / (2*L1*L2) )+2*(math.pi)
    Q2b=(q2b*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕ
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΙΖΕΙ Ο ΠΡΩΤΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΟΝ ΟΡΙΖΟΝΤΙΟ ΑΞΟΝΑ (ΑΡΙΣΤΕΡΟΣΤΡΟΦΗ)
    k1a=L1 + L2*math.cos(q2a)
    k2a=L2*math.sin(q2a)
    q1a=math.atan2(Py,Px)-math.atan2(k2a,k1a)
    Q1a=(q1a*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕΣ
    if Q1a<0 :
        Q1a=Q1a+360 
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΤΙΖΕΙ Ο ΠΡΩΤΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΟΝ ΟΡΙΖΟΝΤΙΟ ΑΞΟΝΑ (ΔΕΞΙΟΣΤΡΟΦΗ)
    k1b=L1 + L2*math.cos(q2b)
    k2b=L2*math.sin(q2b)
    q1b=math.atan2(Py,Px)-math.atan2(k2b,k1b)
    Q1b=(q1b*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕΣ 
    if Q1b<0 :
        Q1b=Q1b+360 
    #ΤΕΛΟΣ ΤΟΜΕΑ

    #ΤΟΜΕΑΣ ΕΥΡΕΣΗΣ ΤΩΝ ΜΕΣΑΙΩΝ ΣΗΜΕΙΩΝ (ΤΕΛΟΣ ΤΟΥ ΠΡΩΤΟΥ, ΑΡΧΗ ΤΟΥ ΔΕΥΤΕΡΟΥ)
    X2a=math.cos(q1a)*L1
    Y2a=math.sin(q1a)*L1
    
    X2b=math.cos(q1b)*L1
    Y2b=math.sin(q1b)*L1
    #ΤΕΛΟΣ ΤΟΜΕΑ
    
    #ΤΟΜΕΑΣ ΕΠΙΛΟΓΗΣ ΤΗΣ ΜΙΑΣ ΑΠΟ ΤΙΣ ΔΥΟ ΛΥΣΕΙΣ ΤΟΥ ΑΝΑΣΤΡΟΦΟΥ ΚΙΝΗΜΑΤΙΚΟΥ ΣΕΛΙΔΑ 9 PDF
    if q2a>0 and q2a<math.pi : #ΑΡΙΣΤΕΡΟΧΕΙΡΗ ΑΠΕΙΚΟΝΙΣΗ
        A=False
    elif q2a>math.pi and q2a>2*math.pi: #ΔΕΞΙΟΧΕΙΡΗ ΑΠΕΙΚΟΝΙΣΗ
        A=True
    #ΤΕΛΟΣ ΤΟΜΕΑ
    
    #ΤΟΜΕΑΣ ΣΧΕΔΙΑΣΕΙΣ ΑΠΕΙΚΟΝΙΣΗΣ ΕΞΩΤΕΡΙΚΟΥ ΚΑΙ ΕΣΩΤΕΡΙΚΟΥ ΚΥΚΛΟΥ
    cirdrw1("inCir",Point(0,0),(L1-L2),2,"yellow",win)
    cirdrw("outCir",Point(0,0),(L1+L2),2,"white",win)
    #ΤΕΛΟΣ ΤΟΜΕΑ
    
    #ΤΟΜΕΑΣ ΑΠΕΙΚΟΝΙΣΗΣ ΣΤΟΙΧΕΙΩΝ ΣΤΟ ΠΑΡΑΘΥΡΟ
    if off!=True:
        
        text("L1_length",Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.05)),9,"white",("L1 length:",round(L1,2)),win)  #ΜΗΚΟΣ L1 ΤΟΥ ΒΡΑΧΙΟΝΑ
        text("L2_length",Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.10)),9,"white",("L2 length:",round(L2,2)),win)  #ΜΗΚΟΣ L2 ΤΟΥ ΒΡΑΧΙΟΝΑ
        text('lastpoint',Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.30)),8,'white',('T(',round(Px,1),round(Py,1),')',),win)  #ΑΡΧΙΚΟ ΣΗΜΕΙΟ ΤΟΥ ΒΡΑΧΙΟΝΑ
        if A==rotation:       #ΑΝ ΕΙΝΑΙ Η ΑΡΙΣΤΕΡΟΣΤΡΟΦΗ Η ΣΩΣΤΗ ΛΥΣΗ
            text("Q1a_angle",Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.20)),9,Dir_color,("f1 angle:",round(Q1a,2)),win) #ΠΡΩΤΗ ΓΩΝΙΑ 
            text("Q2a_angle",Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.25)),9,Dir_color,("f2 angle:",round(Q2a,2)),win) #ΔΕΥΤΕΡΗ ΓΩΝΙΑ
            text('lastpoint',Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.35)),8,'yellow',('A(',round(X2a,1),round(Y2a,1),')',),win)  #A point
        else:                 #ΑΝ ΕΙΝΑΙ Η ΔΕΞΙΟΣΤΡΟΦΗ Η ΣΩΣΤΗ ΛΥΣΗ
            text("Q1b_angle",Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.20)),9,Dir_color,("f1 angle:",round(Q1b,2)),win) #ΠΡΩΤΗ ΓΩΝΙΑ 
            text("Q2b_angle",Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.25)),9,Dir_color,("f2 angle:",round(Q2b,2)),win) #ΔΕΥΤΕΡΗ ΓΩΝΙΑ
            text('lastpoint',Point((XlowLimit+XhighLimit*0.15),(YhighLimit-YhighLimit*0.35)),8,'yellow',('B(',round(X2b,1),',',round(Y2b,1),')',),win)  #B' point


        text('lastpoint',Point(Px,Py),8,'yellow',('T(',round(Px,1),round(Py,1),')',),win) #ΤΕΛΙΚΟ ΣΗΜΕΙΟ ΤΟΥ ΒΡΑΧΙΟΝΑ

    #ΤΟΜΕΑΣ ΣΧΕΔΙΑΣΗΣ ΑΞΟΝΩΝ Χ ΚΑΙ Υ
    linedraw("Xaxis",Point(XlowLimit,0),Point(XhighLimit,0),2,"white",win)
    linedraw("Xaxis",Point(0,YlowLimit),Point(0,YhighLimit),2,"white",win)
    peakof_x_axis = Polygon(Point(XhighLimit,0), Point(XhighLimit-XhighLimit*0.03,YhighLimit*0.03), Point(XhighLimit-XhighLimit*0.03,-YhighLimit*0.03))
    peakof_x_axis.setFill('white')
    peakof_x_axis.draw(win)
    peakof_y_axix = Polygon(Point(0,YhighLimit), Point(XhighLimit*0.03,YhighLimit-YhighLimit*0.03), Point(-XhighLimit*0.03,YhighLimit-YhighLimit*0.03))
    peakof_y_axix.setFill('white')
    peakof_y_axix.draw(win)
    #ΤΕΛΟΣ ΤΟΜΕΑ 

    #ΤΟΜΕΑΣ ΣΧΕΔΙΑΣΗΣ ΤΩΝ ΔΥΟ ΛΥΣΕΩΝ
    if A==rotation :                                                    #ΣΧΕΔΙΑΣΗ ΠΡΩΤΗΣ ΛΥΣΗΣ
        linedraw("Line_L2",Point(X2a,Y2a),Point(Px,Py),4,Dir_color,win)
        linedraw("Line_L1",Point(0,0),Point(X2a,Y2a),4,Dir_color,win)
    else:                                                               #ΣΧΕΔΙΑΣΗ ΔΕΥΤΕΡΗΣ ΛΥΣΗΣ
        linedraw("Line_L2b",Point(X2b,Y2b),Point(Px,Py),4,Dir_color,win)
        linedraw("Line_L1b",Point(0,0),Point(X2b,Y2b),4,Dir_color ,win)
    #ΤΕΛΟΣ ΤΟΜΕΑ

def reversesolution1(L1,L2,Px,Py,win,off):    
    
    #ΤΟΜΕΑΣ ΕΥΡΕΣΗΣ ΓΩΝΙΩΝ
    
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΤΙΖΕΙ Ο ΔΕΥΤΕΡΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΗΝ ΠΡΟΕΚΤΑΣΗ ΤΟΥ ΠΡΩΤΟΥ (ΑΡΙΣΤΕΡΟΣΤΡΟΦΗ)
    q2a=+math.acos( (Px**2+Py**2-L1**2-L2**2) / (2*L1*L2) )
    Q2a=(q2a*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕΣ
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΤΙΖΕΙ Ο ΔΕΥΤΕΡΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΗΝ ΠΡΟΕΚΤΑΣΗ ΤΟΥ ΠΡΩΤΟΥ (ΔΕΞΙΟΣΤΡΟΦΗ)
    q2b=-math.acos( (Px**2+Py**2-L1**2-L2**2) / (2*L1*L2) )+2*(math.pi)
    Q2b=(q2b*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕ
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΙΖΕΙ Ο ΠΡΩΤΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΟΝ ΟΡΙΖΟΝΤΙΟ ΑΞΟΝΑ (ΑΡΙΣΤΕΡΟΣΤΡΟΦΗ)
    k1a=L1 + L2*math.cos(q2a)
    k2a=L2*math.sin(q2a)
    q1a=math.atan2(Py,Px)-math.atan2(k2a,k1a)
    Q1a=(q1a*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕΣ
    if Q1a<0 :
        Q1a=Q1a+360 
    #ΓΩΝΙΑ ΠΟΥ ΣΧΗΜΑΤΙΖΕΙ Ο ΠΡΩΤΟΣ ΒΡΑΧΙΟΝΑΣ ΜΕ ΤΟΝ ΟΡΙΖΟΝΤΙΟ ΑΞΟΝΑ (ΔΕΞΙΟΣΤΡΟΦΗ)
    k1b=L1 + L2*math.cos(q2b)
    k2b=L2*math.sin(q2b)
    q1b=math.atan2(Py,Px)-math.atan2(k2b,k1b)
    Q1b=(q1b*180) / math.pi #ΑΠΟ ΑΚΤΙΝΑ ΣΕ ΜΟΙΡΕΣ 
    if Q1b<0 :
        Q1b=Q1b+360 

    #ΤΕΛΟΣ ΤΟΜΕΑ

    #ΤΟΜΕΑΣ ΕΥΡΕΣΗΣ ΤΩΝ ΜΕΣΑΙΩΝ ΣΗΜΕΙΩΝ (ΤΕΛΟΣ ΤΟΥ ΠΡΩΤΟΥ, ΑΡΧΗ ΤΟΥ ΔΕΥΤΕΡΟΥ)
    X2a=math.cos(q1a)*L1
    Y2a=math.sin(q1a)*L1
    
    X2b=math.cos(q1b)*L1
    Y2b=math.sin(q1b)*L1
    #ΤΕΛΟΣ ΤΟΜΕΑ
    
    #ΤΟΜΕΑΣ ΕΠΙΛΟΓΗΣ ΤΗΣ ΜΙΑΣ ΑΠΟ ΤΙΣ ΔΥΟ ΛΥΣΕΙΣ ΤΟΥ ΑΝΑΣΤΡΟΦΟΥ ΚΙΝΗΜΑΤΙΚΟΥ (ΣΕΛΙΔΑ 9 PDF)
    if q2a>0 and q2a<math.pi : #ΑΡΙΣΤΕΡΟΧΕΙΡΗ ΑΠΕΙΚΟΝΙΣΗ
        A=False
    elif q2a>math.pi and q2a>2*math.pi: #ΔΕΞΙΟΧΕΙΡΗ ΑΠΕΙΚΟΝΙΣΗ
        A=True
    #ΤΕΛΟΣ ΤΟΜΕΑ
    
    #ΤΟΜΕΑΣ ΣΧΕΔΙΑΣΕΙΣ ΑΠΕΙΚΟΝΙΣΗΣ ΕΞΩΤΕΡΙΚΟΥ ΚΑΙ ΕΣΩΤΕΡΙΚΟΥ ΚΥΚΛΟΥ
    cirdrw1("inCir",Point(0,0),(L1-L2),2,"yellow",win)
    cirdrw("outCir",Point(0,0),(L1+L2),2,"white",win)
    #ΤΕΛΟΣ ΤΟΜΕΑ
    
    #ΤΟΜΕΑΣ ΑΠΕΙΚΟΝΙΣΗΣ ΣΤΟΙΧΕΙΩΝ ΣΤΟ ΠΑΡΑΘΥΡΟ
    if off!=True:
        
        text("L1_length",Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.05)),9,"white",("L1 length:",round(L1,2)),win)  #ΜΗΚΟΣ L1 ΤΟΥ ΒΡΑΧΙΟΝΑ
        text("L2_length",Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.10)),9,"white",("L2 length:",round(L2,2)),win)  #ΜΗΚΟΣ L2 ΤΟΥ ΒΡΑΧΙΟΝΑ
        text('lastpoint',Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.30)),8,'white',('T(',round(Px,1),round(Py,1),')',),win)  #ΑΡΧΙΚΟ ΣΗΜΕΙΟ ΒΡΑΧΙΟΝΑ
        if A==rotation:    #ΑΝ ΕΙΝΑΙ Η ΑΡΙΣΤΕΡΟΣΤΡΟΦΗ Η ΣΩΣΤΗ ΛΥΣΗ
            text("Q1a_angle",Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.20)),9,Dir_color,("f1 angle:",round(Q1a,2)),win)  #ΠΡΩΤΗ ΓΩΝΙΑ 
            text("Q2a_angle",Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.25)),9,Dir_color,("f2 angle:",round(Q2a,2)),win)  #ΔΕΥΤΕΡΗ ΓΩΝΙΑ 
            text('lastpoint',Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.35)),8,'yellow',('A(',round(X2a,1),round(Y2a,1),')',),win)  #A point
        else:              #ΑΝ ΕΙΝΑΙ Η ΔΕΞΙΟΣΤΡΟΦΗ Η ΣΩΣΤΗ ΛΥΣΗ
            text("Q1b_angle",Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.20)),9,Dir_color,("f1 angle:",round(Q1b,2)),win) #ΠΡΩΤΗ ΓΩΝΙΑ
            text("Q2b_angle",Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.25)),9,Dir_color,("f2 angle:",round(Q2b,2)),win) #ΔΕΥΤΕΡΗ ΓΩΝΙΑ
            text('lastpoint',Point((XlowLimit+XhighLimit*1.85),(YhighLimit-YhighLimit*0.35)),8,'yellow',('B(',round(X2b,1),',',round(Y2b,1),')',),win)  #B' point


        text('lastpoint',Point(Px,Py),8,'yellow',('T(',round(Px,1),round(Py,1),')',),win)  #ΤΕΛΙΚΟ ΣΗΜΕΙΟ ΒΡΑΧΙΟΝΑ 
    #ΤΕΛΟΣ ΤΟΜΕΑ

    #ΤΟΜΕΑΣ ΣΧΕΔΙΑΣΗΣ Χ ΚΑΙ Υ ΑΞΟΝΩΝ
    linedraw("Xaxis",Point(XlowLimit,0),Point(XhighLimit,0),2,"white",win)
    linedraw("Xaxis",Point(0,YlowLimit),Point(0,YhighLimit),2,"white",win)
    peakof_x_axis = Polygon(Point(XhighLimit,0), Point(XhighLimit-XhighLimit*0.03,YhighLimit*0.03), Point(XhighLimit-XhighLimit*0.03,-YhighLimit*0.03))
    peakof_x_axis.setFill('white')
    peakof_x_axis.draw(win)
    peakof_y_axix = Polygon(Point(0,YhighLimit), Point(XhighLimit*0.03,YhighLimit-YhighLimit*0.03), Point(-XhighLimit*0.03,YhighLimit-YhighLimit*0.03))
    peakof_y_axix.setFill('white')
    peakof_y_axix.draw(win)
    #ΤΕΛΟΣ ΤΟΜΕΑ 

    #ΤΟΜΕΑΣ ΣΧΕΔΙΑΣΗΣ ΤΩΝ ΔΥΟ ΛΥΣΕΩΝ
    if A==rotation :                                                    #ΣΧΕΔΙΑΣΗ ΠΡΩΤΗΣ ΛΥΣΗΣ
        linedraw("Line_L2",Point(X2a,Y2a),Point(Px,Py),4,Dir_color,win)
        linedraw("Line_L1",Point(0,0),Point(X2a,Y2a),4,Dir_color,win)
    else:                                                               #ΣΧΕΔΙΑΣΗ ΔΕΥΤΕΡΗΣ ΛΥΣΗΣ
        linedraw("Line_L2b",Point(X2b,Y2b),Point(Px,Py),4,Dir_color,win)
        linedraw("Line_L1b",Point(0,0),Point(X2b,Y2b),4,Dir_color ,win)
    #ΤΕΛΟΣ ΤΟΜΕΑ
  
#ΕΙΣΑΓΩΓΗ ΔΕΔΩΜΕΝΩΝ ΓΙΑ ΕΠΑΝΑΛΗΨΗ ΔΟΚΙΜΗΣ
while True:
    L_1=InputIntegerFromPopUp("L1","Δώσε το μήκος L1 του βραχίονα",0) #'0' ΓΙΑ ΘΕΤΙΚΟΥΣ ΑΡΙΘΜΟΥΣ
    L_2=InputIntegerFromPopUp("L2","Δώσε το μήκος L2 του βραχίονα",0)

    while True:  
        Xt=InputIntegerFromPopUp("Coordinate_X","Δώσε την αρχική συντεταγμένη Χ ",1) #'1' ΓΙΑ ΑΡΝΗΤΙΚΟΥΣ ΑΡΙΘΜΟΥΣ
        Yt=InputIntegerFromPopUp("Coordinate_Y","Δώσε την αρχική συντεταγμένη Υ ",1)
        L=L_1+L_2
        l=abs(L_1-L_2)
        R=math.sqrt(Xt**2+Yt**2)
        if(L>=R and l<=R):   #ΕΛΕΓΧΟΣ ΓΙΑ ΕΓΚΥΡΟΤΗΤΑ ΣΗΜΕΙΟΥ 
            break
        elif(L<R):         
            messagebox.showwarning("Input_error","ΕΔΩΣΕΣ ΤΙΜΗ ΕΚΤΟΣ ΕΞΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ")
        else:
            messagebox.showwarning("Input_error","ΕΔΩΣΕΣ ΤΙΜΗ ΕΝΤΟΣ ΕΣΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ")     
    
    #ΤΟΜΕΑΣ ΕΠΙΛΟΓΗΣ ΔΕΞΙΟΣΤΡΟΦΗΣ Η ΑΡΙΣΤΕΡΟΣΤΡΟΦΗΣ ΛΥΣΗΣ
    rotation=YesOrNo("Διάλεξε Φορά","Επέλεξε ΝΑΙ αν θέλεις δεξιόστροφη επίλυση ή ΟΧΙ αν θες αριστερόστροφη")
    if rotation==True:    #ΔΕΞΙΑ ΛΥΣΗ
        Dir_color="blue"   
    elif rotation==False : #ΑΡΙΣΤΕΡΗ ΛΥΣΗ
        Dir_color="red"    
    #ΤΕΛΟΣ ΤΟΜΕΑ

    #ΤΟΜΕΑΣ ΔΗΜΙΟΥΡΓΙΑΣ ΠΑΡΑΘΥΡΟΥ (ΘΕΛΩ ΝΑ ΕΙΝΑΙ GLOBAL)
    # ΒΡΙΣΚΩ ΤΙΣ ΔΙΑΣΤΑΣΕΙΣ ΤΗΝ ΟΘΟΝΗΣ 
    scrn_width=GetSystemMetrics(0)
    scrn_heiht=GetSystemMetrics(1)
    scrn=min(scrn_width,scrn_heiht) #ΔΙΑΛΕΓΩ ΤΗΝ ΠΙΟ ΜΙΚΡΗ ΔΙΑΣΤΑΣΗ ΕΤΣΙ ΩΣΤΕ ΝΑ ΕΙΜΑΙ ΣΙΓΟΥΡΟΣ ΠΩΣ ΤΟ ΤΕΤΡΑΓΩΝΟ ΠΑΡΑΘΥΡΟ ΘΑ ΧΩΡΑΕΙ ΚΑΛΑ ΣΤΗΝ ΟΘΟΝΗ
                                    
    #ΟΡΙΑ ΑΞΟΝΩΝ
    marge=0.15 #ΑΦΗΝΩ ΠΕΡΙΘΩΡΙΟ ΑΝΑΛΟΓΑ ΜΕ ΤΑ L1,L2
    XlowLimit=-marge*(L_1+L_2) - (L_1+L_2)
    XhighLimit=+marge*(L_1+L_2) + (L_1+L_2)
    YlowLimit=-marge*(L_1+L_2) - (L_1+L_2)
    YhighLimit=+marge*(L_1+L_2) + (L_1+L_2)
    
    
    win=GraphWin(title="Ανάστροφο κινηματικό",width=scrn*0.8,height=scrn*0.8) 
    win.setCoords(XlowLimit,YlowLimit, XhighLimit,YhighLimit)
    win.setBackground("black")
    #ΤΕΛΟΣ ΤΟΜΕΑ

    #ΕΚΤΕΛΕΣΗ ΤΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ ΛΥΣΗΣ ΩΣΤΕ ΝΑ ΔΕΙ Ο ΧΡΗΣΤΗΣ ΤΗΝ ΑΡΧΙΚΗ ΘΕΣΗ
    reversesolution(L_1,L_2,Xt,Yt,win,False)    
   
    #ΑΠΟΘΗΚΕΥΣΗ ΤΩΝ ΣΗΜΕΙΩΝ Xt,Yt 
    lastPoint_x=Xt
    lastPoint_y=Yt

    #ΕΙΣΑΓΩΓΗ ΤΕΛΙΚΟΥ ΣΗΜΕΙΟΥ ΤΗΣ ΚΙΝΗΣΗΣ ΤΟΥ ΒΡΑΧΙΟΝΑ
    while True:
        while True :
            Xt=InputIntegerFromPopUp("Coordinate_X","Δώσε την συντεταγμένη Χ του τελικού σημείου του βραχίονα",1) #'1' ΓΙΑ ΑΡΝΗΤΙΚΟΥΣ ΑΡΙΘΜΟΥΣ 
            Yt=InputIntegerFromPopUp("Coordinate_Y","Δώσε την συντεταγμένη Υ του τελικού σημείου του βραχίονα",1)
            L=L_1+L_2            #ΑΚΤΙΝΑ ΕΞΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ
            l=abs(L_1-L_2)       #ΑΚΤΙΝΑ ΕΣΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ
            R=math.sqrt(Xt**2+Yt**2) #ΑΚΤΙΝΑ ΑΠΟ 0,0 ΣΕ Xt,Yt
            if(L>=R and l<=R):   #ΕΛΕΓΧΟΣ ΓΙΑ ΕΓΚΥΡΟΤΗΤΑ ΣΗΜΕΙΟΥ 
                break
            elif(L<R):         
                messagebox.showwarning("Δεν Ειναι Δυνατη η Κινηση","ΕΔΩΣΕΣ ΤΙΜΗ ΕΚΤΟΣ ΕΞΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ")
            else:
                messagebox.showwarning("Δεν Ειναι Δυνατη η Κινηση","ΕΔΩΣΕΣ ΤΙΜΗ ΕΝΤΟΣ ΕΣΩΤΕΡΙΚΟΥ ΦΑΚΕΛΟΥ")

        checked=Move_Check(Xt,Yt,lastPoint_x,lastPoint_y,win)
        if checked==True:
            break
    
    reversesolution1(L_1,L_2,Xt,Yt,win,False)

    again=YesOrNo("__","Θελεις να επαναλαβεις με νεα δεδομενα ;") #ΕΡΩΤΗΣΗ ΓΙΑ ΝΑ ΞΑΝΑ ΤΡΈΞΕΙ ΤΟ ΠΡΟΓΡΑΜΜΑ ΜΕ ΝΕΑ ΔΕΔΟΜΕΝΑ
    if(again==0):
        break

win.getMouse()