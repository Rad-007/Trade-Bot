import eel
import csv

# Define the path to your HTML file and set Eel options
eel.init('templates')

# Create an empty list to store the data
data = []

def save_to_csv(todo_list):
    with open('todo_list.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'target', 'status'])
        for todo in todo_list:
            writer.writerow(todo['name'], todo['target'], todo['status'])

def load_from_csv():
    todo_list = []
    try:
        with open('todo_list.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                todo_list.append(row)
    except FileNotFoundError:
        pass
    return todo_list


# Start the Eel app
eel.start('index.html', size=(1500, 1000))




@eel.expose
def delete_from_csv(index):
    data = load_from_csv()
    if 0 <= index < len(data):
        data.pop(index)
        with open('stocks.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)