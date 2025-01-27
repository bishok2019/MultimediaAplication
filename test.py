import requests

# #login user
def user_login():
    login_url = 'http://127.0.0.1:8000/accounts/login/'

    data = {
        'username':'bishok',
        # 'password':'Password@123#',
        'password':'Password@123#_',
        
    }

    try:
        get_response = requests.post(login_url, json=data)
        print(get_response.json())
        print('status:', get_response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {get_response.text}")
# register user
def register_user():
    register_url = 'http://127.0.0.1:8000/accounts/register/'

    data = {
        'username':'victor',
        'email':'Victor@123.com',
        'password':'Password@123#',
        'first_name':'Victor',
        'last_name':'William',
        
    }

    response = requests.post(register_url, json=data)
    print(response.json())
# get_blog
def get_blog():
    blog_url='http://127.0.0.1:8000/blog/blogapi/'


    data = {
        "title": "t1",
        "body": "b1"
    }
    headers={
        'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3NDUwNDg1LCJpYXQiOjE3MzczNjQwODUsImp0aSI6Ijc2Y2I2NDI2Mjg5ZjQ1ZGJiZjMxZDllNjUwNjUyMDI3IiwidXNlcl9pZCI6OX0.3xBiQdpNqv32hVIQQLhCAUhzexGUVLWfJ18MZaUJjdk'
    }
    response = requests.get(blog_url)
    print(response.json())
    # print(response.headers)
# create blog
def create_blog():
    create_url = 'http://127.0.0.1:8000/blog/blogpost/'
    data = {
        "title": "t1",
        "body": "b1"
    }
    headers={
        'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3NDUwNDg1LCJpYXQiOjE3MzczNjQwODUsImp0aSI6Ijc2Y2I2NDI2Mjg5ZjQ1ZGJiZjMxZDllNjUwNjUyMDI3IiwidXNlcl9pZCI6OX0.3xBiQdpNqv32hVIQQLhCAUhzexGUVLWfJ18MZaUJjdk'
    }
    response = requests.post(create_url, json=data, headers=headers)
    print(response.json())
# update blog
def update_blog():
    blog_url='http://127.0.0.1:8000/blog/blogmodify/3'

    data = {
        "title": "t2",
        "body": "b2"
    }
    headers={
        'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3NDUwNDg1LCJpYXQiOjE3MzczNjQwODUsImp0aSI6Ijc2Y2I2NDI2Mjg5ZjQ1ZGJiZjMxZDllNjUwNjUyMDI3IiwidXNlcl9pZCI6OX0.3xBiQdpNqv32hVIQQLhCAUhzexGUVLWfJ18MZaUJjdk'
    }
    response = requests.put(blog_url, json=data, headers=headers)
    print(response.json())
# Delete blog
def delete_blog():
    blog_url='http://127.0.0.1:8000/blog/blogmodify/3'

    data = {
        "title": "t2",
        "body": "b2"
    }
    headers={
        'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3NDUwNDg1LCJpYXQiOjE3MzczNjQwODUsImp0aSI6Ijc2Y2I2NDI2Mjg5ZjQ1ZGJiZjMxZDllNjUwNjUyMDI3IiwidXNlcl9pZCI6OX0.3xBiQdpNqv32hVIQQLhCAUhzexGUVLWfJ18MZaUJjdk'
    }
    response = requests.delete(blog_url, json=data, headers=headers)
    print(response.json())

# delete_blog()
get_blog()

# middleware in django
# how py manage.py works
# url to view