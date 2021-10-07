import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("Please enter sales numbers from last Sunday.")
        print("Six numbers as each shakes types, separated by commas.")
        print("Example: 5,11,8,6,9,2\n")

        data_str = input("Enter your sales numbers here: ")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print('Data is valid!')
            break

    return sales_data


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
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with list data provided
    """
    print('Sales numbers updating...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated!.\n')


def calculating_surplus_data(sales_row):
    """
    Compare sales with stock and work out the surplus for each shake.
    The surplus is a differents between sales and stock:
     - Positive number shows waste
     - Negative number shows shakes made as customer waits as stock sold out.
    """
    print("Working out the surplus numbers.\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    

    surplus_data =[]
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculating_surplus_data(sales_data)
    print(new_surplus_data)


print('Welcome to CrossFit Cafe data collection.')
main()