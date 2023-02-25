# code-challange-transaction-log

run all commands through Docker compose
```docker-compose run --rm app sh -c "python manage.py collectstatic"```

Test Django application
```
docker-compose run --rm app sh -c "coverage run --source='.' manage.py test && coverage report"
```

Test a function
```docker-compose run --rm app sh -c "python manage.py wait_for_db && flake8"```

If some problem ocour on migrations it is possible remove the volume
```docker volume ls ```
```docker volume rm (partition name)````