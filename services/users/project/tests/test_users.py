import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Testes para o Service de Users."""

    def test_users(self):
        """Garante que a rota /ping se comporta corretamente"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """
        Garante que um novo usuário possa ser adicionado ao banco de dados.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('michael@mherman.org was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Garante error is thrown if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Garante um erro é jogado se o JSON não tiver a chave username"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'michael@mherman.org'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Garante que um erro é jogado se o email ja existir."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org'
                }),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Garante que o pegar um único usuário de comporta corretamente."""
        user = add_user('michael', 'michael@mherman.org')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@mherman.org', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Garante que um erro é jogado se id não é fornecido."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Garante que um erro é jogado se o id não existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Garante que listar todos usuários se comporta corretamente."""
        add_user('michael', 'michael@mherman.org')
        add_user('fletcher', 'fletcher@notreal.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('michael', data['data']['users'][0]['username'])
            self.assertIn(
                'michael@mherman.org', data['data']['users'][0]['email'])
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn(
                'fletcher@notreal.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Garantir que a rota principal se comporta corretamente quando não há
        usuários no banco."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos Usuarios', response.data)
        self.assertIn(b'<p>Sem usuarios!</p>', response.data)

    def test_main_with_users(self):
        """Garantir que a rota principal se comporta corretamente quando há
        usuários no banco."""
        add_user('michael', 'michael@mherman.org')
        add_user('fletcher', 'fletcher@notreal.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos Usuarios', response.data)
            self.assertNotIn(b'<p>Sem usuarios!</p>', response.data)
            self.assertIn(b'michael', response.data)
            self.assertIn(b'fletcher', response.data)

    def teste_main_add_user(self):
        """Garantir que um novo usuário pode ser adicionado ao banco de dados
        por um POST."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='michael', email='michael@sonotreal.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos Usuarios', response.data)
            self.assertNotIn(b'<p>Sem usuarios!</p>', response.data)
            self.assertIn(b'michael', response.data)


if __name__ == '__main__':
    unittest.main()
