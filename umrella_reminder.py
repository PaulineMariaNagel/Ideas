# -*- coding: utf-8 -*-
"""
@author: pauline
"""

"""
Daily Umbrella Reminder Script 
-> checks weather forecast for location using the free Open-Meteo API
-> Checks if rain is actually expected today
-> Emails meso I don't forget my umbrella
"""

from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
import requests


# Coordinates for my location (in my case salzburg)
LATITUDE = 47.2692
LONGITUDE = 11.4041

# Email (make sure to use app password if using gmail, dont know how to make this differently)
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"


def check_weather_and_notify():
  print("Checking what the sky looks like today...")

  # free weather forecast
  url = (
      f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude="
      f"{LONGITUDE}&daily=precipitation_probability_max,rain_sum&timezone=auto"
  )

  try:
    response = requests.get(url)
    data = response.json()

    # takes the max rain probability and total expected rain for today 
    max_rain_prob = data["daily"]["precipitation_probability_max"][0]
    total_rain = data["daily"]["rain_sum"][0]

    print(
        f"Today's max rain probability: {max_rain_prob}% (Expected rain:"
        f" {total_rain} mm)"
    )

    # Simple logic: If there's a decent chance of rain (> 40%) or actual rain expected
    if max_rain_prob > 40 or total_rain > 0.5:
      message = (
          f"Good morning! ☔\n\nLooks like rain today. Probability is at"
          f" {max_rain_prob}% (around {total_rain} mm expected).\nBetter grab"
          f" an umbrella before you leave!"
      )
      send_email("Umbrella Alert! ☂️", message)
    else:
      print("No umbrella needed today. Staying dry!")

  except Exception as e:
    print(f"Oops, something went wrong while cheking the weather: {e}")


def send_email(subject, body):
  msg = EmailMessage()
  msg.set_content(body)
  msg["Subject"] = subject
  msg["From"] = SENDER_EMAIL
  msg["To"] = RECEIVER_EMAIL

  # check again if it works
  try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
      smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
      smtp.send_message(msg)
    print("Umbrella reminder email sent successfully!")
  except Exception as e:
    print(f"Failed to send email: {e}")


if __name__ == "__main__":
  check_weather_and_notify()
