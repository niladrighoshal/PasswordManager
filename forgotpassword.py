from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql
import hashlib


def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()



def change_password():
    if (
        usernameEntry.get() == '' or usernameEntry.get() == 'Username'
        or newpasswordEntry.get() == '' or newpasswordEntry.get() == 'New Password'
        or confirmPasswordEntry.get() == '' or confirmPasswordEntry.get() == 'Confirm Password'
    ):
        messagebox.showerror('Error', 'All fields are required')

    elif newpasswordEntry.get() != confirmPasswordEntry.get():
        messagebox.showerror('Error', 'New Password and Confirm Password are not matching')

    
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='root', database='userdata')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return
        
        query='select * from masterdata where username=%s'
        mycursor.execute(query,(usernameEntry.get()))

        user_row=mycursor.fetchone
        if user_row == None:
            messagebox.showerror('Error','Username Does not Exists')

        else:
            hashed_password = hash_password(newpasswordEntry.get())
            query='update masterdata set password=%s where username=%s'
            
            mycursor.execute(query,(hashed_password,usernameEntry.get()))
            con.commit()
            con.close()
            usernameEntry.delete(0, END)
            newpasswordEntry.delete(0, END)
            confirmPasswordEntry.delete(0, END)
            messagebox.showinfo('Success', 'you have succcessfully changed the password. Login with your new password',parent=forgot_password_window)
            forgot_password_window.destroy()
            import signin







def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def user_leave(event):
    if not usernameEntry.get():
        usernameEntry.insert(0, 'Username')

def password_enter(event):
    if newpasswordEntry.get() == 'New Password':
        newpasswordEntry.delete(0, END)
        newpasswordEntry.config(show='●')
        eyeButton.config(image=closeeye)  # Change eye button image to close eye

def password_leave(event):
    if not newpasswordEntry.get():
        newpasswordEntry.config(show='')
        newpasswordEntry.insert(0, 'New Password')
        eyeButton.config(image=openeye)  # Change eye button image to open eye
    
    elif not password_visible:
        newpasswordEntry.config(show='●')
        eyeButton.config(image=closeeye)
def toggle_password_visibility():
    global password_visible
    if password_visible:
        newpasswordEntry.config(show='●')
        eyeButton.config(image=closeeye)
        password_leave(None)
    else:
        newpasswordEntry.config(show='')
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
    forgot_password_window.destroy()
    import signin



def handle_enter(event):
    change_password()








#gui part
forgot_password_window = Tk()
forgot_password_window.geometry('990x660+280+90')
forgot_password_window.resizable(0, 0)
forgot_password_window.title('Forgot Password Page')

# Set the absolute path to the icon file
icon_path = "key.png"

# Try to open the icon using PIL
try:
    icon = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon)
    forgot_password_window.iconphoto(True, icon_photo)
except Exception as e:
    print("Error loading and setting window icon:", e)

bgImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(forgot_password_window, image=bgImage)
bgLabel.image = bgImage
bgLabel.place(x=0, y=0)

heading = Label(forgot_password_window, text='RESET PASSWORD', font=('Poppins', 18, 'bold'), bg='white', fg='firebrick1')
heading.place(x=585, y=110)


usernameEntry = Entry(forgot_password_window, width=25, font=('Poppins', 11), bd=0, fg='black')
usernameEntry.place(x=580, y=180)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)
usernameEntry.bind('<FocusOut>', user_leave)
usernameEntry.bind('<Return>', handle_enter)

frame1 = Frame(forgot_password_window, width=250, height=2, bg='firebrick1')
frame1.place(x=580, y=205)

newpasswordEntry = Entry(forgot_password_window, width=25, font=('Poppins', 11), bd=0, fg='black')
newpasswordEntry.place(x=580, y=255)
newpasswordEntry.insert(0, 'New Password')
newpasswordEntry.bind('<FocusIn>', password_enter)
newpasswordEntry.bind('<FocusOut>', password_leave)
newpasswordEntry.bind('<Return>', handle_enter)

frame2 = Frame(forgot_password_window, width=250, height=2, bg='firebrick1')
frame2.place(x=580, y=280)

closeeye = PhotoImage(file='closeye.png')
openeye = PhotoImage(file='openeye.png')
eyeButton = Button(forgot_password_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=toggle_password_visibility)
eyeButton.place(x=800, y=250)


confirmPasswordEntry = Entry(forgot_password_window, width=25, font=('Poppins', 11), bd=0, fg='black')
confirmPasswordEntry.place(x=580, y=330)
confirmPasswordEntry.insert(0, 'Confirm Password')
confirmPasswordEntry.bind('<FocusIn>', confirmPassword_enter)
confirmPasswordEntry.bind('<FocusOut>', confirmPassword_leave)
confirmPasswordEntry.bind('<Return>', handle_enter)

frame4 = Frame(forgot_password_window, width=250, height=2, bg='firebrick1')
frame4.place(x=580, y=355)


submitButton = Button(forgot_password_window, text='Submit', font=('poppins', 16, 'bold'), fg='white', bg='firebrick1',activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=19,command=change_password)
submitButton.place(x=578, y=400)


alreadyaccount = Label(forgot_password_window, text='Remember the password?', font=('Poppins', 9, 'bold'), bg='white', fg='firebrick1')
alreadyaccount.place(x=575, y=480)

loginButton = Button(forgot_password_window, text='Attempt to Log in', bd=0, bg='white', activebackground='white', cursor='hand2', font=('poppins', 9, 'bold underline'), fg='SystemHighlight', activeforeground='SystemHighlight',command=login_page)
loginButton.place(x=735, y=478)




forgot_password_window.mainloop()
