#
#	Main source code for the QuickRegistration Project.
#		
#	Author: Jari Naeser, 2022
#

# ----------------- Imports -----------------

import mysql.connector as database
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import RPi_I2C_driver

# ----------------- Pin configuration -----------------

BuzzerPin = 37
rgbRedPin = 7
rgbGreenPin = 13
rgbBluePin = 11

# ----------------- Other variables configuration -----------------

db_username = 'root'
db_password = 'root'

buzzerState = False
# initialize LCD screen
lcdScreen = RPi_I2C_driver.lcd()
# initialize rfc reader
rfcReader = SimpleMFRC522()
rgbIntensity = 30
isRunning = True

# Create database connection
connection = database.connect(
	user=db_username,
	password=db_password,
	host="localhost",
	database="QuickRegistrationDB")

# Create database cursor
cursor = connection.cursor()

# ----------------- GPIO configuration -----------------

# Use Board Layout to map pins
GPIO.setmode(GPIO.BOARD)
# Buzzer
GPIO.setup(BuzzerPin, GPIO.OUT)
# RGB led
GPIO.setup(rgbRedPin, GPIO.OUT)
GPIO.setup(rgbGreenPin, GPIO.OUT)
GPIO.setup(rgbBluePin, GPIO.OUT)

# Setup rgb led intensity
RGB_RED = GPIO.PWM(rgbRedPin, rgbIntensity)
RGB_GREEN = GPIO.PWM(rgbGreenPin, rgbIntensity)
RGB_BLUE = GPIO.PWM(rgbBluePin, rgbIntensity)

# ----------------- DB Functions -----------------

def registerUser(cardId, userData):
	try:
		statement = "INSERT INTO registeredUsers (cardId, userData, registeredAt) VALUES (%s, %s, NOW());"
		data = (cardId, userData)
		cursor.execute(statement, data)
		connection.commit()
		print("DB: Successfully registered user " + userData)

		userHasRegistered()
	except database.Error as e:
		print(f"DB: Error while registering user " + userData + ": {e}")

def getUsersWithAccess():
	try:
		statement = "SELECT * FROM usersWithAccess;"

		cursor.execute(statement)
		return cursor.fetchall()

	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")

def isUserAlreadyRegistered(cardId):
	try:
		statement = "SELECT * FROM registeredUsers WHERE cardId LIKE '" + str(cardId) + "';"
		
		cursor.execute(statement)
		results = cursor.fetchone()

		return results != None and results[0] == cardId
		
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")

def getUserWithAccess(cardId):
	try:
		statement = "SELECT * FROM usersWithAccess WHERE cardId LIKE '" + str(cardId) + "';"
		
		cursor.execute(statement)
		return cursor.fetchone()
		
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")

# ----------------- QuickRegistration Functions -----------------

def setRgbColor(red = 0, green = 0, blue = 0):
	# With GPIO.PWM the parameter goes from 0 to 100, therefore divide by 2.55
	RGB_RED.start(red/2.55)
	RGB_GREEN.start(green/2.55)
	RGB_BLUE.start(blue/2.55)

def setLCDText(text, row):
	lcdScreen.lcd_display_string(text, row)

def initComponents():
	# Set buzzer state to low to avoid it making sounds
	GPIO.output(BuzzerPin, 0);
	#Turn off led
	setRgbColor(0,0,0);
	#Lcd screen
	setLCDText("--------------------", 1)
	setLCDText("|      Welcome     |", 2)
	setLCDText("|         :)       |", 3)
	setLCDText("--------------------", 4)

def showDefaultMessage():
	setLCDText("  M-E5110Z GUA/RIV  ", 1)
	setLCDText("  Sistemi Embedded  ", 2)
	setLCDText("                    ", 3)
	setLCDText("Appoggia la tessera ", 4)

def userNotFound():
	# LCD feedback
	setLCDText("       ERRORE       ", 1)
	setLCDText("                    ", 2)
	setLCDText(" Non sei registrato ", 3)
	setLCDText("     nel corso.     ", 4)
	# LED feedback
	setRgbColor(255, 0, 0)
	# Buzzer feedback
	GPIO.output(BuzzerPin, 1);

	time.sleep(1)
	GPIO.output(BuzzerPin, 0);
	time.sleep(4)
	setRgbColor(0, 0, 0)

def showError():
	# LCD feedback
	setLCDText("       ERRORE       ", 1)
	setLCDText("                    ", 2)
	setLCDText("  I dati rilevati   ", 3)
	setLCDText("  non sono idonei.  ", 4)
	# LED feedback
	setRgbColor(255, 0, 0)
	# Buzzer feedback -> long beep
	GPIO.output(BuzzerPin, 1);

	time.sleep(1)
	GPIO.output(BuzzerPin, 0);
	time.sleep(4)
	setRgbColor(0, 0, 0)

def userAlreadyRegistered():
	# LCD feedback
	setLCDText("       AVVISO       ", 1)
	setLCDText("                    ", 2)
	setLCDText(" Hai gia registrato ", 3)
	setLCDText("  la tua presenza.  ", 4)
	# LED feedback
	setRgbColor(0, 0, 255)
	# Buzzer feedback -> Beep Beep Beep
	GPIO.output(BuzzerPin, 1);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 0);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 1);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 0);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 1);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 0);

	time.sleep(4.5)
	setRgbColor(0, 0, 0)

def userHasRegistered():
	# LCD feedback
	setLCDText("      SUCCESSO      ", 1)
	setLCDText("                    ", 2)
	setLCDText(" La tua presenza e  ", 3)							
	setLCDText(" stata registrata.  ", 4)
	# LED feedback
	setRgbColor(0, 255, 0)
	# Buzzer feedback -> Beep Beep	
	GPIO.output(BuzzerPin, 1);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 0);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 1);
	time.sleep(0.1)
	GPIO.output(BuzzerPin, 0);

	time.sleep(4.7)
	setRgbColor(0, 0, 0)

# ----------------- Main -----------------

def main():
	global isRunning
	id = None

	usersWithCourseAccess = getUsersWithAccess();
	initComponents();

	try:
		while isRunning:
			showDefaultMessage();

			id = str(rfcReader.read_id());
			user = getUserWithAccess(id)

			if(user):
				if(isUserAlreadyRegistered(id)):
					#User already registered
					userAlreadyRegistered()
				else:
					#User still has to be registered
					if(user[0] and user[1]):
						registerUser(user[0], user[1])
					else:
						showError()
			else:
				userNotFound()

	except KeyboardInterrupt:
		isRunning = False
		# Reset display content
		lcdScreen.lcd_clear()
		# Turn off screen
		lcdScreen.backlight(0)
		GPIO.cleanup()
		# Close database connection
		connection.close()

# ----------------- Program -----------------

#Runs entire program
main()