import json
import os

class User:
    def __init__(self, user_id, desigred_model):
        self.user_id = user_id
        self.file_path= self.user_id + ".json"
        self.desigred_model = desigred_model
        create_file =self.blank_file()

    def check_existance(self):
        if self.file_path not in os.listdir():
            return False

    def blank_file(self):
        if self.check_existance() == False:
            # Update the data with the new user information
            x= 'you'
            y= 'me'

            data = {
                "user_id": x,
                "Desired_model": y
            }

            with open(self.file_path, 'w') as file:
                json.dump(data, file)


    def save_new_user(self):
        # Update the data with the new user information
        data = {
            "user_id": self.user_id,
            "Desired_model": self.desigred_model
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def check_data_existence(self):
        """Check if the user ID and the desired model already exist in the data"""
        file_path = self.file_path
        with open(file_path, "r") as file:
            file_data = json.load(file)
            if file_data["user_id"] == self.user_id and file_data["Desired_model"] == self.desigred_model:
                return True
        return False

    def check_user_existence(self):
        """Check if the user ID already exist in the data"""
        file_path = self.file_path
        with open(file_path, "r") as file:
            file_data = json.load(file)
            if file_data["user_id"] == self.user_id:
                return True
        return False

    def update_user_data(self):
        """Update the user data with the new desired model"""
        file_path = self.file_path
        data = self.load_user_data()
        # Check if the user ID already exists in the data
        if self.user_id in data['user_id']:
            # Update the existing field
            data["Desired_model"] = self.desigred_model
            with open(file_path, "w") as file:
                json.dump(data, file)
        else:
            pass

    

    def load_user_data(self):
        """Load the user data"""
        file_path = self.file_path
        with open(file_path, "r") as file:
            data = json.load(file)
            return data






def check_json_file_existence(user_id):
    """Check if the json file exists """
    user_id = user_id + ".json"
    if user_id not in os.listdir():
        return False
    else:
        return True














# # Define a function to save data to the file
# def save_user_data(user_id, desigred_model):
#     data = {
#         "user_id": user_id,
#         "Desigred_model": desigred_model
#     }
    
#     with open("user_data.json", "w") as file:
#         json.dump(data, file)

# def update_user_data(user_id, desigred_model):
#     file_path = "user_data.json"

#     with open(file_path, "r") as file:
#         data = json.load(file)
#         print(data)

#     # Check if the user ID already exists in the data
#     if user_id in data.keys():
#         # Update the existing field
#         data[user_id]["Desigred_model"] = desigred_model
#         print(data)
#         with open(file_path, "w") as file:
#             json.dump(data, file)

#     else:
#         pass

    

# def check_data_existence(data1, data2):
#     file_path = "user_data.json"
#     with open(file_path, "r") as file:
#         file_data = json.load(file)
#         if file_data["user_id"] == data1 and file_data["Desigred_model"] == data2:
#             return True
#     return False

# def check_user_existence(data1):
#     file_path = "user_data.json"
#     with open(file_path, "r") as file:
#         file_data = json.load(file)
#         if file_data["user_id"] == data1:
#             return True
#     return False


# # Define a function to load data from the file
# def load_user_data():
#     try:
#         with open("user_data.json", "r") as file:
#             data = json.load(file)
#             return data
#     except FileNotFoundError:
#         return None



