import PySimpleGUI as sg
import json 
import os 
from json_user import User,check_json_file_existence
import subprocess

sg.theme("DarkAmber")   

# Define the layout of the GUI
layout = [
    [sg.Text("User ID:"), sg.Input(key="-USERID-")],
    [sg.Text("Model Name:"), sg.Input(key="-MODELNAME-")],
    [sg.Button("Save"), sg.Button("Train"), sg.Button("Execute"), sg.Button("Exit")]
]

# Create the window
window = sg.Window("Deep Learning App", layout)

# Event loop to process GUI events
while True:
    event, values = window.read()

    # Exit the application if the window is closed or "Exit" button is clicked
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    # Handle different button clicks
    if event == "Save":
        user_id = values["-USERID-"]
        model_name = values["-MODELNAME-"]
        model_name = model_name + ".pt"
        proceed = True  # Flag variable to control flow
        
        base_user = User(user_id=user_id, desigred_model=model_name)
        
        if not os.path.exists(model_name):
            sg.popup("Model does not exist")
            proceed = False
        
        if proceed and base_user.check_data_existence():
            sg.popup(f"Model data already exists.Thank you for using our app")
        elif proceed and base_user.check_user_existence():
            choice = sg.popup_yes_no('User already exists, do you want to update the model name?')
            if choice == 'Yes':
                base_user.update_user_data()
                sg.popup(f"Model data has been updated")
        elif proceed and not base_user.check_user_existence():
            choice = sg.popup_yes_no('User does not exist, do you want to create a new user?')
            if choice == 'Yes':
                base_user.save_new_user()
                sg.popup(f"Model data has been updated")
        else:
            choice=sg.popup_yes_no('No pretrained model found do you want to train a fresh  model?')
            if choice == 'Yes':
                base_user.save_new_user()
                sg.popup(f"Use train button to train the model\n reload the app to  the model")


        

    elif event == "Train":
        user_id = values["-USERID-"]
        model_name = values["-MODELNAME-"]
        model_name = model_name + ".pt"
        base_user = User(user_id=user_id, desigred_model=model_name)
        if base_user.check_data_existence():
            choice = sg.popup_yes_no('Do you want to train the model?')
            if choice == 'Yes':
                subprocess.call(["python", "train.py", user_id, model_name])
                sg.popup(f"Model training Commpeted")

        else:
            sg.popup('Please first use the save button and save your data ')



    elif event == "Execute":
        user_id = values["-USERID-"]
        model_name = values["-MODELNAME-"]
        model_name = model_name + ".pt"
        base_user = User(user_id=user_id, desigred_model=model_name)
        
        proceed = True  # Initialize proceed with a default value
        
        if not os.path.exists(model_name):
            sg.popup("Model does not exist")
            proceed = False
        
        if proceed and base_user.check_data_existence():
            choice = sg.popup_yes_no('Do you want to execute the model?')
            if choice == 'Yes':
                subprocess.call(["python", "program_exe.py", user_id, model_name])
                sg.popup(f"sir please user the same user id and model name to execute that model")
        else:
            sg.popup(f"Please first create an ID and train the model")


    # Close the window
    window.close()
