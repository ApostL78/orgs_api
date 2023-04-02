# orgs_api
Django REST framework приложение, с переопределённым пользователем и списком организаций в которых он состоит

## [Тестовое задание](https://docs.google.com/document/d/1-CnduFBumZC_xlnAxdFjxO2GeXpZgOZy/edit?usp=sharing&ouid=105845999361712496764&rtpof=true&sd=true)

# How It Works

To implement ManyToMany relationship between user and organization we need 3 tables: user, organization and table with keys

![models diograms](https://github.com/ApostL78/orgs_api/blob/master/database_diogram.jpg)

1) There is an endpoint for user creation (registration), listing all users with list of organizations called `users` (http://127.0.0.1:8000/api/users/) methods: GET, POST

Also to get user by ID add his id to the end of url (.../1/) (Anyone can GET info, but only owner can edit by PUT or PATCH)
2) For listing all organizations with their users we have an endpoint `organizations` (http://127.0.0.1:8000/api/organizations/) methods: GET, POST

Make POST request to endpoit `token` (http://127.0.0.1:8000/api/token/) to get access token for authentication and then use it in headers (key: Authentication value: Bearer ACCESS_TOKEN)
### For more complex documentation visit [swagger](http://127.0.0.1:8000/swagger/) or [redoc](http://127.0.0.1:8000/redoc/) page when server is running

# How To Run
To start this app you need to:
1. Clone this repo and move to project
```sh
git clone https://github.com/ApostL78/orgs_api.git && cd orgs_api
```
2. Create and activate `venv`
```sh
python3 -m venv venv && source ./venv/bin/activate
```
3. Create environment variables
```sh
cp .env.example .env
```
and then put your values

4. Install all requirements
```sh
pip install -r requirements.txt
```
5. Migrate and run server
```sh
python3 manage.py migrate && python3 manage.py runserver
```
After the server starts, navigate to `http://localhost:8000/swagger/` in your web browser
