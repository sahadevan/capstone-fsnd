import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP, db

DB_PATH = os.getenv('DB_PATH', 'postgresql+psycopg2://postgres:admin@localhost:5432/casting_test')

CASTING_ASSISTANT_TOKEN = os.getenv('CASTING_ASSISTANT_TOKEN','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlLMGxKS1UtN0xjcndvT0RTbEUxdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nejV0amVmcDJxdzV0YTd1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDAzNDdmOWFkMmE1YTdjZTk5N2QzYTQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjc5NzU2NjIyLCJleHAiOjE2Nzk4NDMwMjIsImF6cCI6IlFEZ2xsMkt6NWxlZ2tvM3FxY1pPUXF2cG4wa3NvbEVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.OcG25OGgTu6mRzHECFZwE0S3stxWRVZLz0vwIwzSN3oVnfdTNbvEfU7e-RR0JdVS_3S3lBNYL1KWXfIaAme9KZN8O3W6YJSI2utsUwvi-M9J5UfOxH5mFo6y-9bKYG25KXyctQ10IBF7hKaiOTe7K94m45s7d-kc59lzizqLddRdCdaEqZxvyltlnzt7i3Vl0Hpn-b08_nsYgJl45-MlplCs87coMzvKDmGW6SoD6yq0rg6reuHsQGNtc6mSplrzxi-zz_mpNg9tiCCKV4SixJCaV2Y1pf42I1rXlbcvIWo-UwtQigrnu1GFaEnw5y5bMWf_a_hH8IE9Z1y01V1w-w')
CASTING_DIRECTOR_TOKEN = os.getenv('CASTING_DIRECTOR_TOKEN','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlLMGxKS1UtN0xjcndvT0RTbEUxdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nejV0amVmcDJxdzV0YTd1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzgxMzU5NDU5NzYwMjU4MDMzNSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Nzk3NTc1MDcsImV4cCI6MTY3OTg0MzkwNywiYXpwIjoiUURnbGwyS3o1bGVna28zcXFjWk9RcXZwbjBrc29sRWkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.iSX9KraYNEIU2geivck73Hjrqxd5LoH7BnN7kQzd7wxZ-X9OVF5qJ6YglhyRFuCyHWbskaYMDFX4PEpKFW_XtE5QxhPRDcCHJRT7xhnIWyAn1R3LJgOsERJJ5oGKYZudyLQENkJjemqtYP8a_9xpkZRUe3zGJdw5dXgFqOUdIAscjk4sHxguqARWNwD0ZC9NT_QJ7-UUyxU0BzWIGQc1hU8lQKSm6tzFOM8RrcFr_fOOpHQbgHI60pfpbANl2fDk1kgQzNMSg6nanNSBJTF8LCzfqPyZ0hT0BhVlYcDiovCwAP9tNd8lI1S5GngeWQD2ZRf6vBycNpBfX79CorVCGA')
EXECUTIVE_PRODUCER_TOKEN = os.getenv('EXECUTIVE_PRODUCER_TOKEN','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlLMGxKS1UtN0xjcndvT0RTbEUxdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nejV0amVmcDJxdzV0YTd1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwODI2MTk1NjE2MTk3MzY0MDM0MSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Nzk3NTYwMTMsImV4cCI6MTY3OTg0MjQxMywiYXpwIjoiUURnbGwyS3o1bGVna28zcXFjWk9RcXZwbjBrc29sRWkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.U8WSNuOiIS_3yOgwvUQ77JZ77J7V0-MJ6_90YL33dqxtABr7yB99RhCdyutlWfNYIC0RJgqnG-1BrVZC1fZ2q6Tejev3C0Vm-MDiUKcyxCq3bcVKBtyH386v3Zvnxx9u_Ni10ZpnHsEnUr0oz3B8FHd2Fe6-M3ZriqBCFpUB1ENXKPbMI8U2toFXqatm8D30W9sBEr9dOJv5pzmmvbTjPfMe6MysXmD-EVFQQgBudqZh3jQUtid2zuO9mIDvjNkMM26vVWh7nYP6zFC51fSZiD54wumcefShCMx5ZbLIw_47D4fP4_SQ2D5Zzmhj9LZS7Qx7aFQqxywTDyUdvCknug')

new_movie = { "title" : "Vaishnavi The Great", "release_date": "1987-04-08" }
update_movie = { "title" : "Sahadevan The Great", "release_date": "1988-11-05" }
new_actor = { "name" : "S.Kaavyazhini", "age": 2, "gender": "Female" }
update_actor = { "name" : "S.Nakshatra", "age": 2, "gender": "Female" }

class CastingTestCase(unittest.TestCase):
    
    def setUp(self):
        APP.config['TESTING'] = True
        self.client = APP.test_client
        # binds the app to the current context
        with APP.app_context():
            db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

# Casting Assistant Test Cases - GET movies, actors
    def test_get_movies_with_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        response = self.client().get('/movies', headers=headers)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_with_token_but_not_valid_HTTP_method(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        response = self.client().put('/movies', headers=headers)

        # Assert
        self.assertEqual(response.status_code, 405)

    def test_get_movies_without_token(self):
        # Arrange & Act
        response = self.client().get('/movies')
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_actors_with_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        response = self.client().get('/actors', headers=headers)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_with_token_but_not_valid_HTTP_method(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        response = self.client().put('/actors', headers=headers)

        # Assert
        self.assertEqual(response.status_code, 405)

    def test_get_actors_without_token(self):
        # Arrange & Act
        response = self.client().get('/actors')
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

# Executive Producer Test Cases CREATE DELETE UPDATE movies
    def test_create_movie_with_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        data = json.loads(json.dumps(new_movie))
        response = self.client().post('/movies', headers=headers, json=data)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_with_token_but_not_valid_HTTP_method(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        data = json.loads(json.dumps(new_movie))
        response = self.client().put('/movies', headers=headers, json=data)

        # Assert
        self.assertEqual(response.status_code, 405)

    def test_create_movie_without_token(self):
        # Arrange & Act
        data = json.loads(json.dumps(new_movie))
        response = self.client().post('/movies', json=data)

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_create_movie_with_invalid_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_DIRECTOR_TOKEN}"}
        data = json.loads(json.dumps(new_movie))
        response = self.client().post('/movies', headers=headers, json=data)

        # Assert
        self.assertEqual(response.status_code, 403)
    
    def test_delete_movie_with_token(self):
        # Arrange
        headers = {"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        data = json.loads(json.dumps(new_movie))
        response = self.client().post('/movies', headers=headers, json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        delete_id = data['movies'][0]['id']

        # Act
        response = self.client().delete(f'/movies/{delete_id}', headers=headers)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], delete_id)

    def test_delete_movie_without_token(self):
        # Arrange & Act
        response = self.client().delete('/movies/1')

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_delete_movie_with_invalid_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_DIRECTOR_TOKEN}"}
        response = self.client().delete(f'/movies/1', headers=headers)       

        # Assert
        self.assertEqual(response.status_code, 403)

    def test_update_movie_with_token(self):
        # Arrange
        headers = {"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        data = json.loads(json.dumps(new_movie))
        response = self.client().post('/movies', headers=headers, json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        update_id = data['movies'][0]['id']

        # Act
        response = self.client().patch(f'/movies/{update_id}', headers=headers, json=update_movie)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'][0]['id'], update_id)

    def test_update_movie_without_token(self):
        # Arrange & Act
        response = self.client().patch(f'/movies/1', json=update_movie)

        # Assert
        self.assertEqual(response.status_code, 401)

# Casting Director Test Cases CREATE DELETE UPDATE actors

    def test_create_actor_with_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_DIRECTOR_TOKEN}"}
        data = json.loads(json.dumps(new_actor))
        response = self.client().post('/actors', headers=headers, json=data)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_with_token_but_not_valid_HTTP_method(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_DIRECTOR_TOKEN}"}
        data = json.loads(json.dumps(new_actor))
        response = self.client().put('/actors', headers=headers, json=data)

        # Assert
        self.assertEqual(response.status_code, 405)

    def test_create_actor_without_token(self):
        # Arrange & Act
        data = json.loads(json.dumps(new_actor))
        response = self.client().post('/actors', json=data)

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_create_actor_with_invalid_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        data = json.loads(json.dumps(new_actor))
        response = self.client().post('/actors', headers=headers, json=data)

        # Assert
        self.assertEqual(response.status_code, 403)

    def test_delete_actor_with_token(self):
        # Arrange
        headers = {"Authorization": f"Bearer {CASTING_DIRECTOR_TOKEN}"}
        data = json.loads(json.dumps(new_actor))
        response = self.client().post('/actors', headers=headers, json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        delete_id = data['actors'][0]['id']

        # Act
        response = self.client().delete(f'/actors/{delete_id}', headers=headers)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], delete_id)

    def test_delete_actor_without_token(self):
        # Arrange & Act
        response = self.client().delete('/actors/1')

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_delete_actor_with_invalid_token(self):
        # Arrange & Act
        headers = {"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        response = self.client().delete(f'/actors/1', headers=headers)       

        # Assert
        self.assertEqual(response.status_code, 403)

    def test_update_actor_with_token(self):
        # Arrange
        headers = {"Authorization": f"Bearer {CASTING_DIRECTOR_TOKEN}"}
        data = json.loads(json.dumps(new_actor))
        response = self.client().post('/actors', headers=headers, json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        update_id = data['actors'][0]['id']

        # Act
        response = self.client().patch(f'/actors/{update_id}', headers=headers, json=update_actor)
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'][0]['id'], update_id)

    def test_update_actor_without_token(self):
        # Arrange & Act
        response = self.client().patch(f'/actors/1', json=update_actor)

        # Assert
        self.assertEqual(response.status_code, 401)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()