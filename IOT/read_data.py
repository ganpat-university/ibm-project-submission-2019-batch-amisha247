import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import smtplib
from email.message import EmailMessage
import time


def send_mail(msg__):
	email_address = "amishapatel19@gnu.ac.in"
	email_password = "yhteqewhzslqrkyr"
	
	# create email
	msg = EmailMessage()
	msg['Subject'] = "ALERT"
	msg['From'] = email_address
	msg['To'] = "amishapatel4966@gmail.com"
	msg.set_content(msg__)
	
	# send email
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(email_address, email_password)
		smtp.send_message(msg)
	
	time.sleep(3600)


cred = credentials.Certificate('fire_base.json')
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://ibm-project-g03-c4efd-default-rtdb.asia-southeast1.firebasedatabase.app'
})
ref = db.reference('/data')


ser = serial.Serial('COM5', 9600)

while True:
	line = ser.readline().decode('utf-8').rstrip()
	json_data = {
		'humidity': line.split('-')[0],
		'temperature': line.split('-')[1],
		'distance': line.split('-')[2]
	}
	ref.set(json_data)
	data = ref.get()
	print(data)
	if int(json_data['distance']) <= 20:
		send_mail('Your distance is less then 20. Current distance is '+json_data['distance'])

	

ser.close()
