from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql
import secrets
import webbrowser
import hashlib


def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


def open_terms_and_conditions():
    webbrowser.open_new("https://ng-password-manager-terms-and-conditions.netlify.app")


def connect_database():
    if (
        emailEntry.get() == '' or emailEntry.get() == 'Email'
        or usernameEntry.get() == '' or usernameEntry.get() == 'Username'
        or passwordEntry.get() == '' or passwordEntry.get() == 'Password'
        or confirmPasswordEntry.get() == '' or confirmPasswordEntry.get() == 'Confirm Password'
    ):
        messagebox.showerror('Error', 'All fields are required')

    elif passwordEntry.get() != confirmPasswordEntry.get():
        messagebox.showerror('Error', 'Password and Confirm Password are not matching')

    elif checktermsandconditions.get()==0 :
        messagebox.showerror('Error', 'Please accept terms & conditions ')
    
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='root')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return
        try:
            query='create database userdata'
            mycursor.execute(query)

            query='use userdata'
            mycursor.execute(query)

            query='create table masterdata(id int auto_increment primary key not null, email varchar(50), username varchar(30), password varchar(140),encryption_key varchar(32))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')
            


        query='select * from masterdata where username=%s'
        mycursor.execute(query, (usernameEntry.get()))
        row=mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Username Already Exists')
        else:

            # Hash the password before storing it in the database
            hashed_password = hash_password(passwordEntry.get())

            # Generate a random encryption key
            encryption_key = secrets.token_hex(16)


            query='insert into masterdata(email, username, password, encryption_key) values (%s, %s, %s,%s)'
            values = (emailEntry.get(), usernameEntry.get(), hashed_password, encryption_key)
            mycursor.execute(query, values)
            con.commit()
            con.close()

            emailEntry.delete(0, END)
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
            confirmPasswordEntry.delete(0, END)
            confirmPasswordEntry.delete(0, END)
            messagebox.showinfo('Success', 'Registration is sucessful')
            checktermsandconditions.set(0)
            signup_window.destroy()
            import signin






def email_enter(event):
    if emailEntry.get() == 'Email':
        emailEntry.delete(0, END)

def email_leave(event):
    if not emailEntry.get():
        emailEntry.insert(0, 'Email')

def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def user_leave(event):
    if not usernameEntry.get():
        usernameEntry.insert(0, 'Username')

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)
        passwordEntry.config(show='●')
        eyeButton.config(image=closeeye)  # Change eye button image to close eye

def password_leave(event):
    if not passwordEntry.get():
        passwordEntry.config(show='')
        passwordEntry.insert(0, 'Password')
        eyeButton.config(image=openeye)  # Change eye button image to open eye
    
    elif not password_visible:
        passwordEntry.config(show='●')
        eyeButton.config(image=closeeye)
def toggle_password_visibility():
    global password_visible
    if password_visible:
        passwordEntry.config(show='●')
        eyeButton.config(image=closeeye)
        password_leave(None)
    else:
        passwordEntry.config(show='')
        eyeButton.config(image=openeye)
    password_visible = not password_visible

# Variable to track password visibility
password_visible = False



def confirmPassword_enter(event):
    if confirmPasswordEntry.get() == 'Confirm Password':
        confirmPasswordEntry.delete(0, END)
        confirmPasswordEntry.config(show='●')
        # eyeButton.config(image=closeeye)  # Change eye button image to close eye

def confirmPassword_leave(event):
    if not confirmPasswordEntry.get():
        confirmPasswordEntry.config(show='')
        confirmPasswordEntry.insert(0, 'Confirm Password')
        # eyeButton.config(image=openeye)  # Change eye button image to open eye
    else:
        confirmPasswordEntry.config(show='●')


def login_page():
    signup_window.destroy()
    import signin


def handle_enter(event):
    connect_database()

#gui part
signup_window = Tk()
signup_window.geometry('990x660+280+90')
signup_window.resizable(0, 0)
signup_window.title('Signup Page')

# Set the absolute path to the icon file
icon_path = "key.png"

# Try to open the icon using PIL
try:
    icon = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon)
    signup_window.iconphoto(True, icon_photo)
except Exception as e:
    print("Error loading and setting window icon:", e)

bgImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(signup_window, image=bgImage)
bgLabel.image = bgImage
bgLabel.place(x=0, y=0)

heading = Label(signup_window, text='CREATE AN ACCOUNT', font=('Poppins', 18, 'bold'), bg='white', fg='firebrick1')
heading.place(x=565, y=110)

emailEntry = Entry(signup_window, width=25, font=('Poppins', 11), bd=0, fg='black')
emailEntry.place(x=580, y=180)
emailEntry.insert(0, 'Email')
emailEntry.bind('<FocusIn>', email_enter)
emailEntry.bind('<FocusOut>', email_leave)

emailEntry.bind('<Return>', handle_enter)

frame1 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame1.place(x=580, y=202)

usernameEntry = Entry(signup_window, width=25, font=('Poppins', 11), bd=0, fg='black')
usernameEntry.place(x=580, y=240)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)
usernameEntry.bind('<FocusOut>', user_leave)
usernameEntry.bind('<Return>', handle_enter)

frame2 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame2.place(x=580, y=262)

passwordEntry = Entry(signup_window, width=25, font=('Poppins', 11), bd=0, fg='black')
passwordEntry.place(x=580, y=300)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)
passwordEntry.bind('<FocusOut>', password_leave)
passwordEntry.bind('<Return>', handle_enter)

frame3 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame3.place(x=580, y=322)

closeeye = PhotoImage(file='closeye.png')
openeye = PhotoImage(file='openeye.png')
eyeButton = Button(signup_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=toggle_password_visibility)
eyeButton.place(x=800, y=293)


confirmPasswordEntry = Entry(signup_window, width=25, font=('Poppins', 11), bd=0, fg='black')
confirmPasswordEntry.place(x=580, y=360)
confirmPasswordEntry.insert(0, 'Confirm Password')
confirmPasswordEntry.bind('<FocusIn>', confirmPassword_enter)
confirmPasswordEntry.bind('<FocusOut>', confirmPassword_leave)
confirmPasswordEntry.bind('<Return>', handle_enter)

frame4 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame4.place(x=580, y=382)


checktermsandconditions=IntVar()

termsandconditions=Checkbutton(signup_window, text='I agree to the Terms & Conditions', font=('poppins', 9, 'bold' ), fg='firebrick1', bg='white', activebackground='white', activeforeground='firebrick1', cursor='hand2', variable=checktermsandconditions)
termsandconditions.place(x=565, y=408)

termsandconditionswebButton = Button(signup_window, text='*', bd=0, bg='white', activebackground='white', cursor='hand2', font=('poppins', 14, 'bold'), fg='SystemHighlight', activeforeground='SystemHighlight',command=open_terms_and_conditions)
termsandconditionswebButton.place(x=777, y=398)

signupButton = Button(signup_window, text='Signup', font=('poppins', 16, 'bold'), fg='white', bg='firebrick1',activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=19,command=connect_database)
signupButton.place(x=578, y=450)


alreadyaccount = Label(signup_window, text='Already have an account?', font=('Poppins', 9, 'bold'), bg='white', fg='firebrick1')
alreadyaccount.place(x=575, y=500)

loginButton = Button(signup_window, text='Log in', bd=0, bg='white', activebackground='white', cursor='hand2', font=('poppins', 9, 'bold underline'), fg='SystemHighlight', activeforeground='SystemHighlight',command=login_page)
loginButton.place(x=770, y=500)




signup_window.mainloop()
