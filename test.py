import customtkinter
import asyncio
from bleak import BleakScanner
import requests
import json
import threading
from main import multilaterate

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

login_frame = customtkinter.CTk()
login_frame.geometry("600x350")

device_list = []
token = None
student_id_encrypted = None


async def main():
    devices = await BleakScanner.discover(timeout=10.0)
    for d in devices:
        device_list.append([d.address, d.rssi])


def login():
    student_id = entry1.get().strip()
    student_password = entry2.get().strip()

    # print((student_id))
    # print((student_password))

    if student_id and student_password:
        try:
            response_code = validate_login(student_id, student_password)
            # response_code = 200
            if response_code == 200:
                entry1.destroy()
                entry2.destroy()
                button.destroy()
                button1.pack(pady=12, padx=10)
                button2.pack(pady=12, padx=10)

        except ValueError:
            pass


def validate_login(student_id, password):
    global token
    global student_id_encrypted
    url = 'https://capstonebackend.fly.dev/auth/signin'
    header = {
        'Content-Type': 'application/json'}
    payload_data = json.dumps({
        "password": password,
        "studentID": student_id
    })

    response = requests.post(url, headers=header, data=payload_data)

    if response.status_code == 200:
        login_success_message.pack()
        login_success_message.after(3000, login_success_message.destroy)
        response_dictionary = json.loads(response.text)
        print(response_dictionary)
        token = response_dictionary['token']
        student_id_encrypted = response_dictionary['user']['_id']
    else:
        login_error_message.pack()
        login_error_message.after(3000, login_error_message.destroy)
    return response.status_code


def raise_hand():
    url = "https://capstonebackend.fly.dev/set/raise_hand"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    payload = json.dumps({
        "course_id": "63e3e57dc347381e72c419e5",
        "student_id": student_id_encrypted,
        "hand_raised": True
    })

    response = requests.put(url, headers=headers, data=payload)

    print(response.status_code)


def scan():
    # print(token)
    url = "https://capstonebackend.fly.dev/set/student_position"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    scanning_message.pack()
    progress_bar.pack(pady=12, padx=10)
    progress_bar.start()
    progress_bar.step()
    asyncio.run(main())
    scanning_message.destroy()
    scanning_success.pack()
    scanning_success.after(3000, scanning_success.destroy)
    progress_bar.stop()
    progress_bar.destroy()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # print(device_list)

    if device_list:
        # location_x, location_y = multilaterate(device_list)
        location_x, location_y = 25, 125
        payload = json.dumps({
            "course_id": "63e3e57dc347381e72c419e5",
            "x_position": location_x,
            "y_position": location_y
        })

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            button1.destroy()
        else:
            error_message.pack()
            error_message.after(3000, error_message.destroy)

# frame = customtkinter.CTkFrame(master=login_frame)
# frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=login_frame, text="Login", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Student ID")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=login_frame, text="Login", command=login)
button.pack(pady=12, padx=10)

button1 = customtkinter.CTkButton(master=login_frame, text="Scan", command=threading.Thread(target=scan).start)
button2 = customtkinter.CTkButton(master=login_frame, text="Raise Hand", command=raise_hand)

login_error_message = customtkinter.CTkLabel(master=login_frame, text="Login Error!\nPlease make sure you are using a valid ID and password")
login_success_message = customtkinter.CTkLabel(master=login_frame, text="Succesfully logged in!")
scanning_message = customtkinter.CTkLabel(master=login_frame, text="Scanning...")
scanning_success = customtkinter.CTkLabel(master=login_frame, text="Finished scanning!")
error_message = customtkinter.CTkLabel(master=login_frame, text="Scan error! Position not found. \n Please check Bluetooth, Internet, and an active class are available")

progress_bar = customtkinter.CTkProgressBar(login_frame, orientation='horizontal', mode='indeterminate')


login_frame.mainloop()
