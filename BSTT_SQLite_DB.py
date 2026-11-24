import sqlite3
import re
import BSTT_notification as notification
import datetime

# Class creation
class signed_in_user:
  def __init__(self):
    file=open("user_info.txt", "rt")
    self.username, self.id, self.organiser=eval(file.read())
    file.close()

  def sign_in(self, username, id, organiser):
    self.username=username
    self.id=id
    self.organiser=organiser
    info=self.username, self.id, self.organiser
    file=open("user_info.txt", "wt")
    file.write(str(info))
    file.close

  def sign_out(self):
    self.username = "Sign In"
    self.id = 0
    self.organiser=0
    info=self.username, self.id, self.organiser
    file=open("user_info.txt", "wt")
    file.write(str(info))
    file.close

minutes=["00","05","10","15","20","25","30","35","40","45","50","55"]
hours=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
days=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
months=["1","2","3","4","5","6","7","8","9","10","11","12"]
years=["2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]
seed=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]

sign_in_info=signed_in_user()

invalid_usernames=["Sign In"]

conn = sqlite3.connect("bstt.db")
cursor = conn.cursor()

def check_email(email: str):
  email_regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
  if re.fullmatch(email_regex, email):
    return True, ""
  else:
    return False, "Please enter a valid email."

def check_username(username: str):
  result=False
  if len(username) < 2:
    message= "Username must be at least 2 characters long."
  elif len(username) > 20:
    message="Username must be less than 20 characters long."
  elif username in invalid_usernames:
     message="Invalid Username"
  else:
    result=True
    message=""
  return result, message
    
def check_password(password: str):
  result = False
  if len(password) < 8:
    message = 'Password must be at least 8 characters long.'
  elif not re.search(r"[a-z]", password):
    message = 'Password must contain at least 1 lowercase character.'
  elif not re.search(r"[A-Z]", password):
    message = 'Password must contain at least 1 uppercase character.'
  elif not re.search(r"\d", password):
    message = 'Password must contain at least 1 number.'
  elif not re.search(r"[^a-zA-Z0-9]", password):
    message = 'Password must contain at least 1 special character.'
  else:
    result=True
    message = ''
  return result, message
  
def check_passwords_match(password1: str, password2: str):
  if password1 != password2:
    return False, "Passwords do not match."
  else:
    return True, ""

def create_tables():
  # TABLE CREATION QUERIES
  # DISABLING REFERENTIAL INTEGRITY TO CREATE NEW TABLE
  cursor.execute("PRAGMA foreign_keys = OFF")

  # USER TABLE
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS user(
  user_ID INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE, 
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  rec_email TEXT,
  organiser INTEGER NOT NULL,
  verified INTEGER NOT NULL,
  locked INTEGER NOT NULL,
  first_name TEXT,
  bio TEXT,
  main_char TEXT,
  secondary_char TEXT, 
  recent_event TEXT,
  recent_placement INTEGER,
  email_notif INTEGER
  )
  """)
  conn.commit()

  # ENABLING REFERENTIAL INTEGRITY TO CREATE NEW TABLES
  cursor.execute("PRAGMA foreign_keys = ON")

  # EVENT, PLAYERS AND MATCHUP TABLES
  cursor.executescript("""
  CREATE TABLE IF NOT EXISTS event(
  event_ID INTEGER PRIMARY KEY,
  event_name TEXT NOT NULL UNIQUE,
  details TEXT,
  day INTEGER NOT NULL,
  month INTEGER NOT NULL,
  year INTEGER NOT NULL,
  time TEXT NOT NULL,
  location TEXT NOT NULL,
  player_cap INTEGER NOT NULL,
  price NUMERIC(4,2) NOT NULL,
  event_status INTEGER,
  player1 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player2 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player3 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player4 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player5 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player6 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player7 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player8 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player9 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player10 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player11 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player12 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player13 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player14 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player15 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player16 INTEGER REFERENCES player(player_ID) ON DELETE CASCADE
  );
  
  CREATE TABLE IF NOT EXISTS player(
  player_ID INTEGER PRIMARY KEY,
  user_ID INTEGER REFERENCES user(user_ID),
  placement INTEGER NOT NULL,
  has_paid INTEGER NOT NULL,
  is_present INTEGER NOT NULL,
  seed INTEGER,
  m1 INTEGER REFERENCES matchup(matchup_ID),
  m2 INTEGER REFERENCES matchup(matchup_ID),
  m3 INTEGER REFERENCES matchup(matchup_ID),
  m4 INTEGER REFERENCES matchup(matchup_ID),
  gf INTEGER REFERENCES matchup(matchup_ID),
  l6 INTEGER REFERENCES matchup(matchup_ID),
  l5 INTEGER REFERENCES matchup(matchup_ID),
  l4 INTEGER REFERENCES matchup(matchup_ID),
  l3 INTEGER REFERENCES matchup(matchup_ID),
  l2 INTEGER REFERENCES matchup(matchup_ID),
  l1 INTEGER REFERENCES matchup(matchup_ID)
  );
  
  CREATE TABLE IF NOT EXISTS event_to_player(
  event_to_player_ID INTEGER PRIMARY KEY,
  event_ID INTEGER REFERENCES event(event_ID) ON DELETE CASCADE,
  player_ID INTEGER REFERENCES player(player_ID) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS matchup(
  matchup_ID INTEGER PRIMARY KEY,
  player_1_ID INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player_1_result INTEGER NOT NULL,
  player_2_ID INTEGER REFERENCES player(player_ID) ON DELETE CASCADE,
  player_2_result INTEGER NOT NULL
  )
  """)
  
def create_user(email: str, username: str, password: str):
    params = email, username, password
    try:
      cursor.execute("""INSERT INTO user (email, username, password, rec_email, organiser, verified, locked, first_name, bio, main_char, secondary_char, recent_event, recent_placement, email_notif)
                     VALUES (?, ?, ?, "", 0, 1, 0, "", "", "", "", "", "", 0)""", params)
      conn.commit()
    except Exception as e:
      message=(f"An error has occurred. \n {e}")
      color="red"
    else:
      message="User created successfully."
      color="green"
    return message, color

def create_event(event_name: str, day: int, month: int, year: int, time: str, location: str, price: float):
  params = event_name, day, month, year, time, location, price
  cursor.execute("""INSERT INTO event (event_name, details, day, month, year, time, location, player_cap, price, event_status)
                 VALUES (?, "", ?, ?, ?, ?, ?, 16, ?, 0)""", params)
  conn.commit()
  notification.send_event_notification(event_name)

def delete_event(event_name_f: str):
  cursor.execute("""DELETE FROM event
                 WHERE event_name = (?)""",(event_name_f,))
  conn.commit() # Cascade referencial integrity will automatically remove data from other tables linked to the event.

def login_user(username: str, password: str):
   if username == "":
      return False, 0, 0, "Enter a username."
   else:
      if password == "":
         return False, 0, 0, "Enter a password."
      else:
         cursor.execute("""SELECT password, user_ID, organiser
                        FROM user
                        WHERE username=(?)""", (username,))
         result = cursor.fetchone()
         if result is None:
            return False, 0, 0, "This user could not be found."
         else:
            if password == result[0]:
               return True, result[1], result[2], "Sign In Successful."
            else:
               return False, 0, 0, "Incorrect password."

def search(search_query: str, category: str):
    if category == "Users":
        cursor.execute("""SELECT username
        FROM user
        WHERE username COLLATE NOCASE LIKE (?)""", (("%" + search_query + "%"),))
    else:
        cursor.execute("""SELECT event_name, day, month, year, time, location, player_cap, price
        FROM event
        WHERE event_name COLLATE NOCASE LIKE (?)""", (("%" + search_query + "%"),))
    results=cursor.fetchall()
    return results

def insertion_sort(arr):
  n = len(arr)  # Get the length of the array
      
  if n <= 1:
    return  # If the array has 0 or 1 element, it is already sorted, so return
  
  for i in range(1, n):  # Iterate over the array starting from the second element
    key = arr[i]  # Store the current element as the key to be inserted in the right position
    j = i-1
    while j >= 0 and key[1] < arr[j][1]:  # Move elements greater than key one position ahead
      arr[j+1] = arr[j]  # Shift elements to the right
      j -= 1
      arr[j+1] = key  # Insert the key in the correct position
      
  return arr

def find_most_recently_participated_event(username_f: str):
  cursor.execute("""SELECT recent_event, recent_placement
                 FROM user
                 WHERE username = (?)""", (username_f,))
  cursor.fetchone()
    
def find_player_ID(user_ID_f: int):
   cursor.execute("""SELECT player_ID
                  FROM player
                  WHERE user_ID = (?)
                  ORDER BY player_ID DESC""", (user_ID_f,))
   result=cursor.fetchone()
   return result[0]

def find_event_ID(event_name_f: str):
  cursor.execute("""SELECT event_ID
                  FROM event
                  WHERE event_name = (?)""", (event_name_f,))
  result=cursor.fetchone()
  return result[0]

def remove_none(x):
  if x is not None:
    return True
  else:
    return False

def find_players_in_event(event_name_f: str):
  cursor.execute("""SELECT player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12, player13, player14, player15, player16
                   FROM event
                   WHERE event_name = (?)""", (event_name_f,))
  result=cursor.fetchone()
  return result

def find_player_attendance_paid_seeding(player_id_f: int):
  cursor.execute("""SELECT player_ID, is_present, has_paid, seed
                 FROM player
                 WHERE player_ID = (?)""", (player_id_f,))
  result = cursor.fetchone()
  return result

def display_players_in_event(event_name_f: str):
  results=find_players_in_event(event_name_f)
  results=list(filter(remove_none, results))
  for n in range(0, len(results)):
    results[n] = find_player_attendance_paid_seeding(results[n])
  return results

def find_no_of_players_in_event(event_name_f: str):
  result=find_players_in_event(event_name_f)
  no_of_players=0
  for n in result:
    if n is not None:
      no_of_players=no_of_players+1
  return no_of_players

def find_usernames_in_event(event_name_f: str):
  players=find_players_in_event(event_name_f)
  results=[]
  for player in players:
    if player is not None:
      results.append(find_username_from_player_ID(player))
  return results

def find_username_from_email(user_email_f: str):
  cursor.execute("""SELECT username
                  FROM user
                  WHERE email = (?)""", (user_email_f,))
  result=cursor.fetchone()
  return result[0]

def find_user_ID_from_username(username_f: str):
  cursor.execute("""SELECT user_ID
                 FROM user
                 WHERE username = (?)""", (username_f,))
  result=cursor.fetchone()
  return result[0]

def find_user_ID_from_player_ID(player_ID_f: int):
  cursor.execute("""SELECT user_ID
                 FROM player
                 WHERE player_ID = (?)""", (player_ID_f,))
  result=cursor.fetchone()
  return result[0]

def find_username_from_player_ID(player_ID_f: int):
  user_ID_f=find_user_ID_from_player_ID(player_ID_f)
  cursor.execute("""SELECT username
                 FROM user
                 WHERE user_ID = (?)""", (str(user_ID_f)))
  result=cursor.fetchone()
  return result

def find_email_notifiable_users():
  cursor.execute("""SELECT email
                  FROM user
                  WHERE email_notif = 1""")
  result=cursor.fetchall()
  return result

def find_main_char(user_ID_f: int):
  cursor.execute("""SELECT main_char
                 FROM user
                 WHERE user_ID = (?)""",(user_ID_f,))
  result=cursor.fetchone()
  return result[0]

def register_for_event(user_ID_f: int, event_name_f: str):
    message=("An error has occurred. Please try again later.")
    result=False
    event_ID_f=find_event_ID(event_name_f)

    # Add information to the player table for first part of sign up process
    cursor.execute("""INSERT INTO player (user_ID, placement, has_paid, is_present)
    VALUES (?, 0, 0, 0)""", (user_ID_f,))
    conn.commit()

    # Finding and saving the previously created playerID for later reference
    player_ID_f=find_player_ID(user_ID_f)
    # Searching all player columns in event table to determine which spaces are empty
    players=find_players_in_event(event_name_f)
    params=event_ID_f, player_ID_f
    for i in range(0,16):
      if players[i] is None:
        try:
          cursor.execute(f"""UPDATE event
                         SET player{i+1} = (?)
                         WHERE event_name = (?) """, (player_ID_f, event_name_f))
          conn.commit()
          cursor.execute("""INSERT INTO event_to_player(event_ID, player_ID)
                         VALUES (?, ?)""", params)
          conn.commit()
        except Exception as e:
          message=("An error has occurred. Please try again later.")
          print(e)
        else:
          message=("Registration successful.")
          result=True
        finally:
          break
    return result, message

       

    #cursor.execute("""INSERT INTO event (player_ID)
    #VALUES ((SELECT userID
    #FROM user
    #WHERE username = (?), logged_in_username), 0)""")

def check_for_existing_data(username: str, email: str):
  cursor.execute("""SELECT user_ID
                 FROM user
                 WHERE username COLLATE NOCASE = (?)""", (username,))
  result=cursor.fetchone()
  if result != None:
     return False, "This username is already in use."
  else:
     cursor.execute("""SELECT user_ID
                    FROM user
                    WHERE email COLLATE NOCASE = (?)""", (email,))
     result=cursor.fetchone()
     if result != None:
        return False, "This email is already in use."
     else:
        return True, "Attempting to send email verifcation code..."
     
def check_for_existing_event(event_name_f: str):
  cursor.execute("""SELECT event_name
                 FROM event
                 WHERE event_name = (?)""", (event_name_f,))
  result=cursor.fetchone()
  if result is not None:
    return True
  else:
    return False

def check_registration_status(user_ID_f: int, event_name_f: str):
  event_participant_IDs=find_players_in_event(event_name_f)
  for p in event_participant_IDs:
    if p is not None:
      user_ID_result=find_user_ID_from_player_ID(p)
      if str(user_ID_result) == str(user_ID_f):
        result=True
        break
  else:
    result=False
  return result

def search_upcoming_events():
  cursor.execute("""SELECT event_name, day, month, year, time, location, player_cap, price, event_status
                 FROM event
                 WHERE event_status = 0
                 ORDER BY year, month, day""", )
  results=cursor.fetchmany(3)
  return results
   
def search_active_events():
  cursor.execute("""SELECT event_name, day, month, year, time, location, player_cap, price, event_status
                 FROM event
                 WHERE event_status = 0
                 OR event_status = 1
                 ORDER BY event_status DESC, year ASC, month ASC, day ASC""")
  results=cursor.fetchall()
  return results

def event_details(name: str): # Returns details, day, month, year, time, location, player cap, price and event status (In that order)
  cursor.execute("""SELECT details, day, month, year, time, location, player_cap, price, event_status
                 FROM event
                 WHERE event_name = (?)""",(name,))
  result=cursor.fetchone()
  return result

def user_details(username_f: str):
  cursor.execute("""SELECT organiser, verified, first_name, bio, main_char, secondary_char, recent_event, recent_placement
                 FROM user
                 WHERE username = (?)""", (username_f,))
  result=cursor.fetchone()
  return result

def user_hidden_details(user_ID_f: int):
  cursor.execute("""SELECT rec_email, password, email_notif
                 FROM user
                 WHERE user_ID = (?)""", (user_ID_f,))
  result=cursor.fetchone()
  return result

def update_account_display_info(first_name_f, bio_f, main_char_f, secondary_char_f, user_ID_f):
  updated_info=first_name_f, bio_f, main_char_f, secondary_char_f, user_ID_f
  try:
    cursor.execute("""UPDATE user
                 SET first_name = (?), bio = (?), main_char = (?), secondary_char = (?)
                 WHERE user_ID = (?)""", (updated_info))
    conn.commit()
  except Exception as e:
    print(e)
    return False
  else:
    return True

def update_rec_email(rec_email_f:str, user_ID_f:int):
  try:
    cursor.execute("""UPDATE user
                 SET rec_email = (?)
                 WHERE user_ID = (?)""", (rec_email_f, user_ID_f))
    conn.commit()
  except Exception as e:
    print(e)
    return False
  else:
    print(rec_email_f)
    return True

def update_password(password_f:str, user_ID_f:int):
  try:
    cursor.execute("""UPDATE user
                 SET password = (?)
                 WHERE user_ID = (?)""", (password_f, user_ID_f))
    conn.commit()
  except Exception as e:
    print(e)
    return False
  else:
    return True

def update_email_notif(email_notif_f, user_ID_f:int):
  try:
    cursor.execute("""UPDATE user
                 SET email_notif = (?)
                 WHERE user_ID = (?)""", (email_notif_f, user_ID_f))
    conn.commit()
  except Exception as e:
    print(e)
    return False
  else:
    return True

def update_event(name, details, day, month, year, time, location):
  cursor.execute("""UPDATE event
                 SET details = (?), day = (?), month = (?), year = (?), time = (?), location = (?)
                 WHERE event_name = (?)""", (details, day, month, year, time, location, name))
  conn.commit()

def set_player_paid(player_id_f: int):
  cursor.execute("""UPDATE player
                 SET has_paid = 1
                 WHERE player_ID = (?)""", (player_id_f,))
  conn.commit()

def unset_player_paid(player_id_f: int):
  cursor.execute("""UPDATE player
                 SET has_paid = 0
                 WHERE player_ID = (?)""", (player_id_f,))
  conn.commit()

def set_player_present(player_id_f: int):
  cursor.execute("""UPDATE player
                 SET is_present = 1
                 WHERE player_ID = (?)""", (player_id_f,))
  conn.commit()

def unset_player_present(player_id_f: int):
  cursor.execute("""UPDATE player
                 SET is_present = 0
                 WHERE player_ID = (?)""", (player_id_f,))
  conn.commit()

def unregister_from_event(user_ID_f: int, event_name_f: str):
  event_participant_IDs=find_players_in_event(event_name_f)
  for p in event_participant_IDs:
    if p is not None:
      user_ID_result=find_user_ID_from_player_ID(p)
      if user_ID_result == user_ID_f:
        try:
          cursor.execute("""DELETE FROM player
                         WHERE player_ID = (?)""",(p,))
          conn.commit()
        except:
          message="An error occurred. Please try again later."
          color="red"
        else:
          message=f"Successfully unregistered from {event_name_f}."
          color="green"

def end_event(event_name_f: str):
  cursor.execute("""UPDATE event
                 SET event_status = 2
                 WHERE event_name = (?)""", (event_name_f,))

def begin_todays_events():
  current_date_time=datetime.datetime.now()
  cursor.execute("""UPDATE event
                 SET event_status = 1
                 WHERE day = (?) AND month = (?) AND year = (?) AND event_status = 0""", (current_date_time.day, current_date_time.month, current_date_time.year))
  conn.commit()

def end_past_events():
  current_date_time=datetime.datetime.now()
  cursor.execute("""UPDATE event
                 SET event_status = 2
                 WHERE year < (?) OR (year = (?) AND month < (?)) OR (year = (?) AND month = (?) AND day < (?))""", (current_date_time.year, current_date_time.year, current_date_time.month, current_date_time.year, current_date_time.month, current_date_time.day))
  conn.commit()

def auto_change_event_status():
  begin_todays_events()
  end_past_events()


# KEEP UNTIL FINISHED, EASE OF ACCESS
cursor.execute("UPDATE event SET day = (?), month = (?), year = (?) WHERE event_name='Test Event'",(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year))
conn.commit()