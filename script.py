import smtplib
import getpass
import base64
import sys

from email.mime.text import MIMEText
from datetime import timedelta, date

import keyring  ## Install it `pip install keyring`, if you are using KWallet please see: https://github.com/jaraco/keyring#installation---linux

## Install it `pip install notify-run`, it's what make me send you the notifications
# from notify_run import Notify


def check_day():
    """Check for days, If date right and if not it will send emails.
    This will work like you open the app so it will check if it's today's date it will say you come tomorrow and if it's tomorrow's date it will ask you for password to add one more day and everything will be good but if its not today's or tomorrow's date it will send emails right away!"""

    ## Check if list "out of range" or in other words that file is empty it will set values to nothing to make you login
    contents = read_from_files("data.txt", "r")
    try:
        today_date = contents[1]
        tomorrow_date = contents[4]
        tomorrow_date_hash = contents[7]
    except IndexError:
        today_date = []
        tomorrow_date = []
        tomorrow_date_hash = []

    ## Check for the date as i said above!
    if today_date == str(date.today()):
        input(
            "\n\nYou already checked today, Please come tomorrow!\n\n(Press Enter To Leave!)\n\n"
        )
        sys.exit(0)

    elif tomorrow_date == str(date.today()) and tomorrow_date_hash == str(encrypt_date(date.today())):
        login()

    elif today_date == [] and tomorrow_date == [] and tomorrow_date_hash == []:
        login()

    else:
        send_email()
        sys.exit(0)


def login():
    """This Function check for password and password saved in your keyring so do not worry!"""
    def retry_password():
        for _ in range(3):
            user_password_again = getpass.getpass(
                "Password is wrong, please try again (it's case sensitive): "
            )
            if user_password_again == user_password():
                add_day()
                return True
            if user_password_again.lower() == "exit":
                sys.exit(0)

    user_password_input = getpass.getpass(
        "Please type your password(or `exit` to leave or press ctrl + c): "
    )  ## Here is your password. If it's right you will be able to login to add tomorrow's date

    if user_password_input == user_password():
        add_day()

    elif user_password_input.lower() == "exit":
        sys.exit(0)

    elif user_password_input != user_password():
        if not retry_password():
            send_email()
            sys.exit(0)


def user_password():
    """This function to add your password in keyring incase if its not"""

    app_name = "Dead Man Swtich APP"
    user_name = (
        getpass.getuser()
    )  ##Gets your username, you not need it actually it just to know for which user password is set

    ## If password not found in your keyring it will ask you to add one
    if keyring.get_password(app_name, user_name) is None:
        user_password_input = input(
            "I assume it's your first time here so please add your password(first time only and it's case sensitive): "
        )
        keyring.set_password(app_name, user_name, user_password_input)

    return keyring.get_password(app_name, user_name)


def add_day():
    """This function add the tomorrow's date into the data file"""

    write_to_files(
        "data.txt",
        "w",
        "Today Date: "
        + "\n"
        + str(date.today())
        + "\n\n"
        + "Tomorrow Date: "
        + "\n"
        + str(date.today() + timedelta(days=1))
        + "\n\n"
        + "Tomorrow Hash: "
        + "\n"
        + str(encrypt_date(date.today() + timedelta(days=1))),
    )

    input(
        "\n\nGlad to hear that you are alive!\ncome back tomorrow!\n\n(Press Enter To Leave!)\n\n"
    )

    ## Use this code if you want to "decrypt" the base64, for me i not need it --until now--
    # decrypt = base64.decodebytes(today_date)
    # decrypt2 = base64.decodebytes(end_date)


def encrypt_date(data):
    """This function converts the tomorrow's date into base64 as kind of hash to ensure no one played in the dates"""

    day = str(data)
    day_date = day.encode("utf-8")
    encrypt = base64.b64encode(day_date)
    return encrypt.decode("utf-8")


def read_from_files(filename, accessmode):
    """This function read from data file to get data and work"""

    try:
        with open(filename, accessmode) as name:
            return name.read().splitlines()
    except FileNotFoundError:
        print("Please create file {}".format(filename))
        sys.exit(0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def write_to_files(filename, accessmode, data):
    """This function write to files the data"""

    try:
        with open(filename, accessmode) as file:
            file.write(data)
    except OSError:
        print("Encountered a problem trying to write {}".format(filename))
        sys.exit(0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def send_email():
    """This function send emails to people"""

    print("\n\nSeems you dead, RIP i'm going to send emails now\n\n")

    mailserver = smtplib.SMTP(
        "smtp.gmail.com", 587
    )  ##You can change SMTP to your email's one, just ask their support! and type your login data as it's same as you just login with their login page
    mailserver.starttls()
    mailserver.login(
        "YOUR_EMAIL@gmail.com", "YOUR_PASSWORD"
    )  ##Type your email and password here to login
    mailserver.set_debuglevel(1)
    msg = MIMEText(
        """BODY OF THE EMAIL (The message)""", "plain"
    )  ##Type your message here and Change "plain" to "html" (with quotes) if you want to type HTML email instead!

    ## An example of HTML email and you could use https://html5-editor.net/ as help if you do not know HTML

    # msg = MIMEText("""\
    #     <html>
    #     <head></head>
    #     <body>
    #         <p>Hi!<br>
    #         How are you?<br>
    #         Here is the <a href="http://www.python.org">link</a> you wanted.
    #         </p>
    #     </body>
    #     </html>
    #     """, 'html')

    sender = "YOUR_EMAIL@gmail.com"  ##Type your email again or your name/username
    recipients = [
        "YOUR_Friend@gmail.com",
        "Your_Family@hotmail.com",
        "Your_Teacher@yahoo.com",
    ]  ##type people to send them the email here
    msg["Subject"] = "SUBJECT OF THE EMAIL (The Title/Name)"  ##subject of the email
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    mailserver.sendmail(sender, recipients, msg.as_string())

    print("\n\nEmail(s), Sent!")
    sys.exit(0)


## Enable it when you are on phone, due its useless on PC because script run on startup only but on phone it will be run most of time
## To make it works, install it inside your termux type `pip install notify-run` then type `notify-run register` and go to link and subscribe inside your browser and keep it open whole day (the borwser and the script)

# def notify_repeter():
#     """This function keep repeating and send notifications"""

#     starttime = time.time()
#     while True:
#         notify = Notify()
#         notify.send('Dead Man\'s Switch App\nDo not forget to Check Your Dead Man\'s switch app')
#         time.sleep(21600.0 - ((time.time() - starttime) % 60.0)) ## Time in seconds, it will repeat every 6 hours


# def notify_thereder():
#     """This is the thread function to keep notifications work in background"""

#     notify_thread = threading.Thread(target=notify_repeter)
#     notify_thread.start()


## Start Notifications System
# notify_thereder()

## Start the app
check_day()
