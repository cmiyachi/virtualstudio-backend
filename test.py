import os
import unittest
import json

from app import create_app
from models import setup_db, studio, instructor

STUDIO_OWNER= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJEQ01EX1FncllPTXhBdmtTcWROciJ9.eyJpc3MiOiJodHRwczovL3RvbWFyaWtlbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViOWY3Yjc1MTM0NGUyMjE2NzUyMjZkIiwiYXVkIjoic3R1ZGlvcyIsImlhdCI6MTU4OTkzNzQ4MSwiZXhwIjoxNTkwMDIzODgxLCJhenAiOiI0QjJKWktOMlpzZ214eDNhN0E5MFJkc3ViZlRmaFZOQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmluc3RydWN0b3JzIiwiZGVsZXRlOnN0dWRpb3MiLCJnZXQ6aW5zdHJ1Y3RvcnMiLCJnZXQ6c3R1ZGlvcyIsInBhdGNoOmluc3RydWN0b3JzIiwicGF0Y2g6c3R1ZGlvcyIsInBvc3Q6aW5zdHJ1Y3RvcnMiLCJwb3N0OnN0dWRpb3MiXX0.wDT3NqQuq69KwOz7aqaMWUfN4_8tdVf4wZcP1W1S238ZhUk10LjqdXgubLUiPUP8h63JXSsvCVMPRqmqopZSz10w0d4PobeH9n8Ff45c2nA5aizPmdMOqKd-xI83VXGBP2rHBa2e_bMJO1E2FyTF2epusiUbV_dHx1BCNd9_Qa2YKUoVHc2stqhUZkG_KQd4Dvu_qC0ilPx0xcrk2oQSUthmMiyzcnPvCJTuVWrchSHPB6JJgptQ1JWOj-38Gd_Jiv1PtnOuvHcbgQlTDsw-aHGrgP-HC29fOZPacVnmbTgN-av10RV2jy3msp9EVGrpNEooLb820V-_5q68JustAA'
MANAGER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJEQ01EX1FncllPTXhBdmtTcWROciJ9.eyJpc3MiOiJodHRwczovL3RvbWFyaWtlbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViOWY3ZjI0ZjY5ZTEyMjU2ZmI0YjhkIiwiYXVkIjoic3R1ZGlvcyIsImlhdCI6MTU4OTkzNzM5NywiZXhwIjoxNTkwMDIzNzk3LCJhenAiOiI0QjJKWktOMlpzZ214eDNhN0E5MFJkc3ViZlRmaFZOQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmluc3RydWN0b3JzIiwiZ2V0Omluc3RydWN0b3JzIiwiZ2V0OnN0dWRpb3MiLCJwYXRjaDppbnN0cnVjdG9ycyIsInBhdGNoOnN0dWRpb3MiLCJwb3N0Omluc3RydWN0b3JzIl19.eMa79HWG94kEe1CSl7BTV3vXMsejuZ3Spi10Ar3Su42gdhl6THlNXUEyJ40s8UvYT0lwUxJFf-yMPYCByTxMVNAj9au0GwPnrKgKRHknZXTRHc86riZGq93g-LdY8sgC5MQ9Y-y9W3yBBavSg2bERff5DLKv8Fw-1j1Vdt9ejhnKUtbXVOCcclLvikLLluqhhKrcV_0R_GwFeQOfAw1F5iWwPdTCWvrp73Mi5Hnn81iNni40ButKUoV5R4V3HInXjRf-lhGzW0coPsyJ8jrpt5oRBzVD0MI65DMD8JEGa3YjSLBkBQw68C5cO8MU0yUpyzJky33REv-jJdlqq9RlNA'
ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJEQ01EX1FncllPTXhBdmtTcWROciJ9.eyJpc3MiOiJodHRwczovL3RvbWFyaWtlbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViOWY3ZGI0ZjY5ZTEyMjU2ZmI0YjI0IiwiYXVkIjoic3R1ZGlvcyIsImlhdCI6MTU4OTkzNzM1MCwiZXhwIjoxNTkwMDIzNzUwLCJhenAiOiI0QjJKWktOMlpzZ214eDNhN0E5MFJkc3ViZlRmaFZOQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Omluc3RydWN0b3JzIiwiZ2V0OnN0dWRpb3MiXX0.NuP05BTNhvIUfiJuIyZ9tsjjetI2-SZ7wxzxQq-oZ_WyRuEP6j-wJhYWDmt5LSrR8IiKM1QaOcD1CDuJvHlTbhvY1K9oFpTZ3m85c2Ji9WUC4-WW8fdDBqyPgpWGb4NYxty8gCS7UEod7ia8wmsKW5H28-1XyNtxDDnh0-NMSiR3wcSD6SleyZCbPVdpTh80PXYR8Q0FzKeOUD8Ena_fIQsJSxjoQRQ1vd8IQsNk44722_bvjVYDfJK_4nvpv0ZrWMqz99mHniYSMal8c94J2Tpb2EZDtb1nVEdDiudwb3XtnK7t7cgxzm7g8_oGFKBT0MmxkqSl7Gw0U87D96vL3A'

class MHTestCase(unittest.TestCase):
    """This class represents the studios-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    #  GET /studios
    def test_get_studios(self):
        response = self.client().get(
            '/studios',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['studios'])

    # GET /studios/id
    def test_get_studio_by_id(self):
        response = self.client().get(
            '/studios/1',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['studio'])
        self.assertEqual(data['studio']['bizname'], 'Artemis Yoga')

    def test_get_studio_by_id_404(self):
        response = self.client().get(
            '/studios/10000',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /studios
    def test_post_studio(self):
        response = self.client().post(
            '/studios',
            json={'bizname': 'Charleston Yoga', 'opening_date': "1981-02-19"},
            headers={"Authorization": "Bearer " + STUDIO_OWNER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'studio added')
        self.assertEqual(data['studio']['bizname'], 'Charleston Yoga')

    def test_post_studio_400(self):
        response = self.client().post(
            '/studios',
            json={'bizname': '', 'opening_date': ""},
            headers={"Authorization": "Bearer " + STUDIO_OWNER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_studio_401(self):
        response = self.client().post(
            '/studios',
            json={'bizname': 'Wrong studio', 'opening_date': "1984-01-23"},
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /studios
    def test_edit_studio(self):
        response = self.client().patch(
            '/studios/2',
            json={'bizname': 'Crossfit', 'opening_date': "2018-10-12"},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'studio updated')
        self.assertEqual(data['studio']['bizname'], 'Crossfit')

    def test_edit_studio_400(self):
        response = self.client().patch(
            '/studios/1',
            json={'bizname': '', 'opening_date': ""},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_studio_404(self):
        response = self.client().patch(
            '/studios/50000',
            json={'bizname': 'Kendal Crossfit', 'opening_date': "2019-11-12"},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /studios/id
    def test_delete_studio(self):
        response = self.client().delete(
            '/studios/3',
            headers={"Authorization": "Bearer " + STUDIO_OWNER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'studio deleted')

    def test_delete_studio_404(self):
        response = self.client().delete(
            '/studios/110000',
            headers={"Authorization": "Bearer " + STUDIO_OWNER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_studio_401(self):
        response = self.client().delete(
            '/studios/1',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')


    # ==========================================================================================================
    #  GET /instructors
    def test_get_instructors(self):
        response = self.client().get(
            '/instructors',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['instructors'])

    # GET /instructors/id
    def test_get_instructor_by_id(self):
        response = self.client().get(
            '/instructors/1',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['instructor'])
        self.assertEqual(data['instructor']['name'], 'Chris Miyachi')

    def test_get_instructor_by_id_404(self):
        response = self.client().get(
            '/instructors/10000',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /instructors
    def test_post_instructor(self):
        response = self.client().post(
            '/instructors',
            json={'name': 'David', 'age': 44, "gender": "male","class_type":"hiit"},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'instructor added')
        self.assertEqual(data['instructor']['name'], 'David')

    def test_post_instructor_400(self):
        response = self.client().post(
            '/instructors',
            json={'name': '', 'age': '', "gender": "", "class_type": ""},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_instructor_401(self):
        response = self.client().post(
            '/instructors',
            json={'name': 'Jude', 'age': 44, "gender": "male","class_type":"kickbox"},
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /instructors
    def test_edit_instructor(self):
        response = self.client().patch(
            '/instructors/2',
            json={'name': 'Cynthia', 'age': 27, "gender": "female","class_type":"crossfit"},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'instructor updated')
        self.assertEqual(data['instructor']['name'], 'Cynthia')

    def test_edit_instructor_400(self):
        response = self.client().patch(
            '/instructors/2',
            json={'name': '', 'age': '', "gender": "", "class_type": ""},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_instructor_404(self):
        response = self.client().patch(
            '/instructors/50000',
            json={'name': 'Cynthia', 'age': 27, "gender": "female","class_type":"crossfit"},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /instructors/id
    def test_delete_instructor(self):
        response = self.client().delete(
            '/instructors/3',
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'instructor deleted')

    def test_delete_instructor_404(self):
        response = self.client().delete(
            '/instructors/110000',
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_instructor_401(self):
        response = self.client().delete(
            '/instructors/1',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
