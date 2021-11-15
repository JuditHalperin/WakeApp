
import smtplib
import ssl
import os


os. chdir(os.getcwd().replace("\\", "/").replace("Scripts", ""))  # set working directory

driver_name = "Dan"

contact_name = "Yudit"
contact_email = "yudithalperin@gmail.com"

sender_email = "driver.drowsiness.detection.mail@gmail.com"
sender_password = "0586169890"

message = open("Data/mail_message.txt").read().replace("CONTACT_NAME", contact_name).replace("DRIVER_NAME", driver_name)

with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=ssl.create_default_context()) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, contact_email, message)
