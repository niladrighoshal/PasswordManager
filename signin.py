from tkinter import *
from PIL import Image, ImageTk
import webbrowser
from tkinter import messagebox
import pymysql
import hashlib


def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


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


def open_facebook_profile():
    webbrowser.open_new("https://www.facebook.com/niladrighoshal14/")  

def open_google_profile():
    webbrowser.open_new("mailto:niladrighoshal.14@gmail.com")  

def open_twitter_profile():
    webbrowser.open_new("https://twitter.com/GhoshalNiladri")  


def signup_page():
    login_window.destroy()
    import signup

def login_user():
    
    if (
        usernameEntry.get()=='' or usernameEntry.get()=='Username'
        or passwordEntry.get()=='' or passwordEntry.get=='Password'
    ):
        messagebox.showerror('Error', 'All Fields are required')

    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='root')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error', 'connection with server is lost. Please try again later')
            return
        mycursor.execute('use userdata')

        query='select * from masterdata where username=%s'
        user_esists=(usernameEntry.get())
        mycursor.execute(query, user_esists)

        user_row = mycursor.fetchone()
        if user_row== None:
            messagebox.showerror('Error', 'This Username does not exists in database')

        else:

            hashed_password = hash_password(passwordEntry.get())
            query='select * from masterdata where username=%s and password=%s'
            values=(usernameEntry.get(), hashed_password)
            mycursor.execute(query, values)

            row = mycursor.fetchone()
            if row== None:
                messagebox.showerror('Error', 'Invalid Username or Password')
            else:
                usernameEntry.delete(0, END)
                passwordEntry.delete(0, END)
                # messagebox.showinfo('Welcome to LockBox', 'Login is successful')
                login_window.destroy()
                import passwordmgr


def handle_enter(event):
    login_user()




def forgot_password_page():
    login_window.destroy()
    import forgotpassword

#gui part
login_window = Tk()
login_window.geometry('990x660+280+90')
login_window.resizable(0, 0)
login_window.title('Login Page')

# Set the absolute path to the icon file
icon_path = "key.png"

# Try to open the icon using PIL
try:
    icon = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon)
    login_window.iconphoto(True, icon_photo)
except Exception as e:
    print("Error loading and setting window icon:", e)

bgImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(login_window, image=bgImage)
bgLabel.image = bgImage
bgLabel.place(x=0, y=0)

heading = Label(login_window, text='USER LOGIN', font=('Poppins', 23, 'bold'), bg='white', fg='firebrick1')
heading.place(x=605, y=120)

usernameEntry = Entry(login_window, width=25, font=('Poppins', 11), bd=0, fg='black')
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)
usernameEntry.bind('<FocusOut>', user_leave)

usernameEntry.bind('<Return>', handle_enter)

frame1 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame1.place(x=580, y=222)

passwordEntry = Entry(login_window, width=25, font=('Poppins', 11), bd=0, fg='black')
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)
passwordEntry.bind('<FocusOut>', password_leave)

passwordEntry.bind('<Return>', handle_enter)

frame2 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame2.place(x=580, y=282)

closeeye = PhotoImage(file='closeye.png')
openeye = PhotoImage(file='openeye.png')
eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=toggle_password_visibility)
eyeButton.place(x=800, y=253)

forgotPasswordButton = Button(login_window, text='Forgot Password?', bd=0, bg='white', activebackground='white', cursor='hand2', font=('poppins', 9, 'bold'), fg='SystemHighlight', activeforeground='SystemHighlight',command=forgot_password_page)
forgotPasswordButton.place(x=715, y=295)

loginButton = Button(login_window, text='Login', font=('poppins', 16, 'bold'), fg='white', bg='firebrick1',activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=19, command=login_user)
loginButton.place(x=578, y=330)

orLabel = Label(login_window, text='----------------  OR  ----------------', font=('poppins', 14), fg='firebrick1', bg='white')
orLabel.place(x=579, y=390)

facebook_logo = PhotoImage(file='facebook.png')
fbLabel = Label(login_window, image=facebook_logo, bg='white')
fbLabel.place(x=640, y=430)
fbLabel.bind("<Button-1>", lambda event: open_facebook_profile())

google_logo = PhotoImage(file='google.png')
googleLabel = Label(login_window, image=google_logo, bg='white')
googleLabel.place(x=690, y=430)
googleLabel.bind("<Button-1>", lambda event: open_google_profile())

twitter_logo = PhotoImage(file='twitter.png')
twitterLabel = Label(login_window, image=twitter_logo, bg='white')
twitterLabel.place(x=740, y=430)
twitterLabel.bind("<Button-1>", lambda event: open_twitter_profile())

signupLabel = Label(login_window, text='Dont have an account?', font=('poppins', 9, 'bold'), fg='firebrick1', bg='white')
signupLabel.place(x=590, y=490)

newaccountButton = Button(login_window, text='Create new one', bd=0, bg='white', activebackground='white', cursor='hand2', font=('poppins', 9, 'bold underline',), fg='SystemHighlight', activeforeground='SystemHighlight', command=signup_page)
newaccountButton.place(x=727, y=490)


login_window.mainloop()
