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
    Get sales figures input from the user, while statment added so the
    programme keeps asking for the right data
    """
    while True:
        print("Please enter sales numbers from last Sunday.")
        print("Five numbers as each shakes types, separated by commas.")
        print("Example: 5,11,8,6,9,\n")

        data_str = input("Enter your sales numbers here:\n")

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
    try:
        [int(value) for value in values]
        if len(values) != 5:
            raise ValueError(
                f'5 numbers required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} Worksheet updated successfully!!\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and work out the surplus for each shake.
    The surplus is a differents between sales and stock:
     - Positive number shows waste
     - Negative number shows shakes made as customer waits as stock sold out.
    """
    print("Working out the surplus numbers...\n")
    stock = SHEET.worksheet('Stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_4_weeks_sales():
    """ 
    Collect sales of each shake from last 4 weeks,
    data per collumn, and return the data as a list of lists.
    """
    sales = SHEET.worksheet('Sales')

    columns = []
    for ind in range(1, 6):
        column = sales.col_values(ind)
        columns.append(column[-4:])
    
    return columns

def calculate_stock_data(data):
    """
    Average stock for each shake, adding 15%
    """
    sales = SHEET.worksheet('Sales')
    print('Calculating stock data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.5
        new_stock_data.append(round(stock_num))

    return new_stock_data

def get_stock_value(data):
    """
    The next week shake numbers prediction
    """
    stock = SHEET.worksheet('Stock').get_all_values()
    print('The stock for next week is :\n')
    
    headings = stock[0]
    stock_row = stock[-1]

    stock_value = []
    for stock in zip(headings, stock_row):
        stock_value.append(stock)
        
    for shakes_name, new_stock_value in zip(headings, stock_row):
        print(f'Shake name: {shakes_name}, number to prepare for next week: {new_stock_value}\n')

    #return stock_value
       
def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "Sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "Surplus")
    sales_columns = get_last_4_weeks_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "Stock")
    get_stock_value(data)

print('Welcome to CrossFit Cafe data collection.')
main()
