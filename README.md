# cars app

This app was bootstrapped with [Imagine.ai](https://imagine.ai) 💛
> Imagine.ai is an app starter on steroids! 

### Run the app in terminal

Install packages and start the application server.

```
$ make install
$ make migrate
$ make run
```

### Run the app inside a Docker container

1. Build the docker container and get it up and running.

```
$ docker-compose build
$ docker-compose up
```

2. Setup database tables by running migrations.

```
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
```

### Make API calls against the server

Go to [http://localhost:8000/graphql](http://localhost:8000/graphql)

### Run Django admin dashboard

1. Setup a password to login to the Django admin dashboard.

```
make adminuser password=<choose-a-secure-password>
```

2. Go to [http://localhost:8000/admin](http://localhost:8000/admin) and login to the dashboard using username `admin` and the password you chose in step 1 above.

### Run tests and check code coverage

```
$ make test
$ make coverage
```

### Lint your code

```
$ make lint
```

### Learn More

1. Learn more about: 
  - the [Django architecture choices](https://imagine.ai/docs/architecture-django) used.
  - the [best practices](https://imagine.ai/docs/best-practices) followed.

2. Imagine is in beta - here are the [known issues](https://imagine.ai/docs/known_issues) that we are working to fix.
