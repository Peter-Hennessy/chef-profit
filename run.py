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


def update_worksheet(data, worksheet):
    """
    Revieves a list of integers to be inmserted into worksheet
    Update thet relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} Worksheet successfuly updated\n")


def calculate_surplus_data(sales_row):
    """
    Comapre sales with staock and calculayte the surplus for each type item.

    Thes surplus is defined as the sales fu=igure subtracted for the stock:
    - Positive surplus indicates waste.
    - Negative surplus bdicates extra made when stock was sold out.
    """
    print("Calculating surplus data....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects collumns of data from the salews wprksheet, collecting 
    the last 5 entries for each sandwiches and returns the data 
    as a list of lists
    """
    sales =SHEET.worksheet("sales")
   #column = sales.col_values(3)
   #print(column)

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns
       





def main():
    """
    Run all program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("Welcome to love sandwiches data automation")
#main()

sales_columns = get_last_5_entries_sales()
