import customtkinter
from customtkinter import *
import asyncio
from bleak import BleakScanner
from tkinter import messagebox
import requests
import json
from main import multilaterate

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

login_frame = customtkinter.CTk()
login_frame.geometry("600x350")

device_list = []

url = "https://capstonebackend.fly.dev/set/student_position"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                     '.eyJfaWQiOiI2Mzg2OWUwMGVmM2NiNzQ3NWFmNDgyZjUiLCJpYXQiOjE2NzU4Nzg3Mzl9'
                     '.o61yOrLGb9ghXZe1ZsjmkdnBuoiuo0hjp6dDH_wGQ_M '
}


async def main():
    devices = await BleakScanner.discover(timeout=10.0)
    for d in devices:
        device_list.append([d.address, d.rssi])


def validate_login(id, password):
    url = "https://capstonebackend.fly.dev/auth/signin"

    payload = json.dumps({
        "studentID": id,
        "password": password
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code


def question():
    pass


def scan():
    student_id = entry1.get()
    student_password = entry2.get()

    if student_id and student_password:
        try:
            student_id = int(student_id)

            response_code = validate_login(student_id, student_password)
            response_code = 200
            if response_code == 200:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
                print(device_list)

                if device_list:
                    entry1.pack_forget()
                    entry2.pack_forget()
                    button1.pack(pady=12, padx=10)

                    location_x, location_y = multilaterate(device_list)
                    payload = json.dumps({
                        "course_id": "63e3e57dc347381e72c419e5",
                        "x_position": location_x,
                        "y_position": location_y
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                    print(response.text)

        except ValueError:
            pass


frame = customtkinter.CTkFrame(master=login_frame)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Student ID")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=login_frame, text="Scan", command=scan)
button.pack(pady=12, padx=10)

button1 = customtkinter.CTkButton(master=login_frame, text="Raise Hand", command=question)

login_frame.mainloop()
