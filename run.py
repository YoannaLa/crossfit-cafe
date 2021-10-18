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

        data_str = input('Enter your sales numbers here:\n')
       
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print('Data is valid!')
            break

    return sales_data


def validate_data(values):
    """
    To convert all input values into numbers(int).
    ErrorMessage if strings cannot be trun to int,
    or less or more than 6 values
    """
    try:
        if len(values) != 5:
            raise ValueError(
                print(f'5 numbers required, you provided {len(values)}')
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
    data per collumn, and return the data.
    """
    sales = SHEET.worksheet('Sales')

    detox_column_last_4_weeks = str(sales.col_values(1)[-4:])
    cleanser_column_last_4_weeks = str(sales.col_values(2)[-4:])
    protein_column_last_4_weeks = str(sales.col_values(3)[-4:])
    cherry_twist_column_last_4_weeks = str(sales.col_values(4)[-4:])
    green_column_last_4_weeks = str(sales.col_values(5)[-4:])
    results = 'Last 4 weeks Sales: \n Detox %s \n Cleanse %s \n Protein %s \n Cherry twist %s \n Green twist %s' % (detox_column_last_4_weeks, cleanser_column_last_4_weeks, protein_column_last_4_weeks, cherry_twist_column_last_4_weeks, green_column_last_4_weeks)
    
    return results
    
   
def get_max_value_from_list(sale_value_list):
    max = 0
    for sale_value in sale_value_list:
        number_value = int(sale_value)
        if number_value > max:
            max = number_value
    return max

  
def most_selling_product_last_4_weeks():
    """
    Most popular shakes in last 4 weeks
    """
    sales = SHEET.worksheet('Sales')
    detox_column_last_4_weeks = sales.col_values(1)[-4:]
    cleanser_column_last_4_weeks = sales.col_values(2)[-4:]
    protein_column_last_4_weeks = sales.col_values(3)[-4:]
    cherry_twist_column_last_4_weeks = sales.col_values(4)[-4:]
    green_column_last_4_weeks = sales.col_values(5)[-4:]
    detox_max = get_max_value_from_list(detox_column_last_4_weeks)
    cleanser_max = get_max_value_from_list(cleanser_column_last_4_weeks)
    protein_max = get_max_value_from_list(protein_column_last_4_weeks)
    cherry_twist_max = get_max_value_from_list(cherry_twist_column_last_4_weeks)
    green_max = get_max_value_from_list(green_column_last_4_weeks)
    max_value_list = [detox_max, cleanser_max, protein_max, cherry_twist_max, green_max]
    max_value = get_max_value_from_list(max_value_list)
    results = 'Max 4 weeks Sales: \n Detox %i \n Cleanse %i \n Protein %s \n Cherry twist %i \n Green twist %i' % (detox_max, cleanser_max, protein_max, cherry_twist_max, green_max)
 
    if (max_value == detox_max):
        print('Detox is the most poluar shake with: %i sold' % max_value)
    if (max_value == cleanser_max):
        print('Cleanser is the most poluar shake with: %i sold' % max_value)
    if (max_value == protein_max):
        print('Protein is the most poluar shake with: %i sold' % max_value)
    if (max_value == cherry_twist_max):
        print('Cherry Twist is the most poluar shake with: %i sold' % max_value)
    if (max_value == green_max):
        print('Green is the most popluar shake this month with: %i sold' % max_value)
        return results


def calculate_stock_data(data):
    """
    Average stock for each shake
    """
    stock = SHEET.worksheet('Stock')
    print('Calculating stock data...\n')
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average
        new_stock_data.append(stock_num)
    
    return new_stock_data


def get_stock_value(data):
    """
    The next week shake numbers prediction
    """
    stock = SHEET.worksheet('Stock').get_all_values()
    print('Numbers for next week:\n')
    
    headings = stock[0]
    stock_row = stock[-1]

    stock_value = []
    for stock in zip(headings, stock_row):
        stock_value.append(stock)
        
    for shakes_name, new_stock_value in zip(headings, stock_row):
        print(f'Shake: {shakes_name.upper()}, No: {new_stock_value}\n')

    return new_stock_value
    

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "Sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "Surplus")
    stock_data = calculate_stock_data(data)
    update_worksheet(stock_data, "Stock")
    new_stock_value = calculate_stock_data(data)
    most_selling_product_last_4_weeks()
    get_stock_value(data)

print('Welcome to CrossFit Cafe data collection.')
main()
