# shopzon
an Ecommerce website using Django,DRF,channels,websocket and celery.


## How to clone and run:
>go to directory where you want to clone and run this command:
  ```sh
  git clone https://github.com/aadil611/shopzon.git; cd shopzon
  ```
		
>create virtual env:
  ```sh
  python -m venv env
  ```
		
>activate virtual env:

 ```sh
  source env/bin/activate
  ```
		
>update pip:

 ```sh
 pip install -U pip
 ```
		
>install requirements:
  ```sh
  pip install -r requirements.txt
  ```
  
  >enter email and password in .env file in given format:
  ```sh
  EMAIL = 'email'
  PASSWORD = 'password'
  ```
- for this you have to create an app password for your gmail account.
  
  ```sh
  open gmail -> manage your account -> security -> app passwords
  ```
  > before creating app password activate 2-step verification
  
  
 >now run these commands in different terminals:
 ```sh
  python manage.py runserver
  celery -A shopzon.celery worker -l info
  ```
