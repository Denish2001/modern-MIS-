from tkinter import*
from PIL import ImageTk,Image
from tkinter import messagebox,ttk
import customtkinter
import mysql.connector
import ttkthemes
from datetime import datetime

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

window=customtkinter.CTk()
window.title("TUK LOG IN PAGE")
window.resizable(FALSE,FALSE)
window.geometry('800x600')

def login():
    if e1.get() == "admin" and e2.get()=="12345":
        window.withdraw()
        top=customtkinter.CTkToplevel()
        top.title("my second window")
        top.geometry("1000x800")
        top.resizable(FALSE,FALSE)
        img=ImageTk.PhotoImage(Image.open("sc2.jpg").resize((1000,800),Image.LANCZOS))
        la=customtkinter.CTkLabel(master=top,image=img)
        la.pack()

        def wexit():
            results=messagebox.askyesno('confirmation','Do you want to exit?')
            if results:
                top.destroy()
            else:
                pass

        def updatestudent():
            uwindow=customtkinter.CTkToplevel()
            uwindow.title("Update student")
            uwindow.grab_set()
            
            def update():
                query= 'Update class set Name=%s,contact=%s,Gender=%s,Date_of_Birth=%s,Status=%s where Admission_number=%s'
                mycursor.execute(query,(entryname.get(),entrycontact.get(),entrygender.get(),entrybirthday.get(),entrystatus.get(),entryadm.get()))
                db.commit()
                messagebox.showinfo('success','update successfull',parent=uwindow)
                uwindow.destroy()
                showall()

            

            entryadm=customtkinter.CTkEntry(master=uwindow,width=300,placeholder_text="Admission Number")
            entryadm.grid(row=0,column=0,pady=20,padx=30)
            entryname=customtkinter.CTkEntry(master=uwindow,width=300,placeholder_text="name")
            entryname.grid(row=1,column=0,pady=20,padx=30)
            entrycontact=customtkinter.CTkEntry(master=uwindow,width=300,placeholder_text="contact")
            entrycontact.grid(row=2,column=0,pady=20,padx=30)
            entrygender=customtkinter.CTkEntry(master=uwindow,width=300,placeholder_text="Gender")
            entrygender.grid(row=3,column=0,pady=20,padx=30)
            entrybirthday=customtkinter.CTkEntry(master=uwindow,width=300,placeholder_text="Date of birth")
            entrybirthday.grid(row=4,column=0,pady=20,padx=30)
            entrystatus=customtkinter.CTkEntry(master=uwindow,width=300,placeholder_text="status")
            entrystatus.grid(row=5,column=0,pady=20,padx=30)

            updatebtn=customtkinter.CTkButton(master=uwindow,text="update",width=300,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=update)
            updatebtn.grid(row=6,columnspan=2,pady=15)

            index=studenttable.focus()
            content=studenttable.item(index)
            listdata=content['values']
            entryadm.insert(0,listdata[0])
            entryname.insert(0,listdata[1])
            entrycontact.insert(0,listdata[2])
            entrygender.insert(0,listdata[3])
            entrybirthday.insert(0,listdata[4])
            entrystatus.insert(0,listdata[5])



        def deletestudent():

            index=studenttable.focus()
            content=studenttable.item(index)
            content_id=content['values'][0]
            q3='delete from class where Admission_number=%s'
            mycursor.execute(q3,(content_id,))
            db.commit()
            messagebox.showinfo('success',f'student id {content_id} has been deleted from database')
            fetched=mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for data in fetched:
                datalist=list(data)
                studenttable.insert('',END,values=datalist)


        def showall():
             q2='SELECT * FROM class'
             mycursor.execute(q2)
             fetched=mycursor.fetchall()
             #statement below is used to prevent duplication of all records when one is added in the tree view
             studenttable.delete(*studenttable.get_children())
             for data in fetched:
                datalist=list(data)
                studenttable.insert('',END,values=datalist)


        def searchstudent():
            
            swindow=customtkinter.CTkToplevel()
            swindow.resizable(False,False)
            swindow.grab_set()

            def searchdata():  
                 q3='select * from class where Admission_number=%s or Name=%s or contact=%s or Gender=%s or status=%s'
                 mycursor.execute(q3,(entryadm.get(),entryname.get(),entrycontact.get(),entrygender.get(),entrystatus.get()))
                 fetched=mycursor.fetchall()
                 studenttable.delete(*studenttable.get_children())
                 for data in fetched:
                   datalist=list(data)
                   studenttable.insert('',END,values=datalist)

            entryadm=customtkinter.CTkEntry(master=swindow,width=300,placeholder_text="Admission Number")
            entryadm.grid(row=0,column=0,pady=20,padx=30)
            entryname=customtkinter.CTkEntry(master=swindow,width=300,placeholder_text="name")
            entryname.grid(row=1,column=0,pady=20,padx=30)
            entrycontact=customtkinter.CTkEntry(master=swindow,width=300,placeholder_text="contact")
            entrycontact.grid(row=2,column=0,pady=20,padx=30)
            entrygender=customtkinter.CTkEntry(master=swindow,width=300,placeholder_text="Gender")
            entrygender.grid(row=3,column=0,pady=20,padx=30)
            entrystatus=customtkinter.CTkEntry(master=swindow,width=300,placeholder_text="status")
            entrystatus.grid(row=4,column=0,pady=20,padx=30)

            searchbtn=customtkinter.CTkButton(master=swindow,text="search student",width=300,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=searchdata)
            searchbtn.grid(row=6,columnspan=2,pady=15)



            

        def add():
            awindow=customtkinter.CTkToplevel()
            awindow.resizable(False,False)
            awindow.grab_set()
            def addstudent():
                if entryadm.get() =='' or entryname.get() == '' or entrygender.get() == '' or entrycontact.get() == '' or entrybirthday.get() == '' or entrystatus.get() == '':
                    messagebox.showwarning('warning','All fields require entry',parent=awindow)
                else:
                    query= 'INSERT INTO class VALUES(%s,%s,%s,%s,%s,%s)'
                    mycursor.execute(query,(entryadm.get(),entryname.get(),entrycontact.get(),entrygender.get(),
                                            entrybirthday.get(),entrystatus.get()))
                    db.commit()
                    results=messagebox.askquestion('Adding student succesfull','Action succesfull. clear the form?',parent=awindow)
                    if results:
                        entryadm.delete(0,END)
                        entryname.delete(0,END)
                        entrycontact.delete(0,END)
                        entrygender.delete(0,END)
                        entrybirthday.delete(0,END)
                        entrystatus.delete(0,END)
                    else:
                        pass
                    q2='SELECT * FROM class'
                    mycursor.execute(q2)
                    fetched=mycursor.fetchall()
                    #statement below is used to prevent duplication of all records when one is added in the tree view
                    studenttable.delete(*studenttable.get_children())
                    for data in fetched:
                        datalist=list(data)
                        studenttable.insert('',END,values=datalist)
            entryadm=customtkinter.CTkEntry(master=awindow,width=300,placeholder_text="Admission Number")
            entryadm.grid(row=0,column=0,pady=20,padx=30)
            entryname=customtkinter.CTkEntry(master=awindow,width=300,placeholder_text="name")
            entryname.grid(row=1,column=0,pady=20,padx=30)
            entrycontact=customtkinter.CTkEntry(master=awindow,width=300,placeholder_text="contact")
            entrycontact.grid(row=2,column=0,pady=20,padx=30)
            entrygender=customtkinter.CTkEntry(master=awindow,width=300,placeholder_text="Gender")
            entrygender.grid(row=3,column=0,pady=20,padx=30)
            entrybirthday=customtkinter.CTkEntry(master=awindow,width=300,placeholder_text="Date of birth")
            entrybirthday.grid(row=4,column=0,pady=20,padx=30)
            entrystatus=customtkinter.CTkEntry(master=awindow,width=300,placeholder_text="status")
            entrystatus.grid(row=5,column=0,pady=20,padx=30)

            addbtn=customtkinter.CTkButton(master=awindow,text="Add student",width=300,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=addstudent)
            addbtn.grid(row=6,columnspan=2,pady=15)

           
            

        def db_connect():
            dbconnection=customtkinter.CTkToplevel()
            dbconnection.grab_set()
            dbconnection.title("Database details")
            dbconnection.geometry("470x260+730+230")
            dbconnection.resizable(0,0)
            

            def connect():
                global mycursor
                global db
                try:
                  db=mysql.connector.connect(host=entryhost.get(),
                                             user=entryusername.get(),
                                             passwd=entrypasswd.get(),
                                             database="studentsabmi2020")
                  mycursor=db.cursor()
                  messagebox.showinfo('Database','You are connected to the database',parent=dbconnection)
                except:
                   messagebox.showerror('error','wrong entries',parent=dbconnection)

                ba.configure(state="normal")
                bb.configure(state="normal")
                bc.configure(state="normal")
                bd.configure(state="normal")
                be.configure(state="normal")

                dbconnection.destroy()


           
            entryhost=customtkinter.CTkEntry(master=dbconnection,width=300,placeholder_text="Enter host name")
            entryhost.grid(row=0,column=0,pady=20,padx=30)
            entryusername=customtkinter.CTkEntry(master=dbconnection,width=300,placeholder_text="Enter username")
            entryusername.grid(row=1,column=0,pady=20,padx=30)
            entrypasswd=customtkinter.CTkEntry(master=dbconnection,width=300,placeholder_text="Enter Password")
            entrypasswd.grid(row=2,column=0,pady=20,padx=30)
            connectbtn=customtkinter.CTkButton(master=dbconnection,text="connect",width=500,corner_radius=5,font=('Century Gothic',18,'bold'),height=30,command=connect)
            connectbtn.grid(row=3,columnspan=2)


        framea=customtkinter.CTkFrame(master=la,width=700,height=50,corner_radius=15)
        framea.place(x=50,y=20)
        frameb=customtkinter.CTkFrame(master=la,width=300,height=500,corner_radius=15)
        frameb.place(x=30,y=100)
        framec=Frame(la)
        framec.place(x=350,y=100,width=600,height=500)
        l2=customtkinter.CTkLabel(master=framea,text="Welcome to TUK management system",font=('Century Gothic',20,'bold'))
        l2.place(x=10,y=10)

        imga=customtkinter.CTkImage(Image.open("download.jpg").resize((40,40),Image.LANCZOS))
        b2=customtkinter.CTkButton(master=frameb,image=imga,text="connect to database",width=250,corner_radius=6,height=50,compound="left",text_color='black',fg_color='white',command=db_connect)
        b2.place(x=20,y=50)
        ba=customtkinter.CTkButton(master=frameb,text="search student",width=250,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=searchstudent)
        ba.place(x=20,y=150)
        bb=customtkinter.CTkButton(master=frameb,text="add student",width=250,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=add)
        bb.place(x=20,y=200)
        bc=customtkinter.CTkButton(master=frameb,text="delete student",width=250,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=deletestudent)
        bc.place(x=20,y=250)
        bd=customtkinter.CTkButton(master=frameb,text="update student",width=250,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=updatestudent)
        bd.place(x=20,y=300)
        be=customtkinter.CTkButton(master=frameb,text="Display all",width=250,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=showall)
        be.place(x=20,y=350)
        img9=customtkinter.CTkImage(Image.open("exit.png").resize((70,40),Image.LANCZOS))
        bf=customtkinter.CTkButton(master=frameb,image=img9,text="Exit",width=250,corner_radius=6,font=('Century Gothic',15,'bold'),height=50,compound="left",text_color='black',fg_color='white',command=wexit)
        bf.place(x=20,y=400)

        
        scrollbarx=Scrollbar(framec,orient=HORIZONTAL)
        scrollbary=Scrollbar(framec,orient=VERTICAL)

        scrollbarx.pack(side=BOTTOM,fill=X)
        scrollbary.pack(side=RIGHT,fill=Y)
        
        studenttable=ttk.Treeview(framec,columns=('Admission','Name','Contact','Gender','Birthday','Status'),
                                  xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set)
        scrollbarx.config(command=studenttable.xview)
        scrollbary.config(command=studenttable.yview)

        studenttable.heading('Admission',text='Admission')
        studenttable.heading('Name',text='Name')
        studenttable.heading('Contact',text='Contact')
        studenttable.heading('Gender',text='Gender')
        studenttable.heading('Birthday',text='Birthdate')
        studenttable.heading('Status',text='Status')

        studenttable.column('Admission',width=90,anchor=CENTER)
        studenttable.column('Name',width=110,anchor=CENTER)
        studenttable.column('Contact',width=110,anchor=CENTER)
        studenttable.column('Gender',width=100,anchor=CENTER)
        studenttable.column('Birthday',width=110,anchor=CENTER)
        studenttable.column('Status',width=110,anchor=CENTER)

        style=ttk.Style()
        style.configure('Treeview',rowheight=30,font=('lucida sans',10,'bold'),foreground="#BE8418",background="#C3DA8C")
        style.configure('Treeview.Heading',font=('lucida sans',12,'bold'),foreground="#BE8418")
    

        studenttable.configure(show='headings')

        studenttable.pack(fill=BOTH,expand=1)
        
       
         

    else:
        messagebox.showerror('Error','Wrong credentials')

img=ImageTk.PhotoImage(Image.open("school0.jpg").resize((800,600),Image.LANCZOS))
l1=customtkinter.CTkLabel(master=window,image=img)
l1.pack()
frame1=customtkinter.CTkFrame(master=l1,width=400,height=500,corner_radius=15)
frame1.place(relx=0.5,rely=0.5, anchor=customtkinter.CENTER)
l2=customtkinter.CTkLabel(master=frame1,text="log into your account",font=('Century Gothic',20),anchor=CENTER)
l2.place(x=50,y=100)
l2=customtkinter.CTkLabel(master=frame1,text="TUK management system",font=('Century Gothic',20))
l2.place(x=50,y=45)
e1=customtkinter.CTkEntry(master=frame1,width=300,placeholder_text="username")
e1.place(x=50,y=200)
e2=customtkinter.CTkEntry(master=frame1,width=300,placeholder_text="password")
e2.place(x=50,y=250)
e2.configure(show="*")
b1=customtkinter.CTkButton(master=frame1,text="log in",width=300,corner_radius=5,font=('Century Gothic',15,'bold'),height=20,command=login)
b1.place(x=50,y=300)
img=customtkinter.CTkImage(Image.open("instagram logo.png").resize((20,20),Image.LANCZOS))
img1=customtkinter.CTkImage(Image.open("facebook.png").resize((20,20),Image.LANCZOS))
b2=customtkinter.CTkButton(master=frame1,image=img,text="Instagram",width=140,corner_radius=6,height=20,compound="left",text_color='black',fg_color='white')
b2.place(x=50,y=380)
b3=customtkinter.CTkButton(master=frame1,image=img1,text="Facebook",width=140,corner_radius=6,height=20,compound="left",text_color='black',fg_color='white')
b3.place(x=200,y=380)






window.mainloop()
