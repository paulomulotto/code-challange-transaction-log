# code-challange-transaction-log

run all commands through Docker compose
```docker-compose run --rm app sh -c "python manage.py collectstatic"```

Test Django application
```docker-compose run --rm app sh -c "python manage.py test"```

Test a function
```docker-compose run --rm app sh -c "python manage.py wait_for_db && flake8"```