from PIL import Image
from random import randint
import customtkinter
import BSTT_SQLite_DB as database
import BSTT_notification as notification
import BSTT_char_icon_dictionary as dict
import datetime



# Creating tables if not already existing
database.create_tables()

# Setting variables for icons used
home_image = customtkinter.CTkImage(Image.open("images/home.png"), size=(20,20))
user_image = customtkinter.CTkImage(Image.open("images/user.png"), size=(20,20))
search_image=customtkinter.CTkImage(Image.open("images/search.png"), size=(20,20))
event_image = customtkinter.CTkImage(Image.open("images/event.png"), size=(20,20))
plus_image = customtkinter.CTkImage(Image.open("images/plus.png"), size=(20,20))
background_image=customtkinter.CTkImage(Image.open("images/background.png"),size=(1280,720))
smash_ball_image=customtkinter.CTkImage(Image.open("images/smash_ball.png"), size=(75,75))

# Initialising GUI
app = customtkinter.CTk()
app.geometry("1280x720")
app.configure(bg="#282828")
app.resizable(False, False)
app.title("BSTT")
account_page=None

# Object creation
sign_in_info=database.signed_in_user()



#Subroutine definitions
def span_multiple_lines(text:str):
  text_length=len(text)
  in_progress=True
  new_text=""
  while in_progress is True:
    if text_length>50:
      new_text=new_text+(text[:50])+" \n"
      text=text[50:]
      text_length=len(text)
    else:
      in_progress=False
      new_text=new_text+text
  return new_text

def hidden_email(email:str):
  if "@" in email:
    i=email.find("@")
    email="*****"+email[(i-2):]
  return email

def correct_currency_format(currency: str):
  currency=str(currency)
  if currency.find(".")==-1:
    currency=currency+".00"
  elif len(currency[currency.find(".")+1:]) == 0:
    currency=currency+"00"
  elif len(currency[currency.find(".")+1:]) == 1:
    currency=currency+"0"
  return currency

def select_character_icon(character: str):
  if character in dict.character_icon_dict:
    return dict.character_icon_dict[character]
  else:
    return None

def combobox_selection(choice):
  if choice =="    View Profile":
    load_user_info_page(sign_in_info.username)
  elif choice=="    Settings":
    load_account_settings_page(sign_in_info.id)
  elif choice=="    Sign Out":
    sign_out()

def edit_segmented_button_selection(choice): 
  if choice=="Edit Profile":
    load_account_display_page(sign_in_info.username)
  elif choice=="Account Settings":
    load_account_settings_page(sign_in_info.username)

def attendance_switch_toggle(state, player_id):
  if state == 1:
    database.set_player_present(player_id)
  elif state == 0:
    database.unset_player_present(player_id)

def paid_switch_toggle(state, player_id):
  if state == 1:
    database.set_player_paid(player_id)
  elif state == 0:
    database.unset_player_paid(player_id)

def mc_user_icon():
  mc=database.find_main_char(sign_in_info.id)
  icon=select_character_icon(mc)
  if icon is None:
    icon=user_image
  return icon

def kill_all_widgets():
  window_frame.destroy()

def create_verification_code():
  code="0"
  for n in range(1,6):
    code=code+str(randint(0,9))
  return code

def load_navbar():
  # Initialising navbar
  global navbar
  navbar=customtkinter.CTkFrame(master=window_frame, height=50, border_width=0, bg_color="white", fg_color="white",)

  # Initialising home button
  global home_button
  home_button=customtkinter.CTkButton(master=navbar, width=50, height=50, image=home_image, text="", hover_color="white", command=home_button_press, bg_color="white", fg_color="white")

  # Initialising search bar & variable
  global search_bar
  search_bar=customtkinter.CTkEntry(master=navbar, width=200, height=30, bg_color="white", placeholder_text="Search for...", placeholder_text_color="grey", text_color="white")

  # Initialising search category select
  global search_category
  search_category=customtkinter.CTkOptionMenu(master=navbar, width=75, height=30, values=["Users","Events"],fg_color="#343434",button_color="#343434")

  # Initialising search icon
  global search_button
  search_button=customtkinter.CTkButton(master=navbar, width=30, height=30, bg_color="white",fg_color="white", image=search_image, hover_color="white", text="", command=search_for)

  # Initialising user profile button
  global user_button_frame
  user_button_frame=customtkinter.CTkFrame(master=navbar, width=100, height=50, bg_color="white", border_color="white", fg_color="white")
  user_button_frame.place(x=5, y=0)
  global user_button
  user_button=customtkinter.CTkButton(master=user_button_frame, width=50, height=52, corner_radius=0, bg_color="white", border_color="white", fg_color="white", hover_color="white", image=user_image, text=sign_in_info.username, text_color="black", command=account_login)
  if sign_in_info.id != 0:
    user_button.configure(image=mc_user_icon(), command=lambda: load_user_info_page(sign_in_info.username))
    user_combobox=customtkinter.CTkComboBox(master=user_button_frame, width=50, corner_radius=0, height=52, fg_color="white", bg_color="white", border_color="white", button_color="#282828", values=["    View Profile", "    Settings", "    Sign Out"], command=combobox_selection)
  if sign_in_info.organiser==1:
    create_event_button=customtkinter.CTkButton(master=navbar, width=100, height=50, corner_radius=0, bg_color="white", border_color="white", fg_color="white", hover_color="white", image=event_image, text="Event Management", text_color="black", command=load_event_management_page)
  

  # Placing navbar widgets
  navbar.place(x=0, y=0, relwidth=1)
  home_button.place(x=1220, y=0)
  user_button.grid(column=0, row=0)
  if sign_in_info.id !=0:
    user_combobox.grid(column=1, row=0) #type: ignore - In the case that id != 0, the combobox will always be created.
  search_bar.place(x=453, y=10)
  search_category.place(x=658,y=10)
  search_button.place(x=738, y=10)
  if sign_in_info.organiser==1:
    create_event_button.place(x=1050, y=0) # type: ignore - In the case that organiser == 1, the event button will always be created.

def load_window():
  # Initialising main frame
  global window_frame
  window_frame=customtkinter.CTkFrame(master=app, width=1280, height=720, bg_color="#343434", fg_color="#343434")
  # Initialising background
  global background
  background=customtkinter.CTkLabel(master=window_frame, image=background_image,text="")
  window_frame.place(x=0, y=0)
  background.pack()
  load_navbar()

def load_home_screen():
  load_window()
  upcoming_events_text=customtkinter.CTkLabel(master=window_frame, width=150, height=50, text=f"Upcoming Events:", font=("CTkFont", 50), text_color="white", bg_color="#282828", fg_color="#282828")
  global home_screen_frame
  home_screen_frame=customtkinter.CTkFrame(master=window_frame, width=580, height=670, border_width=0, fg_color="#282828")
  home_screen_frame.place(x=0, y=50)
  upcoming_events_text.place(x=600, y=100)
  upcoming_events=database.search_upcoming_events()
  if upcoming_events != []: # If any upcoming events are found:
    for i in range(len(upcoming_events)):
      event_frame=customtkinter.CTkFrame(master=home_screen_frame, width=500, height=200, fg_color="white")
      event_frame_title=customtkinter.CTkLabel(master=event_frame, width=200, height=40, corner_radius=10, text=(upcoming_events[i][0]), text_color="black", font=("CTkFont", 35), anchor="w")
      event_frame_details=customtkinter.CTkLabel(master=event_frame, width=100, height=130, text=f" - {upcoming_events[i][1]}/{upcoming_events[i][2]}/{upcoming_events[i][3]}, {upcoming_events[i][4]} \n - Held at {upcoming_events[i][5]} \n - Caps at {upcoming_events[i][6]} players \n - £{correct_currency_format(upcoming_events[i][7])} entry fee", text_color="black", font=("CTkFont", 20), anchor="w")
      event_frame_button=customtkinter.CTkButton(master=event_frame, width=125, height=63, text="View Details", hover_color="#282828", bg_color="white", fg_color="#282828", text_color="white", font=("CTkFont", 15), command=lambda j=i: load_event_info_page(upcoming_events[j][0]))
      event_frame.place(x=40, y=((217*(i+1))-200))
      event_frame_title.place(x=20, y=10)
      event_frame_details.place(x=10, y=60)
      event_frame_button.place(x=360, y=68)
  else:
    no_events_text=customtkinter.CTkLabel(master=home_screen_frame, width=500, height=100, corner_radius=10, text="No events to display.", text_color="white", font=("CTkFont", 50))
    no_events_text.place(x=40, y=285)

def home_button_press():
  kill_all_widgets()
  load_home_screen()

def attempt_login():
  username=login_username_bar.get()
  password=login_password_bar.get()
  result, id, organiser, message=database.login_user(username, password)
  if result == True: # If data matched what was already stored in database
    login_response_text.configure(text=message, text_color="green")
    sign_in_info.sign_in(username, id, organiser)
    user_button.configure(text=sign_in_info.username)
    account_page.destroy() #type: ignore
    kill_all_widgets()
    load_home_screen()
  else:
    login_response_text.configure(text=message, text_color="red")

def attempt_signup():
  email=signup_email_bar.get()
  username=signup_username_bar.get()
  password=signup_password_bar.get()
  password_confirmation=signup_password_confirmation_bar.get()
  email_regex_result, message=database.check_email(email)
  if email_regex_result==True: # If no issues with email
    username_result, message=database.check_username(username)
    if username_result==True: # If no issues are found with username:
      password_result, message=database.check_password(password)
      if password_result == True: # If no issues with password
        password_confirmation_result, message=database.check_passwords_match(password, password_confirmation)
        if password_confirmation_result==True: # If passwords match
          data_result, message=database.check_for_existing_data(username, email)
          if data_result == True: # If matching data was not found
            signup_response_text.configure(text=message, text_color="green")
            verification_code=create_verification_code()
            verification_email_result, message=notification.verification_email(email, username, verification_code)
            if verification_email_result==True: # If email successfully sends
              verification_code_box=customtkinter.CTkInputDialog(title="Enter Verification Code", text="Please enter the verification code you received in the E-Mail that has just been sent.")
              verification_code_box_response=str(verification_code_box.get_input())
              while verification_code_box_response != verification_code and verification_code_box_response != None:
                verification_code_box=customtkinter.CTkInputDialog(title="Enter Verification Code", text="The verification code you entered is incorrect. Please try again.")
                verification_code_box_response=verification_code_box.get_input()
              if verification_code_box_response == verification_code:
                message, color=database.create_user(email, username, password)
                signup_response_text.configure(text=message, text_color=color)
                sign_in_info.sign_in(username, database.find_user_ID_from_username(username), 0) # Users cannot be organisers unless they are given the role
                user_button.configure(text=sign_in_info.username)
                account_page.destroy() #type: ignore
                kill_all_widgets()
                load_home_screen()
            else:
              signup_response_text.configure(text=message, text_color="red")
          else:
            signup_response_text.configure(text=message, text_color="red")
        else:
          signup_response_text.configure(text=message, text_color="red")
      else:
        signup_response_text.configure(text=message, text_color="red")
    else:
      signup_response_text.configure(text=message, text_color="red")
  else:
    signup_response_text.configure(text=message, text_color="red")

def attempt_event_creation(name, desc, day, month, year, time, price, location):
  name=name.strip()
  desc=desc.strip()
  price=price.strip()
  location=location.strip()
  results= False, "An error occurred. Please try again later."
  past_date_check=False
  if name == "":
    results= False, "Enter a name for the event."
  elif database.check_for_existing_event(name) is True: # If an event with the same name is found:
    results= False, "There is already an event with this name in the database."
  elif price == "":
    results= False, "Enter a price for the event."
  elif location == "":
    results=False, "Enter a location for the event."
  else:
    try:
      price=float(price)
    except ValueError:
      results= False, "Incorrect price format."
    else:
      current_date_time=datetime.datetime.now()
      if year<current_date_time.year:
        results= False, "Event date cannot be set in the past."
      elif year==current_date_time.year:
        if month<current_date_time.month:
          results= False, "Event date cannot be set in the past."
        elif month==current_date_time.month:
          if day<current_date_time.day:
            results= False, "Event date cannot be set in the past."
          elif day==current_date_time.day:
            results= False, "Event date cannot be set for the day of creation."
          else:
            past_date_check=True
        else:
          past_date_check=True
      else:
        past_date_check=True
  
  if past_date_check is True:
    event_response_text.configure(text_color="yellow", text="Creating event...")
    database.create_event(name, day, month, year, time, location, price)
    results= True, "Event creation successful."
  return results

def begin_event_creation(name, desc, day, month, year, time, price, location):
  result,message=attempt_event_creation(name, desc, day, month, year, time, price, location)
  if result == False:
    event_response_text.configure(text_color="red", text=message)
  else:
    event_response_text.configure(text_color="green", text=message)
    load_event_management_page()

def attempt_event_edit(name, desc, day, month, year, time, location):
  desc=desc.strip()
  location=location.strip()
  results= False, "An error occurred. Please try again later."
  past_date_check=False
  if location == "":
    results=False, "Enter a location for the event."
  else:
    current_date_time=datetime.datetime.now()
    if year<current_date_time.year:
      results= False, "Event date cannot be set in the past."
    elif year==current_date_time.year:
      if month<current_date_time.month:
        results= False, "Event date cannot be set in the past."
      elif month==current_date_time.month:
        if day<current_date_time.day:
          results= False, "Event date cannot be set in the past."
        elif day==current_date_time.day:
          results= False, "Event date cannot be set for the day of creation."
        else:
          past_date_check=True
      else:
        past_date_check=True
    else:
      past_date_check=True
  
  if past_date_check is True:
    edit_event_response_text.configure(text_color="yellow", text="Updating event...")
    database.update_event(name, desc, day, month, year, time, location)
    results= True, "Event update successful."
  if results[0] is True:
    edit_event_response_text.configure(text_color="green", text=results[1])
    load_event_management_page()
  elif results[0] is False:
    edit_event_response_text.configure(text_color="red", text=results[1])

def attempt_end_event(event_name: str):
  database.end_event(event_name)
  load_event_management_page()

def attempt_delete_event(name):
  if edit_event_response_text.cget("text") != "!! DELETE BUTTON PRESSED - PRESS AGAIN TO CONFIRM !!": # If button has not yet been pressed once:
    edit_event_response_text.configure(text_color="red", text="!! DELETE BUTTON PRESSED - PRESS AGAIN TO CONFIRM !!")
  else:
    database.delete_event(name)
    load_event_management_page()

def attempt_event_registration(user_ID_f: int, event_name_f: str):
  result, message=database.register_for_event(user_ID_f, event_name_f)
  registration_response=customtkinter.CTkLabel(master=window_frame, width=236, height=40, text=message, bg_color="white", fg_color="white", text_color="black", font=("CTkFont", 20))
  if result==False:
    registration_response.configure(text_color="red")
    registration_response.place(x=804, y=660)
  else:
    registration_response.configure(text_color="green")
    registration_response.place(x=804, y=660)
    load_event_info_page(event_name_f)

def attempt_save_account_display_info(first_name_f: str, bio_f: str, main_char_f: str, secondary_char_f: str):
  if main_char_f=="N/A":
    main_char_f=""
  if secondary_char_f=="N/A":
    secondary_char_f=""
  if database.update_account_display_info(first_name_f, bio_f, main_char_f, secondary_char_f, sign_in_info.id) is True:
    load_main_settings_page()
    message=customtkinter.CTkLabel(master=window_frame, width=200, height=10, text="Changes saved successfully.", bg_color="#282828", fg_color="#282828", text_color="green", font=("CTkFont", 20))
    message.place(x=500, y=690)
  else:
    message=customtkinter.CTkLabel(master=window_frame, width=200, height=10, text="An error occurred. Please try again later.", bg_color="#282828", fg_color="#282828", text_color="red", font=("CTkFont", 20))
    message.place(x=500, y=690) 

def attempt_save_account_settings(recovery_email_f:str, entered_recovery_email_f:str, old_password_f:str, entered_old_password_f:str, new_password_f:str, confirm_new_password_f:str, recieve_email_notif: int):
  edit_fail = False
  message="Changes saved successfully."
  try:
    response_text.configure(text="") # type: ignore
  except Exception:
    response_text=customtkinter.CTkLabel(master=window_frame, width=200, height=10, text="", bg_color="#282828", fg_color="#282828", text_color="red", font=("CTkFont", 20))
    response_text.place(x=500, y=690)
  finally:
    if entered_old_password_f == old_password_f: # If the password entered in the text box is the same as the original password
      if new_password_f is not None or confirm_new_password_f is not None:
        password_result, password_message=database.check_password(new_password_f)
        if password_result == True: # If no issues with password
          password_confirmation_result, password_message=database.check_passwords_match(new_password_f, confirm_new_password_f)
          if password_confirmation_result==True: # If passwords match
            change_password=database.update_password(new_password_f, sign_in_info.id)
          else:
            edit_fail=True
            message="Passwords do not match."
        else:
          edit_fail=True
          message=password_message
    elif entered_old_password_f != "":
      edit_fail=True
      message="Incorrect Password"
    if entered_recovery_email_f !=hidden_email(recovery_email_f):
      if database.check_email(entered_recovery_email_f)[0] is True or entered_recovery_email_f == "":
        change_rec_email=database.update_rec_email(entered_recovery_email_f, sign_in_info.id)
      else:
        edit_fail=True
    change_email_notif=database.update_email_notif(recieve_email_notif, sign_in_info.id)
    if edit_fail is True:
      response_text.configure(text=message) # type: ignore
    
    else:
      load_main_settings_page()
      response_text=customtkinter.CTkLabel(master=window_frame, width=200, height=10, text=message, bg_color="#282828", fg_color="#282828", text_color="green", font=("CTkFont", 20))
      response_text.place(x=500, y=690)

def check_event_registration_button_status(event_name_f: str, player_cap_f: int, event_state_f: int, user_ID_f: int):
  button_state="disabled"
  if event_state_f == 1:
    message="This event is currently in progress."
  elif event_state_f==2:
    message="This event has ended."
  elif database.find_no_of_players_in_event(event_name_f) == player_cap_f:
    message="This event is full."
  elif user_ID_f == 0:
    message="Sign in to register."
  elif database.check_registration_status(user_ID_f, event_name_f) == True:
    message="You have already registered for this event."
  else:
    button_state="normal"
    message="Register for event"
  return message, button_state

def search_for():
  query=search_bar.get()
  category=search_category.get()
  results=database.search(query, category)

  kill_all_widgets()
  load_window()

  search_title=customtkinter.CTkLabel(master=window_frame, width=150, height=50, text=f"Showing results for {query}:", font=("CTkFont", 45), text_color="white", bg_color="#282828", fg_color="#282828")
  results_list_frame=customtkinter.CTkScrollableFrame(master=window_frame, width=570, height=670)
  search_title.place(x=600, y=100)
  results_list_frame.place(x=0, y=50)
  if category == "Users":
    for result in results:
      result_frame=customtkinter.CTkFrame(master=results_list_frame, width=570, height=100, bg_color="#282828", fg_color="#282828", border_width=1, border_color="white")
      result_title=customtkinter.CTkLabel(master=result_frame, width=200, height=80, bg_color="#282828", fg_color="#282828", text=result[0], text_color="white", font=("CTkFont", 40))
      result_view_button=customtkinter.CTkButton(master=result_frame, width=80, height=50, bg_color="#282828", fg_color="white", text="View User", anchor="w", text_color="black", font=("CTkFont", 15), hover_color="white", command=lambda j=result[0]: load_user_info_page(j))
      result_frame.pack()
      result_title.place(x=10, y=10)
      result_view_button.place(x=450, y=25)
  else:
    for result in results:
      result_frame=customtkinter.CTkFrame(master=results_list_frame, width=570, height=100, bg_color="#282828", fg_color="#282828", border_width=1, border_color="white")
      result_title=customtkinter.CTkLabel(master=result_frame, width=100, height=25, corner_radius=10, text=(result[0]), bg_color="#282828", fg_color="#282828", text_color="white", font=("CTkFont", 40), anchor="w")
      result_details=customtkinter.CTkLabel(master=result_frame, width=100, height=40, bg_color="#282828", fg_color="#282828", text=f" - {result[1]}/{result[2]}/{result[3]}, {result[4]} \n - Held at {result[5]} \n - Caps at {result[6]} players \n - £{correct_currency_format(result[7])} entry fee", text_color="white", font=("CTkFont", 10), anchor="w")
      result_view_button=customtkinter.CTkButton(master=result_frame, width=100, height=50, bg_color="#282828", fg_color="white", text="View Event", text_color="black", font=("CTkFont", 15), hover_color="white", command=lambda j=result[0]:load_event_info_page(j))
      result_frame.pack()
      result_title.place(x=5, y=5)
      result_details.place(x=5, y=50)
      result_view_button.place(x=450, y=25)

def account_creation():
  login_page_frame.destroy()
  # Initialising frame for signup screen
  global signup_page_frame
  signup_page_frame=customtkinter.CTkFrame(master=account_page, width=300, height=400)
    
  # Initialising icon for signup screen
  account_page_image=customtkinter.CTkLabel(master=signup_page_frame, width=75, height=75, image=smash_ball_image, text="")

  # Initialising "Create Account" text
  create_account_text=customtkinter.CTkLabel(master=signup_page_frame, width=200, height=10, text="Create an Account:", text_color="white", bg_color="transparent", fg_color="#2a2a2a")

  # Initialising email bar for signup screen
  global signup_email_bar
  signup_email_bar=customtkinter.CTkEntry(master=signup_page_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", placeholder_text="Email", placeholder_text_color="grey", text_color="black")

  # Initialising username bar for signup screen
  global signup_username_bar
  signup_username_bar=customtkinter.CTkEntry(master=signup_page_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", placeholder_text="Username", placeholder_text_color="grey", text_color="black")
    
  # Initialising password bar for signup screen
  global signup_password_bar
  signup_password_bar=customtkinter.CTkEntry(master=signup_page_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", placeholder_text="Password", show="*", placeholder_text_color="grey", text_color="black")
  
  # Initialising password bar for signup screen
  global signup_password_confirmation_bar
  signup_password_confirmation_bar=customtkinter.CTkEntry(master=signup_page_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", placeholder_text="Confirm Password", show="*", placeholder_text_color="grey", text_color="black")
  
  # Initialising OK button for login screen
  signup_button=customtkinter.CTkButton(master= signup_page_frame, width=50, height=30, bg_color="transparent", fg_color="white", text="OK", text_color="black", corner_radius=10, hover_color="white", command=attempt_signup)

  # Initialising response text for signup screen
  global signup_response_text
  signup_response_text=customtkinter.CTkLabel(master=signup_page_frame, width=300, height=10, text="", text_color="red", bg_color="transparent", fg_color="#2a2a2a")

  # Initialising login button for signup screen
  account_login_button=customtkinter.CTkButton(master=signup_page_frame, width=150, height=30, text="Already have an account? \n Click here to sign in.", text_color="blue", bg_color="transparent", fg_color="#2a2a2a", border_color="#2a2a2a", hover_color="#2a2a2a", command=back_to_login)

  signup_page_frame.place(x=0, y=0)
  account_page_image.place(x=113, y=5)
  create_account_text.place(x=0, y=80)
  signup_email_bar.place(x=50, y=100)
  signup_username_bar.place(x=50, y=150)
  signup_password_bar.place(x=50, y=200)
  signup_password_confirmation_bar.place(x=50, y=250)
  signup_button.place(x=125, y=300)
  signup_response_text.place(x=0, y=350)
  account_login_button.place(x=75, y=365)
  
def back_to_login():
  signup_page_frame.destroy()
  account_login()

def account_login():
  if sign_in_info.username=="Sign In": # If the user is not yet signed in
    global account_page
    try:
      account_page.focus() # type: ignore
    except:
      account_page=customtkinter.CTkToplevel()
      account_page.geometry("300x400")
      account_page.resizable(False, False)
      account_page.title("Sign In to BSTT")
      account_page.attributes("-topmost", True)
    finally:   
      # Initialising frame for login screen
      global login_page_frame
      login_page_frame=customtkinter.CTkFrame(master=account_page, width=300, height=400)
    
      # Initialising icon for login screen
      account_page_image=customtkinter.CTkLabel(master=login_page_frame, width=75, height=75, image=smash_ball_image, text="")

      # Initialising "Sign In" text
      login_text=customtkinter.CTkLabel(master=login_page_frame, width=200, height=10, text="Log In:", text_color="white", bg_color="transparent", fg_color="#2a2a2a")

      # Initialising username bar for login screen
      global login_username_bar
      login_username_bar=customtkinter.CTkEntry(master=login_page_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", placeholder_text="Username", placeholder_text_color="grey", text_color="black")
    
      # Initialising password bar for login screen
      global login_password_bar
      login_password_bar=customtkinter.CTkEntry(master=login_page_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", placeholder_text="Password", show="*", placeholder_text_color="grey", text_color="black")

      # Initialising OK button for login screen
      login_button=customtkinter.CTkButton(master=login_page_frame, width=50, height=30, bg_color="transparent", fg_color="white", text="OK", text_color="black", corner_radius=10, hover_color="white", command=attempt_login)
    
      # Initialising response message for login screen
      global login_response_text
      login_response_text=customtkinter.CTkLabel(master=login_page_frame, width=300, height=10, text="", text_color="red", bg_color="transparent", fg_color="#2a2a2a")

      # Initialising account creation button for login screen
      account_create_button=customtkinter.CTkButton(master=login_page_frame, width=150, height=30, text="Don't have an account? \n Click here to create one.", text_color="blue", bg_color="transparent", fg_color="#2a2a2a", border_color="#2a2a2a", hover_color="#2a2a2a", command=account_creation)

      login_page_frame.place(x=0, y=0)
      account_page_image.place(x=113, y=5)
      login_text.place(x=0, y=100)
      login_username_bar.place(x=50, y=125)
      login_password_bar.place(x=50, y=175)
      login_button.place(x=125, y=225)
      login_response_text.place(x=0, y=350)
      account_create_button.place(x=75, y=365)
  else:
    sign_in_info.sign_out() # Placeholder for account page
    user_button.configure(text=sign_in_info.username)

def sign_out():
  sign_in_info.sign_out()
  home_button_press()

def load_event_registration_frame(event_name, player_cap, status):
  global event_participant_frame
  event_participant_frame=customtkinter.CTkFrame(master=window_frame, width=256, height=500, bg_color="white", fg_color="white")
  event_participant_list_text=customtkinter.CTkLabel(master=event_participant_frame, width=256, height=50, text=f"Current players:\n{database.find_no_of_players_in_event(event_name)}/{player_cap}", text_color="black", font=("CTkFont", 25), fg_color="white", bg_color="white")
  event_participant_list_frame=customtkinter.CTkScrollableFrame(master=event_participant_frame, width=236, height=350, bg_color="white", fg_color="#282828", scrollbar_fg_color="#282828", scrollbar_button_color="white")
  event_participant_frame.place(x=804, y=135)
  event_participant_list_text.place(x=0, y=13)
  event_participant_list_frame.place(x=0, y=75)
  participant_list=database.find_usernames_in_event(event_name)
  for participant in participant_list:
    if len(participant[0]) > 1:
      participant = participant[0]
    participant_name_frame=customtkinter.CTkFrame(master=event_participant_list_frame, width=236, height=40, bg_color="#282828", fg_color="#282828", border_width=1, border_color="white")
    participant_name_text=customtkinter.CTkLabel(master=participant_name_frame, width=236, height=39, text=participant, bg_color="#282828", fg_color="#282828", text_color="white", font=("CTkFont", 20))
    participant_name_frame.pack()
    participant_name_text.place(x=0, y=0)
  event_registration_button=customtkinter.CTkButton(master=event_participant_frame, width=256, height=75, text="", bg_color="white", fg_color="white", text_color="black", hover_color="white", command=lambda: attempt_event_registration(sign_in_info.id, event_name))
  def_text, def_state=check_event_registration_button_status(event_name, player_cap, status, sign_in_info.id)
  event_registration_button.configure(state=def_state, text=def_text)
  event_registration_button.place(x=0, y=425)

def load_event_info_page(event_name: str):

  kill_all_widgets()
  load_window()

  details,day,month,year,time,location,player_cap,price,status=database.event_details(event_name)
  event_title=customtkinter.CTkLabel(master=window_frame, width=1, height=40, text=event_name, text_color="white", font=("CTkFont", 50), fg_color="#282828", bg_color="#282828")
  event_dmyt=customtkinter.CTkLabel(master=window_frame, width=1, height=10, text=f"- {day}/{month}/{year}, {time}", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_desc=customtkinter.CTkLabel(master=window_frame, width=1, height=200, text=span_multiple_lines(details), text_color="white", font=("CTkFont", 15), fg_color="#282828", bg_color="#282828")
  event_price=customtkinter.CTkLabel(master=window_frame, width=1, height=10, text=f"- Price to enter: £{correct_currency_format(price)}", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_location=customtkinter.CTkLabel(master=window_frame, width=1, height=10, text=f"- Location: {location}", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_title.place(x=50, y=100)
  event_dmyt.place(x=50, y=160)
  event_desc.place(x=60, y=190)
  event_price.place(x=60, y=400)
  event_location.place(x=60, y=430)
  load_event_registration_frame(event_name, player_cap, status)

def load_user_info_page(username): # COME BACK TO AFTER EVENT FINISHED HAS BEEN FULLY IMPLEMENTED
  kill_all_widgets()
  load_window()

  organiser, verified, first_name, bio, main_char, secondary_char, recent_event, recent_placement=database.user_details(username)
  user_title=customtkinter.CTkLabel(master=window_frame, width=1, height=40, text=username, text_color="white", font=("CTkFont", 50), fg_color="#282828", bg_color="#282828")
  user_verified=customtkinter.CTkLabel(master=window_frame, width=25, height=10, font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  if verified == 1:
    user_verified.configure(text="Verified", text_color="green")
  else:
    user_verified.configure(text="Unverified", text_color="red")
  user_first_name=customtkinter.CTkLabel(master=window_frame, width=1, height=10, text=first_name, text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  user_bio=customtkinter.CTkLabel(master=window_frame, width=1, height=200, text=span_multiple_lines(bio), text_color="white", font=("CTkFont", 15), fg_color="#282828", bg_color="#282828")
  user_main_char=customtkinter.CTkLabel(master=window_frame, width=1, height=10, text="Main character: N/A", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  user_main_char_image=customtkinter.CTkLabel(master=window_frame, width=25, height=25, bg_color="#282828", fg_color="#282828", text="")
  user_secondary_char=customtkinter.CTkLabel(master=window_frame, width=1, height=10, text="Secondary character: N/A", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  user_secondary_char_image=customtkinter.CTkLabel(master=window_frame, width=25, height=25, bg_color="#282828", fg_color="#282828", text="")
  if main_char is not None:
    user_main_char.configure(text=f"Main character:        {main_char}")
    user_main_char_image.configure(image=select_character_icon(main_char))
  if secondary_char is not None:
    user_secondary_char.configure(text=f"Secondary character:        {secondary_char}")
    user_secondary_char_image.configure(image=select_character_icon(secondary_char))
  if organiser==1:
    user_organiser=customtkinter.CTkLabel(master=window_frame, width=50, height=40, text="Organiser", text_color="yellow", font=("CTkFont", 30), fg_color="#282828", bg_color="#282828")
    user_organiser.place(x=1100, y=70)
  if username == sign_in_info.username:
    edit_account_button=customtkinter.CTkButton(master=window_frame, width=125, height=63, text="Edit Profile", bg_color="#282828", fg_color="white", border_width=1, border_color="black", text_color="black", hover_color="white", font=("CTkFont", 25), command=lambda: load_account_display_page(sign_in_info.username))
    edit_account_button.place(x=577, y=60)
  user_title.place(x=50, y=100)
  user_verified.place(x=60, y=160)
  user_first_name.place(x=60, y=200)
  user_bio.place(x=20, y=240)
  user_main_char.place(x=450, y=160)
  user_main_char_image.place(x=600, y=160)
  user_secondary_char.place(x=450, y=200)
  user_secondary_char_image.place(x=655, y=200)
  user_recent_event_frame=customtkinter.CTkFrame(master=window_frame, width= 580, height=268, border_width=1, border_color="white", bg_color="#282828", fg_color="#282828")
  user_recent_event_frame.place(x=0, y=452)
  recent_event=database.find_most_recently_participated_event(username)
  if recent_event is None:
    no_event_text=customtkinter.CTkLabel(master=user_recent_event_frame, width=570, height=200, text="No events to display.", text_color="white", font=("CTkFont", 50), fg_color="#282828", bg_color="#282828")
    no_event_text.place(x=5, y=34)
  else:
    user_recent_event_title=customtkinter.CTkLabel(master=user_recent_event_frame, width=570, height=40, text="Last event participated:", text_color="white", font=("CTkFont", 30), fg_color="#282828", bg_color="#282828")
    # ADD THE EVENT NAME AND THE USER'S PLACEMENT IN THE EVENT
    user_recent_event_title.place(x=5, y=5)

def load_account_settings_page(username):
  load_main_settings_page()
  recovery_email, password, recieve_email_notif=database.user_hidden_details(sign_in_info.id)

  edit_recovery_email_bar_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Recovery Email:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  edit_recovery_email_bar=customtkinter.CTkTextbox(master=window_frame, width=400, height=10, text_color="black", font=("CTkFont", 20), fg_color="white", bg_color="#282828")
  old_password_change_bar_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Original Password:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  old_password_change_bar=customtkinter.CTkTextbox(master=window_frame, width=250, height=10, text_color="black", font=("CTkFont", 20), fg_color="white", bg_color="#282828")
  password_change_bar_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="New Password:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  password_change_bar=customtkinter.CTkTextbox(master=window_frame, width=250, height=10, text_color="black", font=("CTkFont", 20), fg_color="white", bg_color="#282828")
  confirm_password_change_bar_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Confirm New Password:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  confirm_password_change_bar=customtkinter.CTkTextbox(master=window_frame, width=250, height=10, text_color="black", font=("CTkFont", 20), fg_color="white", bg_color="#282828")
  recieve_email_notif_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Recieve Email notifications regarding events:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  recieve_email_notif_switch=customtkinter.CTkSwitch(master=window_frame, width=100, height=50, text="", fg_color="white", bg_color="#282828", button_color="green", progress_color="green", button_hover_color="green")
  save_button=customtkinter.CTkButton(master=window_frame, width=125, height=50, text="Save", bg_color="#282828", fg_color="green", border_width=1, border_color="black", text_color="white", hover_color="green", font=("CTkFont", 25), command=lambda: attempt_save_account_settings(recovery_email, edit_recovery_email_bar.get(1.0, "end-1c"), password, old_password_change_bar.get(1.0, "end-1c"), password_change_bar.get(1.0, "end-1c"), confirm_password_change_bar.get(1.0, "end-1c"), int(recieve_email_notif_switch.get())))

  edit_recovery_email_bar_title.place(x=50, y=100)
  edit_recovery_email_bar.insert("0.0", hidden_email(recovery_email))
  edit_recovery_email_bar.place(x=60, y=130)
  old_password_change_bar_title.place(x=50, y=200)
  old_password_change_bar.place(x=60, y=230)
  password_change_bar_title.place(x=50, y=280)
  password_change_bar.place(x=60, y=310)
  confirm_password_change_bar_title.place(x=50, y=360)
  confirm_password_change_bar.place(x=60, y=390)
  recieve_email_notif_title.place(x=50, y=500)
  recieve_email_notif_switch.place(x=60, y=530)

  if recieve_email_notif==1:
    recieve_email_notif_switch.select()
  else:
    recieve_email_notif_switch.deselect()
  save_button.place(x=1145, y=100)

def load_account_display_page(username: str):
  load_main_settings_page()
  organiser, verified, first_name, bio, main_char, secondary_char, recent_event, recent_placement=database.user_details(username)
  user_title=customtkinter.CTkLabel(master=window_frame, width=1, height=40, text=username, text_color="white", font=("CTkFont", 50), fg_color="#282828", bg_color="#282828")
  user_verified=customtkinter.CTkLabel(master=window_frame, width=25, height=10, font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  if verified == 1:
    user_verified.configure(text="Verified", text_color="green")
  else:
    user_verified.configure(text="Unverified", text_color="red")
  edit_first_name_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="First Name:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  edit_first_name=customtkinter.CTkTextbox(master=window_frame, width=200, height=10, text_color="black", font=("CTkFont", 20), fg_color="white", bg_color="#282828")
  edit_bio_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Bio:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  edit_bio=customtkinter.CTkTextbox(master=window_frame, width=400, height=200, text_color="black", font=("CTkFont", 15), fg_color="white", bg_color="#282828")
  edit_main_char_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Main Character:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  edit_main_char=customtkinter.CTkOptionMenu(master=window_frame, width=1, height=10, text_color="black", font=("CTkFont", 20), fg_color="white", bg_color="#282828", button_color="white", button_hover_color="white", values=dict.character_list)
  edit_secondary_char_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Secondary Character:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  edit_secondary_char=customtkinter.CTkOptionMenu(master=window_frame, width=1, height=10, text_color="black", font=("CTkFont", 20), fg_color="white", bg_color="#282828", button_color="white", button_hover_color="white", values=dict.character_list)
  save_button=customtkinter.CTkButton(master=window_frame, width=125, height=50, text="Save", bg_color="#282828", fg_color="green", border_width=1, border_color="black", text_color="white", hover_color="green", font=("CTkFont", 25), command=lambda: attempt_save_account_display_info(edit_first_name.get(1.0, "end-1c"), edit_bio.get(1.0, "end-1c"), edit_main_char.get(), edit_secondary_char.get()))
  user_title.place(x=50, y=100)
  user_verified.place(x=60, y=160)
  edit_first_name_title.place(x=50, y=190)
  edit_first_name.insert("0.0",first_name)
  edit_first_name.place(x=60, y=220)
  edit_bio_title.place(x=50, y=270)
  edit_bio.insert("0.0",bio)
  edit_bio.place(x=20, y=300)
  edit_main_char_title.place(x=440, y=130)
  edit_main_char.set(main_char)
  edit_main_char.place(x=450, y=160)
  edit_secondary_char_title.place(x=440, y=200)
  edit_secondary_char.set(secondary_char)
  edit_secondary_char.place(x=450, y=230)
  save_button.place(x=1145, y=100)

def load_main_settings_page():
  kill_all_widgets()
  load_window()

  account_setting_segmented_button=customtkinter.CTkSegmentedButton(master=window_frame, width=1280, height=40, corner_radius=0, values=["Edit Profile", "Account Settings"], border_width=1, bg_color="#282828", fg_color="#282828", command=edit_segmented_button_selection)
  account_setting_segmented_button.place(x=0, y=50, relwidth=1)

def load_event_management_page():
  database.auto_change_event_status()
  kill_all_widgets()
  load_window()

  events_title=customtkinter.CTkLabel(master=window_frame, width=150, height=50, text="Active Events:", font=("CTkFont", 45), text_color="white", bg_color="#282828", fg_color="#282828")
  create_event_button=customtkinter.CTkButton(master=window_frame, width=567, height=60, corner_radius=5, bg_color="#282828", border_width=1, border_color="white", fg_color="#282828", hover_color="#282828", image=plus_image, text="Create an Event", text_color="white", command=load_create_event_page)
  events_list_frame=customtkinter.CTkScrollableFrame(master=window_frame, width=570, height=600, bg_color="#282828", border_color="#282828", fg_color="#282828")
  events_title.place(x=620, y=100)
  create_event_button.place(x=7, y=58)
  events_list_frame.place(x=0, y=120)

  results=database.search_active_events()
  for result in results:
    result_frame=customtkinter.CTkFrame(master=events_list_frame, width=570, height=100, bg_color="#282828", fg_color="#282828", border_width=1, border_color="white")
    result_title=customtkinter.CTkLabel(master=result_frame, width=100, height=25, corner_radius=10, text=(result[0]), bg_color="#282828", fg_color="#282828", text_color="white", font=("CTkFont", 40), anchor="w")
    result_details=customtkinter.CTkLabel(master=result_frame, width=100, height=40, bg_color="#282828", fg_color="#282828", text=f" - {result[1]}/{result[2]}/{result[3]}, {result[4]} \n - Held at {result[5]} \n - Caps at {result[6]} players \n - £{correct_currency_format(result[7])} entry fee", text_color="white", font=("CTkFont", 10), anchor="w")
    if result[8]==0:
      result_status=customtkinter.CTkLabel(master=result_frame, width=100, height=40, bg_color="#282828", fg_color="#282828", text="Not Started", text_color="red", font=("CTkFont", 15))
      result_edit_manage_button=customtkinter.CTkButton(master=result_frame, width=100, height=50, bg_color="#282828", fg_color="white", text="Edit Event", text_color="black", font=("CTkFont", 15), hover_color="white", command=lambda j=result[0]:load_edit_event_page(j))
    else:
      result_status=customtkinter.CTkLabel(master=result_frame, width=100, height=40, bg_color="#282828", fg_color="#282828", text="In Progress", text_color="yellow", font=("CTkFont", 15))
      result_edit_manage_button=customtkinter.CTkButton(master=result_frame, width=100, height=50, bg_color="#282828", fg_color="white", text="Manage Event", text_color="black", font=("CTkFont", 15), hover_color="white", command=lambda j=result[0]:load_event_matchup_page(j))
    result_frame.pack()
    result_title.place(x=5, y=5)
    result_details.place(x=5, y=50)
    result_status.place(x=300, y=30)
    result_edit_manage_button.place(x=450, y=25)

def load_create_event_page():
  kill_all_widgets()
  load_window()

  create_event_title=customtkinter.CTkLabel(master=window_frame, width=1, height=40, text="Create Event:", text_color="white", font=("CTkFont", 50), fg_color="#282828", bg_color="#282828")
  event_name_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Event Name:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_name=customtkinter.CTkEntry(master=window_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", text_color="black")
  event_desc_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Description:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_desc=customtkinter.CTkTextbox(master=window_frame, width=200, height=200, fg_color="white", border_color="white", bg_color="transparent", text_color="black")
  event_dmy_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Date:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_dmy_frame=customtkinter.CTkFrame(master=window_frame, width=225, height=50, bg_color="#282828")
  event_d=customtkinter.CTkOptionMenu(master=event_dmy_frame, width=50, height=50, bg_color="#282828", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.days)
  event_m=customtkinter.CTkOptionMenu(master=event_dmy_frame, width=50, height=50, bg_color="#282828", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.months)
  event_y=customtkinter.CTkOptionMenu(master=event_dmy_frame, width=50, height=50, bg_color="#282828", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.years)
  event_time_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Time:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_time_frame=customtkinter.CTkFrame(master=window_frame, width=150, height=50, bg_color="#282828")
  event_time_h=customtkinter.CTkOptionMenu(master=event_time_frame, width=50, height=50, bg_color="white", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.hours)
  event_time_m=customtkinter.CTkOptionMenu(master=event_time_frame, width=50, height=50, bg_color="white", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.minutes)
  global event_response_text
  event_response_text=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_price_text=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Price:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_price=customtkinter.CTkEntry(master=window_frame, width=200, height=30, fg_color="white", border_color="white", bg_color="transparent", text_color="black")
  event_location_text=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Location:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_location=customtkinter.CTkTextbox(master=window_frame, width=200, height=200, fg_color="white", border_color="white", bg_color="transparent", text_color="black")
  event_create_button=customtkinter.CTkButton(master=window_frame, width=100, height=75, bg_color="transparent", fg_color="white", text="Create", text_color="black", corner_radius=10, hover_color="white", command=lambda: begin_event_creation(event_name.get(), event_desc.get(1.0, "end-1c"), int(event_d.get()), int(event_m.get()), int(event_y.get()), (event_time_h.get()+":"+event_time_m.get()), event_price.get(), event_location.get(1.0, "end-1c")))

  create_event_title.place(x=50, y=100)
  event_name_title.place(x=50, y=175)
  event_name.place(x=60, y=195)
  event_desc_title.place(x=50, y=270)
  event_desc.place(x=60, y=290)
  event_dmy_title.place(x=305, y=175)
  event_dmy_frame.place(x=315, y=195)
  event_d.grid(row=0, column=0)
  event_m.grid(row=0, column=1)
  event_y.grid(row=0, column=2)
  event_time_title.place(x=305, y=300)
  event_time_frame.place(x=315, y=320)
  event_time_h.grid(row=0, column=0)
  event_time_m.grid(row=0, column=1)
  event_price_text.place(x=50, y=545)
  event_price.place(x=60, y=565)
  event_location_text.place(x=305, y=425)
  event_location.place(x=315, y=445)
  event_create_button.place(x=110, y=640)
  event_response_text.place(x=300, y=667)

def load_edit_event_page(event_name):
  kill_all_widgets()
  load_window()

  event_info=database.event_details(event_name)
  desc=event_info[0]
  day=str(event_info[1])
  month=str(event_info[2])
  year=str(event_info[3])
  minute=str(event_info[4])[3:]
  hour=str(event_info[4])[:2]
  location=event_info[5]

  edit_event_title=customtkinter.CTkLabel(master=window_frame, width=1, height=40, text="Edit Event:", text_color="white", font=("CTkFont", 50), fg_color="#282828", bg_color="#282828")
  event_desc_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Description:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_desc=customtkinter.CTkTextbox(master=window_frame, width=200, height=200, fg_color="white", border_color="white", bg_color="transparent", text_color="black")
  event_desc.insert("0.0",desc)
  event_dmy_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Date:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_dmy_frame=customtkinter.CTkFrame(master=window_frame, width=225, height=50, bg_color="#282828")
  event_d=customtkinter.CTkOptionMenu(master=event_dmy_frame, width=50, height=50, bg_color="#282828", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.days)
  event_d.set(day)
  event_m=customtkinter.CTkOptionMenu(master=event_dmy_frame, width=50, height=50, bg_color="#282828", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.months)
  event_m.set(month)
  event_y=customtkinter.CTkOptionMenu(master=event_dmy_frame, width=50, height=50, bg_color="#282828", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.years)
  event_y.set(year)
  event_time_title=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Time:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_time_frame=customtkinter.CTkFrame(master=window_frame, width=150, height=50, bg_color="#282828")
  event_time_h=customtkinter.CTkOptionMenu(master=event_time_frame, width=50, height=50, bg_color="white", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.hours)
  event_time_h.set(hour)
  event_time_m=customtkinter.CTkOptionMenu(master=event_time_frame, width=50, height=50, bg_color="white", fg_color="white", button_color="white", button_hover_color="white", dropdown_hover_color="grey", dropdown_fg_color="white", text_color="black", dropdown_text_color="black", values=database.minutes)
  event_time_m.set(minute)
  global edit_event_response_text
  edit_event_response_text=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_location_text=customtkinter.CTkLabel(master=window_frame, width=1, height=1, text="Location:", text_color="white", font=("CTkFont", 20), fg_color="#282828", bg_color="#282828")
  event_location=customtkinter.CTkTextbox(master=window_frame, width=200, height=200, fg_color="white", border_color="white", bg_color="transparent", text_color="black")
  event_location.insert("0.0",location)
  event_edit_button=customtkinter.CTkButton(master=window_frame, width=100, height=75, bg_color="transparent", fg_color="white", text="Edit", text_color="black", corner_radius=10, hover_color="white", command=lambda: attempt_event_edit(event_name, event_desc.get(1.0, "end-1c"), int(event_d.get()), int(event_m.get()), int(event_y.get()), (event_time_h.get()+":"+event_time_m.get()), event_location.get(1.0, "end-1c")))
  event_delete_button=customtkinter.CTkButton(master=window_frame, width=100, height=50, bg_color="transparent", fg_color="red", text="DELETE EVENT", text_color="white", corner_radius=10, hover_color="red", command=lambda: attempt_delete_event(event_name))

  edit_event_title.place(x=50, y=100)
  event_desc_title.place(x=50, y=175)
  event_desc.place(x=60, y=195)
  event_dmy_title.place(x=305, y=175)
  event_dmy_frame.place(x=315, y=195)
  event_d.grid(row=0, column=0)
  event_m.grid(row=0, column=1)
  event_y.grid(row=0, column=2)
  event_time_title.place(x=305, y=300)
  event_time_frame.place(x=315, y=320)
  event_time_h.grid(row=0, column=0)
  event_time_m.grid(row=0, column=1)
  event_location_text.place(x=50, y=450)
  event_location.place(x=60, y=470)
  event_edit_button.place(x=365, y=500)
  event_delete_button.place(x=1170, y=50)
  edit_event_response_text.place(x=400, y=667)
  
def load_event_matchup_page(event_name):
  players=database.display_players_in_event(event_name)
  kill_all_widgets()
  load_window()

  attendance_frame=customtkinter.CTkScrollableFrame(master=window_frame, width=500, height=670, bg_color="#282828", fg_color="#282828", scrollbar_button_color="white", scrollbar_button_hover_color="white", scrollbar_fg_color="#282828")
  attendance_frame.place(x=0, y=50)
  if players != []: # If at least 1 player has signed up for the event:
    for player in players:
      player_frame=customtkinter.CTkFrame(master=attendance_frame, width=500, height=110, corner_radius=0, fg_color="#282828", border_width=1, border_color="white")
      player_name=customtkinter.CTkLabel(master=player_frame, width=490, height=30, text=database.find_username_from_player_ID(player[0]), text_color="white", font=("CTkFont", 25))
      attendance_switch=customtkinter.CTkSwitch(master=player_frame, width=150, height=50, text="Is present?")
      attendance_switch.select() if player[1] == 1 else attendance_switch.deselect()
      attendance_switch.configure(command=lambda attendance_switch=attendance_switch, player=player: attendance_switch_toggle(attendance_switch.get(), player[0]))
      paid_switch=customtkinter.CTkSwitch(master=player_frame, width=150, height=50, text="Has paid?")
      paid_switch.select() if player[2] == 1 else paid_switch.deselect()
      paid_switch.configure(command=lambda paid_switch=paid_switch, player=player: paid_switch_toggle(paid_switch.get(), player[0]))
      player_frame.pack(pady=1)
      player_name.place(x=5, y=10)
      attendance_switch.place(x=67, y=55)
      paid_switch.place(x=284, y=55)
    attendance_paid_button=customtkinter.CTkButton(master=attendance_frame, width=150, height=75, text="Confirm", bg_color="#282828", fg_color="white", text_color="black", hover_color="white", font=("CTkFont", 20), command=lambda: continue_to_seeding(event_name))
    attendance_paid_button.pack(pady=19)

  else:
    no_players_text=customtkinter.CTkLabel(master=attendance_frame, width=300, height=100, text="No players have registered for this event.\n No further action is needed.", text_color="white", font=("CTkFont", 25))
    end_event_button=customtkinter.CTkButton(master=attendance_frame, width=150, height=75, text="End event", bg_color="#282828", fg_color="white", text_color="black", hover_color="white", font=("CTkFont", 20), command=lambda: attempt_end_event(event_name))
    no_players_text.pack()
    end_event_button.pack()

def continue_to_seeding(event_name):
  print("Seeding sub-screen")

load_home_screen()
#load_event_matchup_page("Test Event")
app.mainloop()
# IN PROGRESS - EVENT BRACKET SYSTEM (HIGHEST PRIORITY) - PLAYER CHECK COMPLETE, BEGIN SEEDING IN FUNCTION continue_to_seeding()

# UP NEXT:
# ADD NOTIFICATIONS FOR EVENT EDITS/DELETION FOR SIGNED UP USERS (MEDIUM PRIORITY)
# ADD ACCOUNT LOCKING SYSTEM FOR MULTIPLE FAILED ATTEMPTS (5) TO PREVENT BRUTE FORCE ACCOUNT ACCESS (LOW-MEDIUM PRIORITY)

