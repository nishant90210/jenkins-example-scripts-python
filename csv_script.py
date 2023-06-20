import csv
import requests

CSV_FILE = 'numbers.csv'
API_ENDPOINT = 'http://demo8119202.mockable.io/'

def call_api(number):
    payload = {'number': number}  # Customize the payload based on the API requirements
    response = requests.get(API_ENDPOINT, params=payload)
    return response.json()  # Assuming the API returns JSON data

def main():
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            number = int(row[0])  # Assuming the number is in the first column
            result = call_api(number)
            print(f'Response for number {number}: {result}')
            # Do further processing or save the result as needed

if __name__ == '__main__':
    main()