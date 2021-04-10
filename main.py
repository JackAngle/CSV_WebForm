import csv
import requests

WEBFORM_URL = 'http://127.0.0.1:8000/add_topic/'

with open('file.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
    data = (dict(spamreader))

    # Edit data
    data = dict((k.lower(), v) for k, v in data.items()) # change all keys to lowercase
    # Change topic_img key to image
    try:
        data['image'] = data.pop('topic_img')
    except KeyError:
        print("KeyError: key is not exist to be changed")

    # Change topic_img key to image
    try:
        data = dict((k.replace(' ', '_'), v) for k, v in data.items())
    except KeyError:
        print("KeyError: key is not exist to be changed")

    # for row in spamreader:
    #     # print(', '.join(row))
    #     data = tuple(row)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }

    client = requests.Session()
    client.get(WEBFORM_URL) #sets_cookies

    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrf_token = client.cookies['csrftoken']
        data['csrfmiddlewaretoken'] = csrf_token
    else:
        # older versions
        csrf_token = client.cookies['csrf']
        data['csrfmiddlewaretoken'] = csrf_token
    data['next'] = '/add_topic/'

    print(data)
    # resp = requests.get(WEBFORM_URL)
    # print("Response to GET request: %s" % resp.content)
    # login_data = dict(username=EMAIL, password=PASSWORD, csrfmiddlewaretoken=csrftoken, next='/')
    client = client.post(WEBFORM_URL, data=data, headers=dict(Referer=WEBFORM_URL))
    print("Headers from a POST request response: %s" % client.headers)
    print("HTML Response: %s" % client.text)




