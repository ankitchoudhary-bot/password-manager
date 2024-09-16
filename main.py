from tkinter import *
from tkinter import messagebox
import pyperclip 
import json
window=Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)
canvas=Canvas(height=200,width=200)
logo_img=PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(column=1,row=0)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    import random
    letters=random.randint(5,9)
    symbol=random.randint(2,4)
    number=random.randint(3,6)
    alphabets=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S""T","U","V","W","X","Y","Z"]
    numbers=["1","2","3","4","5","6","7","8","9","0"]
    symbols=["#","$","%","*","&","@","(",")","!"]
    password=[]
    for i in range(1,letters+1):
        random_number=random.choice(alphabets)
        password+=random_number
    for i in range(1,symbol+1):
        random_symbol=random.choice(symbols)
        password+=random_symbol
    for i in range(1,number+1):
        random_number=random.choice(numbers)
        password+=random_number

    random.shuffle(password)
    final_password="".join(password)  
    password_entry.insert(0,final_password)
    pyperclip.copy(final_password)
#-----------------------------FIND PASSWORD---------------------------------#
def find_password():
    website=website_entry.get()
    try:
        with open("data.json") as data_file:
            data=json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No Data File Found.")
    else:
        if website in data:
            email=data[website]["email"]
            password=data[website]["password"]
            messagebox.showinfo(title=website,message=f"Email:{email}\n Password:{password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exists.")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website=website_entry.get()
    email=email_username_entry.get()
    password=password_entry.get()
    new_data={
        website:{
            "email":email,
            "password":password
        }
    }
    if len(website)==0 or len(password)==0:
        messagebox.showinfo(title="Oops!!",message="Please enter valid website or password")
    else:
        is_ok=messagebox.askokcancel(title=website,message=f"These are the details entered:\n Email:{email}\n Password:{password}\n Is it OK to save?")
        if is_ok:
            try:
                with open("data.json") as data_file:
                    data=json.load(data_file)
                    
            except FileNotFoundError:
                with open("data.json","w") as data_file:
                    json.dump(new_data,data_file,indent=4)
            else:
                data.update(new_data)
                with open("data.json","w") as data_file:
                    json.dump(data,data_file,indent=4)
            finally:       
                website_entry.delete(0,END)
                password_entry.delete(0,END)
        
        
# ---------------------------- UI SETUP ------------------------------- #
website_label=Label(text="Website:")
website_label.grid(column=0,row=1)

email_username_label=Label(text="Email/Username:")
email_username_label.grid(column=0,row=2)

password_label=Label(text="Password:")
password_label.grid(column=0,row=3)

website_entry=Entry(width=33)
website_entry.focus()
website_entry.grid(column=1,row=1)

email_username_entry=Entry(width=52)
email_username_entry.insert(0,"anki116799@gmail.com")
email_username_entry.grid(column=1,row=2,columnspan=2)

password_entry=Entry(width=33)
password_entry.grid(column=1,row=3)

generate_password_button=Button(text="Generate Password",width=15,command=generate_password)
generate_password_button.grid(column=2,row=3)

add_button=Button(text="Add",width=44,command=save)
add_button.grid(column=1,row=4,columnspan=2)

search_button=Button(text="Search",width=15,command=find_password)
search_button.grid(column=2,row=1)
window.mainloop()