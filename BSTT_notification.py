import BSTT_SQLite_DB as database
import os
import discord
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import dotenv_values
env=dotenv_values("var.env")

SENDER_EMAIL=(env["SENDER_EMAIL"])
SENDER_PWORD=(env["SENDER_PWORD"])
DISCORD_TOKEN=(env["DISCORD_TOKEN"])

#SENDER_EMAIL=str(os.getenv("SENDER_EMAIL"))
#DISCORD_TOKEN=str(os.getenv("DISCORD_TOKEN"))

def verification_email(rec_email, rec_username, verification_code):
  result=False
  server = smtplib.SMTP("smtp.outlook.com", 587)
  message = 'Subject: {}\n\n{}'.format(f'Your Verification Code is {verification_code}.', (f'Hi {rec_username}, \n\n Here is your verification code: \n\n\n {verification_code} \n\n\n To finish creating your account, please enter this code into the Enter Verification Code window that should appear on your device. \n\n If you did not request this code, you can safely ignore this E-Mail.'))
  try:
    server.starttls()
  except Exception:
    response="An error occurred while attempting to send a verification code. Please try again."
    print("An error occurred while connecting to the server. Please try again.")
  else:
    print("Connected to server.")
  try:
    server.login(SENDER_EMAIL, SENDER_PWORD) # type: ignore
  except Exception as e:
    response="An error occurred while attempting to send a verification code. Please try again."
    print("An error occurred while signing into Outlook. Please ensure the email and password for BSTT's no reply email are valid.")
    print (e)
  else:
    print("Sign-in successful.")
    try:
      server.sendmail(SENDER_EMAIL, rec_email, message) # type: ignore
    except Exception as e:
      print(f"Failed to send E-mail to {rec_email}. \n {e}")
      response=(f"Failed to send E-mail to {rec_email}. Please ensure this is a valid email and try again.")
    else:
      result=True
      response="Check your email to continue."
      print("E-mail sent successfully.")
    server.quit
  return result, response

def email_event_notification(event_name_f: str):
  
  server = smtplib.SMTP("smtp.outlook.com", 587)
  failed_list = []
  print("Sending email notifications...")
  try:
    server.starttls()
  except Exception:
    print("An error occurred while connecting to the server. Please try again.")
  else:
    print("Connected to server.")
  try:
    server.login(SENDER_EMAIL, SENDER_PWORD) # type: ignore
  except Exception as e:
    print("An error occurred while signing into Outlook. Please ensure the email address and password are correct and try again.")
    print (e)
  else:
    print("Sign-in successful.")
    notifiable_users=database.find_email_notifiable_users()
    for rec_email in notifiable_users:
      rec_username=database.find_username_from_email(rec_email[0])
      message = 'Subject: {}\n\n{}'.format('A new tournament has been created!', (f'Hi {rec_username}, \n\n Registration for {event_name_f} is now open! To register, please check the BSTT app. \n\n\n\n\n This E-mail was sent to you because you have opted to receive notifications for tournament creations. To opt out, disable "Receive E-mail notifications" in your account settings.'))
      try:
        server.sendmail(SENDER_EMAIL, rec_email, message) # type: ignore
      except Exception :
        failed_list.append(rec_email)
    if len(failed_list) >= 1:
      print(f"Failed to send E-mails to these addresses: \n {failed_list}")
    else:
      print("All E-mails sent successfully.")
    server.quit

def send_event_notification(event_name_f: str):
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)
  global event_name
  event_name=event_name_f

  email_event_notification(event_name)

  @client.event
  async def on_ready():
    print("Sending discord notification...")
    channel = client.get_channel(1125381928036614216)
    await channel.send(f"@everyone Registration for {event_name} is open! Check it out on BSTT.") # type: ignore
    print("Discord notification sent! Closing connection.")
    await client.close()
    

  try:
    client.run(DISCORD_TOKEN) # type: ignore
  except Exception as e:
    print(f"An error has occurred. Please try again later.\n {e}")