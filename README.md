# Code Challenge Transaction Log
This is a financial transaction system developed in Python using Django Rest Framework.

## Installation instructions / Run Instructions
### Step 1 - Docker and Docker Compose
To run this project you must have Docker and Docker Compose installed.

If you do not have it installed, you can check the following link:
- https://docs.docker.com/engine/install/

### Step 2 - Clone the Project
Clone that project to your machine.

### Step 3 - Run the project
1. In a terminal go the project folder that you cloned before.
2. Execute de command  ```docker-compose build```
3. Execute de command  ```docker-compose up```

## The Solution
The solution was implemented using Django Rest Framework and Postgres.
The solution consist in 6 main apps:
- [account](app/account)
- [account.transaction](app/account/transaction/)
- [client](app/client)
- [core](app/core)
- [transaction](app/transaction)
- [user](app/user)


After run the project you can use and test APIs through http://localhost:8000/api/docs

Some actions required login. To do that you can use the API `/api/user/create/` with a payload like:
```
"{
  "email": "test@test.com",
  "password": "passtest123",
  "name": "test"
}
```

With that new user, you can use the API `/api/user/token/` to get a token.

Now, with the token, you can click in the Authorize button, go to the tokenAuth option and fill the field Value with **Token + "THE TOKEN THAT YOU GOT BEFORE"** and click in Authorize.

After that you can test the system using that user.

A nice sequence of actions is:
- Create user 1 (POST: /api/user/create/)
- Create account for user 1 (POST: /api/client/client/)
- Create a account for that user with money (POST: /api/account/)

- Create user 2 (POST: /api/user/create/)
- Create account for user 2 (POST: /api/client/client/)
- Create a account for user 2 user with money (POST: /api/account/)

- Generate a token for user 1: (POST: /api/user/token/)
- Authorize user 1
- Get the balance (GET: /api/account/balance/)
- Make some transactions. Options for type field are: DEPOSITS = 'DP', WITHDRAWALS = 'WD', EXPENSES = 'EX'
- Check the balance (GET: /api/account/balance/)
- Logout and now login with user 2
- Check the balance

If you want to change the user, you can go back to Authorize and clicking in logout.


## Attachment
- Command to run tests on the project:

    ```
    docker-compose run --rm app sh -c "python manage.py test"
    ```

- Command to run lint checker on the project:

    ```
    docker-compose run --rm app sh -c "python manage.py wait_for_db && flake8"
    ```

- Command to get the coverage test on the project:
    ```
    docker-compose run --rm app sh -c "coverage run --source='.' manage.py test && coverage report"
    ```
