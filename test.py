import os
import unittest
import json

from app import create_app
from models import setup_db, studio, instructor

STUDIO_OWNER= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJEQ01EX1FncllPTXhBdmtTcWROciJ9.eyJpc3MiOiJodHRwczovL3RvbWFyaWtlbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViOWY3Yjc1MTM0NGUyMjE2NzUyMjZkIiwiYXVkIjoic3R1ZGlvcyIsImlhdCI6MTU4OTc0NzY5MiwiZXhwIjoxNTg5ODM0MDkyLCJhenAiOiI0QjJKWktOMlpzZ214eDNhN0E5MFJkc3ViZlRmaFZOQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmluc3RydWN0b3JzIiwiZGVsZXRlOnN0dWRpb3MiLCJnZXQ6aW5zdHJ1Y3RvcnMiLCJnZXQ6c3R1ZGlvcyIsInBhdGNoOmluc3RydWN0b3JzIiwicGF0Y2g6c3R1ZGlvcyIsInBvc3Q6aW5zdHJ1Y3RvcnMiLCJwb3N0OnN0dWRpb3MiXX0.Yo7PtPuo_s1cz6ggpG-lu0vstq8fsQN33TyTbUOQz0pr14oLc3nIjpMtIeov5bEtRSUpAmO4zMJh21qNIdL9He5C0Hk53CYnknwM9Lcrz0i3XQgVfNnT4fXajhegiwiU_NJ-uJJ_OJmcxapB5dIlEYTTGdppsG5U-gDlQZMeBZAovSvbtiQLAUOhGJQLyojtOmb-T0mOP-6cDk_i1nvEd7Bf_lbv8eQAs_rWh7LFgiAWVkZunOxOisylqXgB0bEiGWOOjgUotR6kWAlX52wLgbMo9gk1yFa3g9PnDWSldobi2kvjQFKOjnprcuDo7uC4bGvKMpUwtnCJeu6KaFD-Kg'
MANAGER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJEQ01EX1FncllPTXhBdmtTcWROciJ9.eyJpc3MiOiJodHRwczovL3RvbWFyaWtlbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViOWY3ZjI0ZjY5ZTEyMjU2ZmI0YjhkIiwiYXVkIjoic3R1ZGlvcyIsImlhdCI6MTU4OTc0Nzc3NCwiZXhwIjoxNTg5ODM0MTc0LCJhenAiOiI0QjJKWktOMlpzZ214eDNhN0E5MFJkc3ViZlRmaFZOQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmluc3RydWN0b3JzIiwiZ2V0Omluc3RydWN0b3JzIiwiZ2V0OnN0dWRpb3MiLCJwYXRjaDppbnN0cnVjdG9ycyIsInBhdGNoOnN0dWRpb3MiLCJwb3N0Omluc3RydWN0b3JzIl19.0xkQEnoKKfSWM59tU3XahkxxCwCDO5Q-gq0emFH6nxIdo6b0GMRIV8iAwmMJGgAGuP8Dnxwf1Ur0VSPniXpt9qjHD47t78E4mFv0irKuqsxCeBYV5AX2a2XdEZzPjSnZ--tvdbSICGJbN91oeIWJFdZ0DBmJNXXJ6bxKMfRZIznkK-_ur3eeEutgijz13jne2xFDh8U5hFGO8GNoYSCsY3QEg_SpzffiatDKCf0tUG59eOnT3iujNBKljg96l7eykV82SJNjxIafZ_TpUHNnk36Xm1aUFLhLesbFNqKaXpKoAAY2ChGJuEGvsPdrYrq2Mb-57Kb5_b-CQ9N2lZ39Mw'
ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJEQ01EX1FncllPTXhBdmtTcWROciJ9.eyJpc3MiOiJodHRwczovL3RvbWFyaWtlbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViOWY3ZGI0ZjY5ZTEyMjU2ZmI0YjI0IiwiYXVkIjoic3R1ZGlvcyIsImlhdCI6MTU4OTc0NzgyNiwiZXhwIjoxNTg5ODM0MjI2LCJhenAiOiI0QjJKWktOMlpzZ214eDNhN0E5MFJkc3ViZlRmaFZOQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Omluc3RydWN0b3JzIiwiZ2V0OnN0dWRpb3MiXX0.G1DGUe1GFH3GwPNTF0_DCeZZykUr7CuOdPGV3HY01B-8woJxqAqFaIhmqtw7iJCHazmwPFeoS_yr0jGkOFq8SDd8N0FqSiss-0OIUout2MijILPSMSXK5oXTA5hZXEYApFbSQ_cYMXMcXTiwBH8xiTRjjuS_96rqHlnKW8bMkPbNPHdzesnJmgGSfBHjCTmumt9A8ZsteQ_QBJcaC1ql4aEqtOdIxQpoAg48zbJAPXk8_pzqPGXmegeezCHV_6B3MJ7lbWZOOYiDj3ZsJnyHhWYJIt8rtT2vZi_nxlSSDzS23rCLvNdn0NH3MSzM1xYtOTkYouPfCixjGkt3tYNFSg'

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
            json={'name': 'David', 'age': 44, "gender": "male"},
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
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_instructor_401(self):
        response = self.client().post(
            '/instructors',
            json={'name': 'Jude', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /instructors
    def test_edit_instructor(self):
        response = self.client().patch(
            '/instructors/2',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
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
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + MANAGER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_instructor_404(self):
        response = self.client().patch(
            '/instructors/50000',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
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
