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
    Get sales figures input from the user
    """
    print("Please enter sales numbers from last Sunday.")
    print("Six numbers as each shakes types, separated by commas.")
    print("Example: 5,11,8,6,9,2\n")

    data_str = input("Enter your sales numbers here: ")

    sales_data = data_str.split(",")
    validate_data(sales_data)

def validate_data(values):
    """
    To convert all string values into integers (int).
    ErrorMessage if strings cannot be trun to int,
    or less or more than 6 values. 
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f'6 numbers required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')

get_sales_data()
