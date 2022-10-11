from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
password_gen = ''


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    global password_gen
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_numbers = [random.choice(numbers) for char in range(nr_numbers)]
    password_letters = [random.choice(letters) for char in range(nr_letters)]
    password_symbols = [random.choice(symbols) for char in range(nr_symbols)]
    password_list = [char for char in password_symbols + password_letters + password_numbers]

    random.shuffle(password_list)

    password_gen = "".join(password_list)
    password_text_box.insert(0, password_gen)
    pyperclip.copy(password_gen)


# ---------------------------- SAVE PASSWORD ------------------------------- #


# Function to add data into txt file
def add():
    website_entry = website_text_box.get().title()
    email_entry = email_text_box.get()
    password_entry = password_text_box.get()
    new_data = {
        website_entry: {
            'email': email_entry,
            'password': password_entry,
        }
    }

    if len(website_entry) == 0 or len(email_entry) == 0 or len(password_entry) == 0:
        messagebox.showerror(title='Sorry About That...', message='Please fill in all the boxes!')
    else:
        try:
            with open('day_29_data.json', mode='r') as file:
                data = json.load(file)

        except FileNotFoundError:
            print('No Data File Found. One Has Been Made.')
            with open('day_29_data.json', mode='w') as file:
                json.dump(new_data, file, indent=4)
                data = dict()
        except json.JSONDecodeError:
            data = dict()
        finally:
            data.update(new_data)

            with open('day_29_data.json', mode='w') as file:
                json.dump(data, file, indent=4)

            website_text_box.delete(0, END)
            password_text_box.delete(0, END)


# ---------------------------- SEARCH PASSWORD -------------------------- #

def find_password():
    website_entry = website_text_box.get().title()
    with open('day_29_data.json') as file:
        data = json.load(file)
    try:
        email_for_search = data[website_entry]['email']
    except KeyError as ke:
        messagebox.showerror(title='No Website Found', message=f'{ke} is not in the website library, please try again.')
    else:
        password_for_search = data[website_entry]['password']
        messagebox.showinfo(title='Login Info', message=f' Website: \n{website_entry}\nEmail: {email_for_search}\nPassword:\n'
                                                        f' {password_for_search}')
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

# logo
canvas = Canvas(width=200, height=200)
lock_image = PhotoImage(file='day_29_logo.png')
canvas.create_image((120, 100), image=lock_image)
canvas.grid(column=1, row=0)

# Website Label
website = Label(text='Website: ')
website.grid(column=0, row=1)

# Website Text Box
website_text_box = Entry(width=21)
website_text_box.focus()
website_text_box.grid(column=1, row=1, columnspan=1)

#Website Button
website_search = Button(text='Search', command=find_password)
website_search.config(width=10)
website_search.grid(column=2, row=1)

# Email/Username Label
email = Label(text='Email/Username:')
email.grid(column=0, row=2)

# Email Text Box
email_text_box = Entry(width=35)
email_text_box.insert(0, 'aadesomoju001@gmail.com')
email_text_box.grid(column=1, row=2, columnspan=2)

# Password Label
password = Label(text="Password:")
password.grid(column=0, row=3)

# Password Text Box
password_text_box = Entry(width=21)
password_text_box.grid(column=1, row=3, columnspan=1)

# Password Button
password_generator = Button(text='Generate Password', command=generate_password)
password_generator.config(width=10)
password_generator.grid(column=2, row=3)

# Add Button
add_button = Button(text='Add', command=add)
add_button.config(height=1, width=33)
add_button.grid(columnspan=2, column=1, row=4)

window.mainloop()
