import os
import tempfile
import unittest
from app import create_app

class TesteCadastro(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.app = create_app({'TESTING': True, 'DATABASE': os.path.join(self.tmp.name, 'teste.db')})
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def cadastrar(self, nome='Ana Silva', email='ana@exemplo.com'):
        return self.client.post('/criar', data={'nome':nome,'email':email,'telefone':'61999999999'}, follow_redirects=True)

    def test_criar_e_listar(self):
        r = self.cadastrar()
        self.assertIn(b'Ana Silva', r.data)

    def test_nome_invalido(self):
        r = self.cadastrar(nome='A')
        self.assertIn('Informe um nome'.encode(), r.data)

    def test_email_duplicado(self):
        self.cadastrar()
        r = self.cadastrar(nome='Outra Pessoa')
        self.assertIn('já está cadastrado'.encode(), r.data)

    def test_editar(self):
        self.cadastrar()
        r = self.client.post('/editar/1', data={'nome':'Ana Atualizada','email':'ana@exemplo.com','telefone':''}, follow_redirects=True)
        self.assertIn(b'Ana Atualizada', r.data)

    def test_excluir(self):
        self.cadastrar()
        r = self.client.post('/excluir/1', follow_redirects=True)
        self.assertNotIn(b'Ana Silva', r.data)

    def test_registro_inexistente(self):
        self.assertEqual(self.client.get('/editar/999').status_code, 404)

if __name__ == '__main__':
    unittest.main()
