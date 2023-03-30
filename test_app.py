import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP, db

DB_PATH = os.getenv('DB_PATH', 'postgresql+psycopg2://postgres@localhost:5432/casting_test')

CASTING_ASSISTANT_TOKEN = os.getenv('CASTING_ASSISTANT_TOKEN','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlLMGxKS1UtN0xjcndvT0RTbEUxdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nejV0amVmcDJxdzV0YTd1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDAzNDdmOWFkMmE1YTdjZTk5N2QzYTQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjgwMTkzOTkwLCJleHAiOjE2ODAyODAzOTAsImF6cCI6IlFEZ2xsMkt6NWxlZ2tvM3FxY1pPUXF2cG4wa3NvbEVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.UdCCq_PYHnpVxhFy72eyzJojLTz2qZZMgEHL0sfP4oSRHZTcZ-LNHimHWxwzPELCTVdR0He2caRGn8UGCh3GRQd2P3SFG8QE_qP-xxq_1TX-6gYpgLzZWbtlAPMJz3Xcrfg82kGjqLg7iYlcoP4yZ1i0rblSc3tmGSUvSwKHEvsDo0arhYQivlo4rxTHozHl6FOYlBCgm-89MZCuZ9sfDZSqaJf2FtB_7bhfMEdQ8IgPmU-yq5DrguXQNXlLKtXrMxydQ8UNgTVoiUvr40okcis5gnlSMmqREawQjVNn9kqgQr2FkUU3DJN7vT4PNWXTDNrzbEML9D9mh3dB-d4MJA')
CASTING_DIRECTOR_TOKEN = os.getenv('CASTING_DIRECTOR_TOKEN','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlLMGxKS1UtN0xjcndvT0RTbEUxdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nejV0amVmcDJxdzV0YTd1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzgxMzU5NDU5NzYwMjU4MDMzNSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2ODAxOTM2MTcsImV4cCI6MTY4MDI4MDAxNywiYXpwIjoiUURnbGwyS3o1bGVna28zcXFjWk9RcXZwbjBrc29sRWkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.iqOGHosZkRRpOuLzUiwDArrUEw-0Dzwfn0rux_TucerokTM-pPgjAjSRQeMrJIlWTtBGlKVKenjCrW1O2c4PdEjClQhQ1R-en0P7VCLEOEwnbUlFM3teEMcjtNHE_s2MmWhKWZTgYI5Bziwz2sS-_W_1iQT7rShg2fpij9AxoUiU_6GwVAzeRe4pnBDnXSNyj6N7SlZXlX_vudGrbKMkZ978FlmUK0Rr0Wo-9wav0fNhISrkC6hrWRAM5SYB8EVWrXEWLE0etAZ4GwsFtVHaittaapLWBqipVD_WpLidlac7KjdBCPK_d3mYCSgbiiVeRvsW2hlsYKsPYIfx9XGxww')
EXECUTIVE_PRODUCER_TOKEN = os.getenv('EXECUTIVE_PRODUCER_TOKEN','eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlLMGxKS1UtN0xjcndvT0RTbEUxdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nejV0amVmcDJxdzV0YTd1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwODI2MTk1NjE2MTk3MzY0MDM0MSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2ODAxOTM4MDQsImV4cCI6MTY4MDI4MDIwNCwiYXpwIjoiUURnbGwyS3o1bGVna28zcXFjWk9RcXZwbjBrc29sRWkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Me0VxmmpN6hU9PMCYotAPBlnVUSpvfWkHt8XfV8ec8KSuM_f3W05blNPGjSnTkH_FRBbNzm3IiCjhAeoZXNtJL8xsPpaweY8rP11rbdajznRUKYnAxeW9wbeioSdF8c6coL-DwUww7_TapY-c7kfNAgNvO6onDO_Ib0cm0McUK4AiY6v_evU6GBX6Uzl4RXItD3HhpCJpLz4zxhjPHg3I-YE2H_rfDNEJFxzW5F_DmzbcO2g3tMFwMvaHQJnvgqtL0wmOgaZ-QNyHmH4las55BZboe_jgbjHKIaUovgG-Ktimluur_PPEH6J0pOA1He_ZKVBHsOa2E9GhrkDMPZpfg')

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