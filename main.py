import helper_functions
from db import database


def login():
  while True:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    database.cursor.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}';")
    user = database.cursor.fetchone()
    if user:
      print(f"Welcome {user[1]}")
      return user
    else:
      print("Invalid username or password! try again? (y/n)")
      ch = input("enter your choice: ").lower()
      if ch == 'n':
        return False

def register(username=False, password=False):
  if not username:
    username = helper_functions.longerThan(input("Enter your username: "), 15, "Username")
  if not password:
    password = helper_functions.longerThan(input("Enter your password: "), 15, "Password")
  role = "user"
  
  database.cursor.execute(f"SELECT * FROM user WHERE username = '{username}';")
  user = database.cursor.fetchone()
  if user:
    print("Username already exists!")
    ch = input("Do you want to try again? (y/n): ").lower()
    if ch == 'y':
      register(username,password)
    else:
      return False
  else:
    database.cursor.execute(f"INSERT INTO user (username, password, role) VALUES ('{username}', '{password}', '{role}');")
    database.db.commit()
    
    database.cursor.execute(f"SELECT * FROM user WHERE username = '{username}';")
    return database.cursor.fetchone()

def view_users(user):
  database.cursor.execute("SELECT * FROM user;")
  users = database.cursor.fetchall()
  for user in users:
    print(f"UID: {user[0]}, Username: {user[1]}, Role: {user[3]}")

def add_user(user):
  username = helper_functions.longerThan(input("Enter the username: "), 15, "Username")
  password = helper_functions.longerThan(input("Enter the password: "), 15, "Password")
  role = input("Enter the role: ")
  database.cursor.execute(f"INSERT INTO user (username, password, role) VALUES ('{username}', '{password}', '{role}');")
  database.db.commit()
  print("User added")

def edit_user(user):
  view_users(user)
  UID = int(input("Enter the UID of the user you want to edit: "))
  database.cursor.execute(f"SELECT * FROM user WHERE UID = {UID};")
  if not database.cursor.fetchone():
    print("User not found")
    return
  username = helper_functions.longerThan(input("Enter the new username: "), 15, "Username")
  password = helper_functions.longerThan(input("Enter the new password: "), 15, "Password")
  role = input("Enter the new role: ")
  database.cursor.execute(f"UPDATE user SET username = '{username}', password = '{password}', role = '{role}' WHERE UID = {UID};")
  database.db.commit()
  print("User edited")

def remove_user(user):
  view_users(user)
  UID = int(input("Enter the UID of the user you want to remove: "))
  database.cursor.execute(f"SELECT * FROM user WHERE UID = {UID};")
  if not database.cursor.fetchone():
    print("User not found")
    return
  database.cursor.execute(f"DELETE FROM user WHERE UID = {UID};")
  database.db.commit()
  print("User removed")

def view_notes(user,adm=True):
  if user[3] == 'admin' and adm:
    ch = input("Do you want to view someone else's notes? (y/n): ").lower()
    if ch == 'y':
      UID = int(input("Enter the UID of the user: "))
    else:
      UID = user[0]
  else:
    UID = user[0]
  
  database.cursor.execute(f"SELECT * FROM note WHERE UID = {UID};")
  notes = database.cursor.fetchall()
  for note in notes:
    print(f"NID: {note[0]}, Title: {note[1]}, Text: {note[2]}")

def add_note(user):
  title = helper_functions.longerThan(input("Enter the title of the note: "), 50, "Title")
  text = helper_functions.longerThan(input("Enter the text of the note: "), 255, "Text")
  database.cursor.execute(f"INSERT INTO note (title, text, UID) VALUES ('{title}', '{text}', {user[0]});")
  database.db.commit()
  print("Note added")

def remove_note(user):
  view_notes(user,False)
  NID = int(input("Enter the NID of the note you want to remove: "))
  database.cursor.execute(f"SELECT * FROM note WHERE NID = {NID} AND UID = {user[0]};")
  if not database.cursor.fetchone():
    print("You can't remove someone else's note")
    return
  database.cursor.execute(f"DELETE FROM note WHERE NID = {NID};")
  database.db.commit()
  print("Note removed")

def edit_note(user):
  view_notes(user)
  NID = int(input("Enter the NID of the note you want to edit: "))
  database.cursor.execute(f"SELECT * FROM note WHERE NID = {NID} AND UID = {user[0]};")
  if not database.cursor.fetchone():
    print("You can't edit someone else's note")
    return
  title = helper_functions.longerThan(input("Enter the new title of the note: "), 50, "Title")
  text = helper_functions.longerThan(input("Enter the new text of the note: "), 255, "Text")
  database.cursor.execute(f"UPDATE note SET title = '{title}', text = '{text}' WHERE NID = {NID};")
  database.db.commit()
  print("Note edited")

def UI(user):
  # view users, add user, edit user, remove user, view notes, add note, edit note, remove note
  functions = {
    1: view_notes,
    2: add_note,
    3: edit_note,
    4: remove_note
  }
  if user[3] == 'admin':
    functions[5] = view_users
    functions[6] = add_user
    functions[7] = edit_user
    functions[8] = remove_user
  functions[len(functions)+1] = 'exit'
  
  while True:
    for i in range(1,len(functions)+1):
      print(f"{i}. {functions[i].__name__.replace('_',' ') if callable(functions[i]) else functions[i]}")
    ch = int(input("Enter your choice: "))
    if ch == len(functions):
      break
    else:
      functions[ch](user)

while True:
  print("1. Login\n2. Register\n3. Exit")
  ch = int(input("Enter your choice: "))
  if ch == 1:
    user  = login()
    UI(user)
  elif ch == 2:
    user = register()
  elif ch == 3:
    break
  else:
    print("Invalid choice! try again")
