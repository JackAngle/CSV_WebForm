import csv
import requests
import click
import sys
import time


@click.command()
@click.option('--name', prompt=True)
def hello(name):
    click.echo('Hello %s! Nice to meet you! Now let\'s start!' % name)


# Open csv file
# Return data if SUCCESS
# Exit program if FAIL
def open_csv(file_path):
    try:
        with open(file_path, newline='') as csv_file:
            print(file_path)
            csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
            data = (dict(csv_reader))
            return data
    except FileNotFoundError:
        print('Invalid csv file path!!!')
        time.sleep(1)
        sys.exit(-1)


# Convert keys:
#   0 - No convert
#   1 - Uppercase
#   2 - Lowercase
def convert_keys(data, command=0):
    # Change all keys to uppercase
    if command == 1:
        data = dict((k.upper(), v) for k, v in data.items())
        return data
    # Change all keys to lowercase
    elif command == 2:
        data = dict((k.lower(), v) for k, v in data.items())
        return data

    return data


# Convert values:
#   0 - No convert
#   1 - Uppercase
#   2 - Lowercase
def convert_values(data, command=0):
    # Change all values to uppercase
    if command == 1:
        data = dict((k, v.upper()) for k, v in data.items())
        return data
    # Change all values to lowercase
    elif command == 2:
        data = dict((k, v.lower()) for k, v in data.items())
        return data

    return data


# Filter out file path in data's values and return files dict
def filter_file_path_out(data):
    files = {}
    option = None
    for key, value in data.items():
        click.echo(key)
    option = click.prompt('PLEASE SELECT KEY(S) THAT CONTAINS FILE PATH! '
                          'MULTIPLE VALUES IS OK. SEPARATE BY SPACE'
                          'YOUR INPUT', type=str)
    if option is not None:
        for item in option.split(' '):
            files[item] = data.get(item)
            data.pop(item)
        return data, files

    return data, files


# Process keys:
#  Check input, if -1 then Exit program
def process_keys(option):
    while option not in (-1, 0, 1, 2):
        click.echo('Invalid argument!\n')
        option = click.prompt('Please select a valid convert type for keys: \n '
                              '-1 - Exit program\n'
                              '0  - No convert\n'
                              '1  - All uppercase\n'
                              '2  - All lowercase\n'
                              'YOUR INPUT', type=int)
        if option == -1:
            sys.exit(-1)
    return option


# Process values:
#  Check input, if -1 then Exit program
def process_values(option):
    while option not in (-1, 0, 1, 2):
        click.echo('Invalid argument!\n')
        option = click.prompt('Please select a valid convert type for values: \n '
                              '-1 - Exit program\n'
                              '0  - No convert\n'
                              '1  - All uppercase\n'
                              '2  - All lowercase\n'
                              'YOUR INPUT', type=int)
        if option == -1:
            sys.exit(-1)
    return option


# Process space character in key (because webform keys are normally variables):
def process_spaces_in_keys(data, replace_character: str):
    if replace_character is not None:
        data = dict((k.replace(' ', replace_character), v) for k, v in data.items())
        return data
    return data


# Function for reading csv & return data
@click.command()
@click.option('--key-convert', '-kc',
              type=click.Choice(['uppercase', 'lowercase', '0', '1', '2'], case_sensitive=False))
@click.option('--value-convert', '-vc',
              type=click.Choice(['uppercase', 'lowercase', '0', '1', '2'], case_sensitive=False))
@click.option('--file-path', default='', help='File path of csv file')
@click.option('--url', '-u', type=str, required=True, help="URL to webform")
@click.option('--space-replace', '-sr', type=str, help='Replace spaces in keys of data with a character',
              default=None)
def get_csv_data(file_path, url, key_convert, value_convert, space_replace):
    while file_path == '':
        file_path = click.prompt('Please enter a valid file path to csv file', type=str)

    # Read & get data from csv file
    data = open_csv(file_path)

    # Convert keys
    key_convert = process_keys(key_convert)
    data = convert_keys(data, key_convert)  # change all keys to lowercase

    # Convert values
    value_convert = process_values(value_convert)
    data = convert_values(data, value_convert)  # change all keys to lowercase

    # Replace space in keys with '_'
    data = process_spaces_in_keys(data, space_replace)

    # Specify file path in data's values
    data, files = filter_file_path_out(data)

    return webformrequest(data, files, url)


# Function for sending request to webform

def webformrequest(data, files, web_form_url):
    if web_form_url is not web_form_url.endswith('/'):
        web_form_url = web_form_url + '/'
    client = requests.Session()
    client.get(web_form_url)  # sets_cookies

    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrf_token = client.cookies['csrftoken']
        data['csrfmiddlewaretoken'] = csrf_token
    else:
        # older versions
        csrf_token = client.cookies['csrf']
        data['csrfmiddlewaretoken'] = csrf_token
    data['next'] = '/add_topic/'

    click.echo("Data to be sent: " + str(data))
    for i in files:
        files[i] = open(files.get(i), 'rb')
    click.echo("Files to be sent: " + str(files))
    client = client.post(web_form_url, data=data, headers=dict(Referer=web_form_url), files=files)
    print("Headers from a POST request response: %s" % client.headers)
    print("HTML Response: %s" % client.text)


if __name__ == '__main__':
    get_csv_data()



