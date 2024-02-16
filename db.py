import mysql.connector


class DB():
  # Connect to the database
  db = mysql.connector.connect(host="localhost", user="root", passwd="jan04198")
  cursor = db.cursor()
  def __init__(self):
    # check if database exists. if not, create it
    self.cursor.execute("SHOW DATABASES;")
    databases = self.cursor.fetchall()
    if ('notes',) not in databases:
      self.cursor.execute("CREATE DATABASE notes;")
      self.db.commit()
      print("Database created")
      
      # create user and note tables
      self.cursor.execute("USE notes;")
      self.cursor.execute("CREATE TABLE user (UID INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(15) NOT NULL, password VARCHAR(15) NOT NULL, role VARCHAR(10));")
      self.cursor.execute("CREATE TABLE note (NID INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50) NOT NULL, text VARCHAR(255) NOT NULL, UID INT NOT NULL, FOREIGN KEY (UID) REFERENCES user(UID));")
      self.db.commit()
      print("Tables created")
      
      # add admin user
      self.cursor.execute('INSERT INTO user (username, password, role) VALUES ("admin", "admin", "admin");')
      self.db.commit()
      print("Admin user added")
    else:  
      self.cursor.execute("USE notes;")

database = DB()