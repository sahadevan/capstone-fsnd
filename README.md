# Capstone Casting Agency Project

## Casting Agency App

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. The application must:

1. Create a movie or actor.
2. Read all movies or actors.
3. Update a movie or actor.
4. Delete a movie or actor.

The above operations must be authorized before being performed. The authorization includes the following roles

1. Casting Assistant
   1. Can view actors and movies
2. Casting Director
   1. All permissions a Casting Assistant has and…
   2. Add or delete an actor from the database
   3. Modify actors or movies
3. Executive Producer
   1. All permissions a Casting Director has and…
   2. Add or delete a movie from the database

## Setting up the App

### Install Dependencies

1. **Python >= 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

Set Database Environment variables

```bash
export DB_NAME="casting"
```

```bash
export DB_PATH="postgresql+psycopg2://postgres@localhost:5432/casting"
```

With Postgres running, create a `casting` database:

```bash
createdb casting
```

Migration script available in `./migrations` directory
DB upgrade

```bash
flask db upgrade
```

### Run the Server

From within the `./starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

`GET '/api/v1.0/movies'`

- Fetches all movies
- Request Arguments: None
- Returns: An object with success flag, `movies`, that contains an array of movie objects

```json
{
  "movies": [
    {
      "release_date": "Sun, 26 Mar 2023 00:00:00 GMT",
      "title": "Frozen"
    },
    {
      "release_date": "Tue, 12 Dec 2006 00:00:00 GMT",
      "title": "The Number 23"
    }
  ],
  "success": true
}
```

---

`GET '/api/v1.0/actors'`

- Fetches all actors
- Request Arguments: None
- Returns: An object with success flag, `actors`, that contains an array of actor objects

```json
{
  "actors": [
    {
      "age": 70,
      "gender": "Male",
      "name": "stone gold steve austin"
    },
    {
      "age": 2,
      "gender": "Female",
      "name": "S.Nakshatra"
    }
  ],
  "success": true
}
```

---

`DELETE '/api/v1.0/movies/${id}'`

- Deletes a specified movie using the id of the movie
- Request Arguments: `id` - integer
- Returns: An object with success flag, deleted movie id

```json
{
  "delete": 11,
  "success": true
}
```

---

`DELETE '/api/v1.0/actors/${id}'`

- Deletes a specified actor using the id of the actor
- Request Arguments: `id` - integer
- Returns: An object with success flag, deleted actor id

```json
{
  "delete": 10,
  "success": true
}
```

---

`POST '/api/v1.0/movies'`

- Sends a post request in order to create a movie
- Request Body:

```json
{
  "title": "Frozen 2",
  "release_date": "2022-03-26"
}
```

- Returns: a success flag and `movies`, that contains an array of new movie object

```json
{
  "movies": [
    {
      "id": 46,
      "release_date": "Sun, 26 Mar 2022 00:00:00 GMT",
      "title": "Frozen 2"
    }
  ],
  "success": true
}
```

---

`POST '/api/v1.0/actors'`

- Sends a post request in order to create a actor
- Request Body:

```json
{
  "name": "Dwayne Johnson",
  "age": 50,
  "gender": "Male"
}
```

- Returns: a success flag and `actors`, that contains an array of new actor object

```json
{
  "actors": [
    {
      "age": 50,
      "gender": "Male",
      "id": 22,
      "name": "Dwayne Johnson"
    }
  ],
  "success": true
}
```

---

`PATCH '/api/v1.0/movies/${id}'`

- Sends a patch request in order to update a movie
- Request Arguments: `id` - integer
- Request Body:

```json
{
  "title": "The Fall",
  "release_date": "2023-03-25"
}
```

- Returns: a success flag and `movies`, that contains an array of new movie object

```json
{
  "movies": [
    {
      "id": 10,
      "release_date": "Sat, 25 Mar 2023 00:00:00 GMT",
      "title": "The Fall"
    }
  ],
  "success": true
}
```

---

`PATCH '/api/v1.0/actors/${id}'`

- Sends a patch request in order to update an actor
- Request Arguments: `id` - integer
- Request Body:

```json
{
  "name": "Halle Berry",
  "age": 34,
  "gender": "Female"
}
```

- Returns: a success flag and `actors`, that contains an array of new actor object

```json
{
  "actors": [
    {
      "age": 34,
      "gender": "Female",
      "id": 12,
      "name": "Halle Berry"
    }
  ],
  "success": true
}
```

---

## Testing

In case if you want to run the test cases against separate DB use,

```bash
export DB_NAME="casting_test"
```

To deploy the tests, run

```bash
python test_app.py
```

or

```bash
python -m unittest test_app.py
```
