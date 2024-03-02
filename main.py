#modules
from tkinter import *
import mysql.connector
from PIL import ImageTk,Image
from tkinter import messagebox


# connection
mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                passwd="Root@123",
                                database="cinema")
mycursor = mydb.cursor()

# pages

#registration page

def register():
    global root1
    global img1,resized,img,Label2
    root1 = Tk()
    root1.title("Register")
    root1.geometry("900x600+320+50")
    img = Image.open("images/mov_bg.jpg")
    resized = img.resize((900,600),Image.LANCZOS)
    img1 = ImageTk.PhotoImage(resized)
    Label2 = Label(root1,image=img1).pack()
    frame2 = Frame(Label2,width=400,height=400,bg="white")
    frame2.place(x=100,y=100)
    heading1 =Label(frame2,text="Sign up",bg = "white",font=('RoundKindDemo',25,"bold"))
    heading1.place(x=130,y=5)
    def goBack1():
        root1.destroy()
        login()
    button2=Button(frame2,text="BACK",height=1,width=8,bg="black",fg="white",font=("RoundKindDemo",8,"bold"),command=goBack1)
    button2.place(x=163,y=50)
    Luser= Label(frame2,text="Create Username",bg="white",fg="black",font=("Microsoft Yahei UI light",10,"bold"))
    Luser.place(x=135,y=80)
    user=Entry(frame2,width=25,fg="#B2B2B2",border=0,bg="black",font=("Arial",11))
    user.place(x=97,y=105)
    Lemail= Label(frame2,text="Email Address",bg="white",fg="black",font=("Microsoft Yahei UI light",10,"bold"))
    Lemail.place(x=145,y=155)
    email=Entry(frame2,width=25, fg="#B2B2B2",border=0,bg="black",font=("Arial",11))
    email.place(x=97,y=180)
    Lp_wd= Label(frame2,text="Set Password",bg="white",fg="black",font=("Microsoft Yahei UI light",10,"bold"))
    Lp_wd.place(x=150,y=220)
    p_wd=Entry(frame2,width=25,fg="#B2B2B2",border=0,bg="black",font=("Arial",11))
    p_wd.place(x=97,y=245)
    
    #registration logic

    def callupdate():
        name = user.get()
        password = p_wd.get()
        emailid = email.get()
        mycursor.execute('''select case when exists(select email from customer where email=%s) 
                            then 0 else 1 end as val''',(emailid,))
        sql_query = mycursor.fetchall()
        sql_query = sql_query[0][0]
        print(sql_query)
        if(sql_query==0):
            messagebox.showinfo("Error", "Email already in use,\nplease use another")
        else:
            mycursor.execute("insert into customer(name,email,password) values(%s,%s,%s)", (name, emailid, password))
            mydb.commit()
            mycursor.execute('''select max(ID) from customer''')
            custId = mycursor.fetchall()
            custId = custId[0][0]
            root1.destroy()
            login()
        
    button1=Button(frame2,text="REGISTER",width=30,bg="black",fg="white",font=("RoundKindDemo",15,"bold"),command=callupdate)
    button1.place(x=-20,y=320)

    root1.mainloop()

#login page

def login():
    root = Tk()
    root.title("Login") 
    root.geometry("900x600+320+50")
    def goBack():
        root.destroy()
        register()
    img = Image.open("images/mov_bg.jpg")
    resized = img.resize((900,600),Image.LANCZOS)
    img1 = ImageTk.PhotoImage(resized)
    Label1 = Label(root,image=img1).pack()
    frame = Frame(Label1,width=350,height=400,bg="black")
    frame.place(x=100,y=100)
    heading =Label(frame,text="Sign in",fg="white",bg = "black",font=('RoundKindDemo',25,"bold"))
    heading.place(x=100,y=5)
    button1=Button(frame,text="REGISTER NOW",width=25,font=("RoundKindDemo",15,"bold"),command=goBack)
    button1.place(x=-10,y=300)
    user=Entry(frame,width=25,fg="#B2B2B2",border=0,bg="black",font=("Arial",11))
    user.place(x=137,y=80)
    user.insert(0,"Email Id")
    Frame(frame,width=290,height=2,bg="white").place(x=25,y=100)
    p_wd=Entry(frame,width=25,fg="#B2B2B2",border=0,bg="black",font=("Arial",11),show="*")
    p_wd.place(x=137,y=150)
    p_wd.insert(0,"Password")
    Frame(frame,width=290,height=2,bg="white").place(x=25,y=170)

    #login logic

    def callchk():
        email = user.get()
        password = p_wd.get()
        mycursor.execute('''select case when (%s in (select distinct email from customer) and 
                                    %s in (select distinct password from customer)) then 1 else 0 end as val''',
                                    (email,password))
        sql_qry = mycursor.fetchone()
        if (sql_qry[0] == 0):
            messagebox.showinfo("Error", "Invalid Credentials! \n Please Try Again...")
        else:
            root.destroy()
            mycursor.execute('''select ID from customer where email=%s and password=%s''',(email,password))
            custId = mycursor.fetchall()
            custId = custId[0][0]
            movies(custId)
    
    button2=Button(frame,text="LOGIN",command=callchk,width=25,font=("RoundKindDemo",15,"bold"))
    button2.place(x=-10,y=240)

    root.mainloop()

#theatre page

def callTheatrePage(movie_id,custId):
    thtpg = Tk()
    thtpg.title("theatre booking")
    thtpg.geometry("900x600+320+50")

    nav = Frame(width=900, height=25, bg='grey').pack()
    def logout():
        thtpg.destroy()
        login()

    def home():
        thtpg.destroy()
        movies(custId)

    def goBack():
        thtpg.destroy()
        movies(custId)

    
    Home = Button(nav, text="Home",command=home).place(x=0, y=0)
    Back= Button(text="Back",command=goBack).place(x=45,y=0)
    Logout = Button(nav, text="Logout",command=logout).place(x=852, y=0)

    mycursor.execute('select name from customer')
    name = mycursor.fetchall()
    n=int(custId)
    name=name[n-1][0]
    disp = Label(nav, text="Hello "+name, bg='grey', fg='white').place(x=720, y=0)

    img = Image.open(f"images/{movie_id}.jpg")
    resized = img.resize((900,600),Image.LANCZOS)
    img1 = ImageTk.PhotoImage(resized)
    Label2 = Label(thtpg,image=img1).pack()

    query = '''select s.ID,t.name,start_time,show_date,hall_ID
                from shows s,theatre t
                where s.movie_ID=%s and s.theatre_ID=t.ID
                order by show_date,start_time'''
    mycursor.execute(query,(movie_id,))
    shows = mycursor.fetchall()
    mycursor.execute('select name from movie where ID=%s',(movie_id,))
    movie_name = mycursor.fetchall()
    movie_name = movie_name[0][0]
    r = IntVar()
    chk=0
    l = Label(Label2,text=movie_name,font="200",bg="yellow").place(x=400,y=50)
    def clicked(show_ID):
        if(show_ID==0):
            messagebox.showinfo("Error", "Please select a show")
        else:
            thtpg.destroy()
            seats(show_ID,custId)
    f = Frame(Label2).place(x=100,y=100)
    t=50
    m=100
    for sh in shows:
        m+=50
        rb = Radiobutton(f,font="50",variable=r,value=sh[0],bg="yellow").place(x=t,y=m)
        Label(f,text=str(sh[1])+"\t",font="50",bg="yellow").place(x=t+50,y=m)
        Label(f, text=str(sh[2])+"\t\t",font="50",bg="yellow").place(x=t+200,y=m)
        Label(f, text=str(sh[3])+"\t",font="50",bg="yellow").place(x=t+400,y=m)
        Label(f, text="hall:"+str(sh[4]),font="50",bg="yellow").place(x=t+600,y=m)
        

    b = Button(text="Proceed",font="50",command=lambda:clicked(r.get()),bg="blue",fg="white").place(x=400,y=500)
    thtpg.mainloop()


#movie page/ dashboard

def movies(custID):
    movie = Tk()
    movie.title("movie booking")
    movie.geometry("900x600+320+50")

    nav = Frame(width=900, height=40, bg='#6967ce').pack()
    def goBack():
        movie.destroy()
        login()

    n=int(custID)
    
    Home = Button(nav, text="Home", bg='#f4b400' ,padx=20,pady=10).place(x=0, y=0)
    Logout = Button(nav, text="Logout",command=goBack, bg='#f4b400',padx=20,pady=10).place(x=813, y=0)

    mycursor.execute('select name from customer')
    name = mycursor.fetchall()
    name=name[n-1][0]
    disp = Label(nav, text="Hello "+name, bg='#6967ce', fg='white',padx=20,pady=10).place(x=620, y=0)

    img = Image.open("images/home_bg.jpg")
    resized = img.resize((900,600),Image.LANCZOS)
    img1 = ImageTk.PhotoImage(resized)
    Label2 = Label(movie,image=img1).pack()

    mycursor.execute('select ID,name from movie')
    lst = mycursor.fetchall()
    lable = Label(Label2, text="SELECT MOVIE",fg = "white",bg = "#6967ce",padx=20,pady=10).place(x=360, y=0)
    def clicked(id):
        if(id==0):
            messagebox.showinfo("Error","Please select a movie")
        else:
            movie.destroy()
            callTheatrePage(id,custID)
    chk=0
    r = IntVar()
    t=100
    
    for k in lst:
        t+=50
        rb = Radiobutton(Label2,text = k[1], font="50",variable = r, value = k[0],bg="yellow").place(x=375,y=t)
    btn = Button(Label2,text="select",command= lambda: clicked(r.get()),padx=200,bg="#f4b400").place(x=240,y=450)
    movie.mainloop()


#seat selection page

def seats(show_ID,custId):
    mycursor.execute('''select hall_ID,theatre_ID from shows where ID=%s''',(show_ID,))
    info = mycursor.fetchall()
    h_ID = info[0][0]
    t_ID = info[0][1]
    mycursor.execute('''select capacity from hall where ID=%s and theatre_ID=%s''',(info[0][0],info[0][1]))
    info = mycursor.fetchall()
    info = info[0][0]
    seatPage = Tk()
    seatPage.title("seat booking")
    seatPage.geometry("900x600+320+50")

    nav = Frame(width=900, height=25, bg='grey').pack()
    def logout():
        seatPage.destroy()
        login()

    def home():
        seatPage.destroy()
        movies(custId)

    def goBack():
        seatPage.destroy()
        mycursor.execute('''select movie_ID from shows where ID=%s''',(show_ID,))
        movie_ID = mycursor.fetchall()
        movie_ID = movie_ID[0][0]
        callTheatrePage(movie_ID,custId)

    n=int(custId)
    Home = Button(nav, text="Home",command=home).place(x=0, y=0)
    Back= Button(text="Back",command=goBack).place(x=45,y=0)
    Logout = Button(nav, text="Logout",command=logout).place(x=852, y=0)

    mycursor.execute('select name from customer')
    name = mycursor.fetchall()
    name=name[n-1][0]
    disp = Label(nav, text="Hello "+name, bg='grey', fg='white').place(x=720, y=0)

    img = Image.open("images/home_bg.jpg")
    resized = img.resize((900,600),Image.LANCZOS)
    img1 = ImageTk.PhotoImage(resized)
    Label2 = Label(seatPage,image=img1).pack()

    Label(text="Select a seat",padx=200,bg="blue",fg="white").place(x=220,y=30)
    Label(text="Green-Avalaible",bg="blue",fg="white").place(x=300,y=70)
    Label(text="Yellow-Occupied",bg="blue",fg="white").place(x=500,y=70)
    f = Frame(Label2,bg="yellow")
    f.place(x=270,y=160)
    status = []
    chkbtn = []
    mycursor.execute('''select seat_ID from books where show_ID=%s''',(show_ID,))
    data = mycursor.fetchall()
    booked = []
    for i in data:
        booked.append(i[0])
    mycursor.execute('''SELECT seat_ID from seatinline where show_ID=%s and book_date=curdate() 
                        and (cast(curtime() as time)-cast(book_time as time))<=1000''',(show_ID,))
    data = mycursor.fetchall()
    for i in data:
        booked.append(i[0])
    for i in range(0,info):
        var = IntVar()
        chk = Checkbutton(f,variable=var,onvalue=1,offvalue=0,selectcolor="green",fg="white",bg="yellow")
        chkbtn.append(chk)
        status.append(var)
    for i in booked:
        chkbtn[i-1] = Checkbutton(f,state="disabled",padx=5,pady=5,selectcolor="red",bg="yellow")
    print(i)
    R = 0
    C = 0
    for i in range(0,info):
        chkbtn[i].grid(row=R,column=C)
        C = C+1
        if(C>=10):
            C = 0
            R = R+1
    def clicked():
        newBooked = []
        chk = 0
        for i in range(0,len(status)):
            if(status[i].get()==1):
                chk=1
                newBooked.append(i+1)
        if(chk==0):
            messagebox.showinfo("Error", "Please select a seat")
        else:
            seatPage.destroy()
            callPaymentPage(show_ID,newBooked,custId)
        
    Label(text="Screen",bg="yellow",padx=150,pady=5).place(x=280,y=120)
    Button(text="Proceed",padx=200,command=clicked,bg="blue",fg="white").place(x=225,y=500)
    
    seatPage.mainloop()


#payment page

def callPaymentPage(show_ID,newBooked,custId):
    for i in newBooked:
        mycursor.execute('''insert into seatinline(seat_ID,show_ID,book_time,book_date) values
                            (%s,%s,curtime(),curdate())''',(i,show_ID))
    mydb.commit()
    payPage = Tk()
    payPage.title("Payment")
    payPage.geometry("900x600+320+50")

    nav = Frame(width=900, height=25, bg='grey').pack()
    def logout():
        payPage.destroy()
        login()

    def home():
        payPage.destroy()
        movies(custId)

    def goBack():
        payPage.destroy()
        seats(show_ID,custId)

    n=int(custId)
    Home = Button(nav, text="Home",command=home).place(x=0, y=0)
    Back= Button(text="Back",command=goBack).place(x=45,y=0)
    Logout = Button(nav, text="Logout",command=logout).place(x=852, y=0)

    mycursor.execute('select name from customer')
    name = mycursor.fetchall()
    name=name[n-1][0]
    disp = Label(nav, text="Hello "+name, bg='grey', fg='white').place(x=720, y=0)

    img = Image.open("images/home_bg.jpg")
    resized = img.resize((900,600),Image.LANCZOS)
    img1 = ImageTk.PhotoImage(resized)
    Label2 = Label(payPage,image=img1).pack()

    mycursor.execute('''select* from shows where ID=%s''',(show_ID,))
    show_info = mycursor.fetchall()
    mycursor.execute('''select name from movie where ID=%s''', (show_info[0][1],))
    movie_name = mycursor.fetchall()
    movie_name = movie_name[0][0]
    mycursor.execute('''select name from theatre where ID=%s''', (show_info[0][3],))
    theatre_name = mycursor.fetchall()
    theatre_name = theatre_name[0][0]
    
    
    Label(text="Payment",padx=200,bg="blue",fg="white").place(x=200,y=50)
    f = Frame(Label2,bg="yellow")
    f.place(x=320,y=180)
    fl_amt = int(show_info[0][7])*len(newBooked)
    print(fl_amt)
    amt = str(fl_amt)
    print(amt)
    def clicked():
        payPage.destroy()
        
        mycursor.execute('''insert into payment(amt,pay_time,pay_date)
                            values(%s,curtime(),curdate())''',(fl_amt,))
        mydb.commit()
        mycursor.execute('''select max(ID) from payment''')
        pay_ID = mycursor.fetchall()
        pay_ID = pay_ID[0][0]
        for i in newBooked:
            mycursor.execute('''insert into books
                                values(%s,%s,%s,%s)''',(custId,i,show_ID,pay_ID))
        mydb.commit()
        movies(custId)
        for i in newBooked:
            mycursor.execute('''delete from seatinline where seat_ID=%s and show_ID=%s''',(i,show_ID))
        mydb.commit()
        
    Label(f,text="Movie:",font="50",bg="yellow").grid(row=1)
    Label(f,text="Hall:",font="50",bg="yellow").grid(row=2)
    Label(f,text="Theatre:",font="50",bg="yellow").grid(row=3)
    Label(f,text="Start Time:", font="50",bg="yellow").grid(row=4)
    Label(f,text="End Time:", font="50",bg="yellow").grid(row=5)
    Label(f,text="Date:", font="50",bg="yellow").grid(row=6)
    Label(f,text="Price:", font="50",bg="yellow").grid(row=7)
    Label(f,text="Seat numbers:",font="50",bg="yellow").grid(row=8)
    Label(f,text=movie_name, font="50",bg="yellow").grid(row=1,column=1)
    Label(f,text=show_info[0][2], font="50",bg="yellow").grid(row=2,column=1)
    Label(f,text=theatre_name, font="50",bg="yellow").grid(row=3,column=1)
    Label(f,text=show_info[0][4], font="50",bg="yellow").grid(row=4,column=1)
    Label(f,text=show_info[0][5], font="50",bg="yellow").grid(row=5,column=1)
    Label(f,text=show_info[0][6], font="50",bg="yellow").grid(row=6,column=1)
    Label(f,text=amt, font="50",bg="yellow").grid(row=7,column=1)
    desc = ""
    for i in newBooked:
        desc += "  "+str(i)
    Label(f, text=desc, font="50",bg="yellow").grid(row=8, column=1)
    b = Button(payPage,command = clicked,text="Pay",padx=200,bg="blue",fg="white")
    b.place(x=220, y=500)
    payPage.mainloop()

login()