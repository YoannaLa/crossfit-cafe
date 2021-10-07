import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cross_fit_cafe_shakes')

def get_sales_data():
    """
    Get sales figures input from the user.
    """
    print("Please enter sales numbers from last Sunday.")
    print("Data should be six numbers for six shakes types, separated by commas ,")
    print("Example: 5,11,8,6,9,2\n")

    data_str = input("Enter your sales numbers here: ")
    print(f"The data provided is {data_str}")


get_sales_data()