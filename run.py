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
SHEET = GSPREAD_CLIENT.open('chef_profit')

def get_sales_data():
    """
    Get sales data from user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be a four didget number, and  seperated by a full stop.")
        print("Example: 10,20,30,40,50,60\n")
    
        data_str = input("Enter Selling price Here: ")
                   

        sales_data = data_str.split(",")

        if  validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if the srings cannot be converted into lines,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly  values requires, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet, add row with list of data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)	
    print("Sales successfuly updated.\n")

def calculate_suprlus_data(sales_row):
    """
    Comapre sales with staock and calculayte the surplus for each type item.

    Thes surplus is defined as the sales fu=igure subtracted for the stock:
    - Positive surplus indicates waste.
    - Negative surplus bdicates extra made when stock was sold out.
    """
    print("Calculating surplus data....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():
    """
    Run all program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_suprlus_data(sales_data)

    
print("Welcome to love sandwiches data automation")
main()
