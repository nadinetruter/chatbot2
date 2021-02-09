import json
import random
import requests
from datetime import datetime

url = "http://127.0.0.1:5000/api/"

userdata_to_create = [
    {
        "user": ("orange@gmail.com", "tomato"),
        "patients": [
            ("Jesse", "Boise", "male", "1602316430082", {
                "street_name": "Fly Street",
                "house_number": 15,
                "city": "Cape Town",
                "country": "South Africa",
                "postal_code": "7530"
            }, "0185249836"),
            ("Adam", "Banderker", "male", "1208032185082", {
                "street_name": "Wimbledon Street",
                "house_number": 4,
                "city": "Cape Town",
                "country": "South Africa",
                "postal_code": "7530"
            }, "0865001215"),
        ],
        "appointments": [
            ("General", "Stomach Bug"),
            ("Semi-private", "COVID-19")
        ]
    },
    {
        "user": ("tomato@gmail.com", "tomato"),
        "patients": [
            ("Kauthar", "Carelse", "female", "0214523248083", {
                "street_name": "Apache Way",
                "house_number": 256,
                "city": "Johannesburg",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0336578746"),
            ("Tinashi", "Muneri", "male", "0331120458082", {
                "street_name": "Alonzo Street",
                "house_number": 88,
                "city": "Pretoria",
                "country": "South Africa",
                "postal_code": "5555"
            }, "0155466897"),
        ],
        "appointments": [
            ("General", "Diabetes"),
            ("Private", "Heart Attack")
        ]
    }
]
admindata_to_create = [
    {
        "user": ("Oreo", "oreo@gmail.com", "oreo"),
        "admins": [
            ("Orange", "Juice", "male", "8101015800087", {
                "street_name": "Slim Street",
                "house_number": 12,
                "city": "Johannesburg",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0765559187"),
            ("Grape", "Juice", "male", "2001015800085", {
                "street_name": "Alto Avenue",
                "house_number": 1,
                "city": "Port Elizabeth",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0811555598"),
        ],
        "hospitals": [
            ("Groote Schuur Hospital", [-33.94081566091405, 18.4616755829101]),
            ("Melomed Bellville Private Hospital",
             [-33.901385762815195, 18.624403298254883])
        ]
    },
    {
        "user": ("Chocolate", "chocolate@gmail.com", "choolate"),
        "admins": [
            ("Mango", "Juice", "female", "3605034800089", {
                "street_name": "Apache Way",
                "house_number": 14,
                "city": "Port Elizabeth",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0725555144"),
            ("Apple", "Juice", "male", "3401015800086", {
                "street_name": "Michael Way",
                "house_number": 13,
                "city": "Johannesburg",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0555700552"),
        ],
        "hospitals": [
            ("Karl Bremer Hospital",
             [-33.891870448304935, 18.609708891065416]),
            ("Mediclinic Louis Leipoldt",
             [-33.90009911632751, 18.613056288015194]),
            ("Mediclinic Panorama", [-33.87518210873116, 18.576183400259424])
        ]
    },
    {
        "user": ("Cookies", "cookies@gmail.com", "cookies"),
        "admins": [
            ("Pineapple", "Juice", "male", "4909095800080", {
                "street_name": "Aborford Way",
                "house_number": 2,
                "city": "Johannesburg",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0605555625"),
            ("Guava", "Juice", "female", "5910245800086", {
                "street_name": "Cross Port",
                "house_number": 206,
                "city": "Port Elizabeth",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0605559927"),
        ],
        "hospitals": [
            ("Netcare N1 City Hospital",
             [-33.89320714098042, 18.558594069568404])
        ]
    },
    {
        "user": ("Biscuit", "biscuit@gmail.com", "biscuit"),
        "admins": [
            ("Grapefruit", "Juice", "female", "2311034800085", {
                "street_name": "Apache Way",
                "house_number": 256,
                "city": "Johannesburg",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0555519579"),
            ("Lemon", "Juice", "female", "5209114800081", {
                "street_name": "Apache Way",
                "house_number": 256,
                "city": "Johannesburg",
                "country": "South Africa",
                "postal_code": "1234"
            }, "0835553106"),
        ],
        "hospitals": [
            ("Netcare UCT Private Academic Hospital",
             [-33.94159234030289, 18.462903977495348]),
            ("Netcare Kuilsriver Hospital",
             [-33.91735414153332, 18.67510024629595])
        ]
    }
]


def create_and_login_user(email_address, password):
    data = {
        "email": email_address,
        "password": password
    }

    # Firstly, create the user.
    signup_url = url + "auth/signup"

    resp = requests.post(signup_url, json=data)

    if (resp.status_code == 200):
        # Secondly, login the user in.
        login_url = url + "auth/login"

        resp = requests.post(login_url, json=data)
        if resp.status_code == 200:
            token = resp.json()["token"]

            return token
        raise Exception(resp.content)
    raise Exception(resp.content)


def create_and_login_adminuser(name, email_address, password):
    data = {
        "name": name,
        "email": email_address,
        "password": password
    }

    # Firstly, create the user.
    signup_url = url + "auth/admin/signup"

    resp = requests.post(signup_url, json=data)

    if (resp.status_code == 200):
        # Secondly, login the user in.

        login_url = url + "auth/admin/login"
        resp = requests.post(login_url, json=data)
        if resp.status_code == 200:
            token = resp.json()["token"]

            return token
        raise Exception(resp.content)
    raise Exception(resp.content)


def create_patient(jwt_token, name, surname, gender, id_number, address, phone):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }
    data = {
        "name": name,
        "surname": surname,
        "gender": gender,
        "id_number": id_number,
        "address": address,
        "phone": phone
    }

    patients_url = url + "patients"

    resp = requests.post(patients_url, json=data, headers=headers)

    if resp.status_code == 200:
        return resp.json()["id"]
    else:
        raise Exception(resp.content)


def create_admin(jwt_token, name, surname, gender, id_number, address, phone_number):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }
    data = {
        "name": name,
        "surname": surname,
        "gender": gender,
        "id_number": id_number,
        "address": address,
        "phone": phone_number,
    }

    admin_url = url + "admins"

    resp = requests.post(admin_url, json=data, headers=headers)

    if resp.status_code == 200:
        return resp.json()["id"]
    else:
        raise Exception(resp.content)


def create_hospital(jwt_token, hospital_name, coordinates):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }
    data = {
        "hospital_name": hospital_name,
        "point": coordinates
    }

    hospital_url = url + "hospitals"

    resp = requests.post(hospital_url, json=data, headers=headers)

    if resp.status_code == 200:
        return resp.json()["id"]
    else:
        raise Exception(resp.content)


def create_appointment(jwt_token, patient_id, hospital_id, date, ward, reason):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }
    data = {
        "patient_selected": patient_id,
        "hospital_selected": hospital_id,
        "appointment_date": date,
        "ward_type": ward,
        "reason_for_visit": reason
    }

    appointments_url = url + "appointments"

    resp = requests.post(appointments_url, json=data, headers=headers)

    if resp.status_code == 200:
        return resp.json()["id"]
    else:
        raise Exception(resp.content)


if __name__ == "__main__":
    user_results = {}
    adminuser_results = {}

    admin_user_count = 1
    print('Creating Admin Users')

    for data_item in admindata_to_create:
        print(
            f'Creating Admin User [{admin_user_count}/{len(admindata_to_create)}]')
        user_data = data_item["user"]
        token = create_and_login_adminuser(
            user_data[0], user_data[1], user_data[2]
        )

        if user_data[1] not in adminuser_results:
            adminuser_results[user_data[1]] = {}
        adminuser_results[user_data[1]]["jwt_token"] = token
        adminuser_results[user_data[1]]["admins"] = []
        adminuser_results[user_data[1]]["hospitals"] = []

        for admin in data_item["admins"]:
            admin_id = create_admin(
                token, admin[0], admin[1], admin[2], admin[3], admin[4], admin[5]
            )
            adminuser_results[user_data[1]]["admins"].append(admin_id)
            print(f'─ Admin: {admin[0]}\t\t[✓]')

        for hospital in data_item["hospitals"]:
            hospital_id = create_hospital(token, hospital[0], hospital[1])
            adminuser_results[user_data[1]]["hospitals"].append(hospital_id)
            print(f'─ Hospital: {hospital[0]}\t\t[✓]')

        print('')
        admin_user_count += 1

    user_count = 1
    print('Creating Users')

    for data_item in userdata_to_create:
        print(f'Creating User [{user_count}/{len(userdata_to_create)}]')
        # Firstly, create the User data.
        user_data = data_item["user"]
        token = create_and_login_user(user_data[0], user_data[1])

        if user_data[1] not in user_results:
            user_results[user_data[1]] = {}
        user_results[user_data[1]]["jwt_token"] = token
        user_results[user_data[1]]["patients"] = []
        user_results[user_data[1]]["appointments"] = []

        # Next, create the patient data.
        for patient in data_item["patients"]:
            patient_id = create_patient(
                token, patient[0], patient[1], patient[2], patient[3], patient[4], patient[5]
            )
            user_results[user_data[1]]["patients"].append(patient_id)
            print(f'─ {patient[0]}\t\t[✓]')

        for appointment in data_item["appointments"]:
            index = random.choice(admindata_to_create)["user"][1]
            print(index)

            appointment_id = create_appointment(
                token,
                random.choice(
                    adminuser_results[index]["hospitals"]
                ),
                random.choice(user_results[user_data[1]]["patients"]),
                datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
                appointment[0],
                appointment[1]
            )
            print(f'─ {appointment[1]}\t\t[✓]')

        print('')
        user_count += 1
