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
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    Loops until data is valid.
    """
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here: ')
        
        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data is valid.')
            break
    
    return sales_data


def validate_data(values):
    """
    Converts all values the integers,
    returns ValueError if strings cannot convert
    or if there isn't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
                )
    except ValueError as e:
        print(f'Invalid data: {e}, Please try again.\n')
        return False

    return True


def calculate_surplus_data(sales_row):
    """
    Compares sales data with stock data to calculate surplus data.
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def update_worksheet(data, worksheet):
    """
    Updates relevant worksheet with provided list of integers.
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully.\n')


def get_last_5_entries_sales():
    """
    Collect last 5 entries of each sandwich sales
    and return that data as a list of lists.
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    

print('Welcome to Love Sandwiches Data Automation')
main()

sales_columns = get_last_5_entries_sales()