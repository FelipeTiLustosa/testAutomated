# DOCUMENTO DE CASO DE TESTE: CT-001.docx
# Testes de Autenticação (Login/Logout)

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class TestAutenticacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial antes dos testes."""
        print("\nIniciando testes de autenticação...")
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def setUp(self):
        """Preparação antes de cada teste."""
        self.driver.get("https://the-internet.herokuapp.com/login")
        time.sleep(1)

    def test_1_login_sucesso(self):
        """Teste de login com credenciais válidas."""
        print("\nExecutando teste de login com sucesso...")
        
        # Preenche credenciais válidas
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Verifica se login foi bem-sucedido
        mensagem = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.success"))
        )
        self.assertIn("You logged into a secure area!", mensagem.text)
        print("✓ Login realizado com sucesso")

    def test_2_login_falha(self):
        """Teste de login com credenciais inválidas."""
        print("\nExecutando teste de login com falha...")
        
        # Tenta login com senha incorreta
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("senhaerrada")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Verifica mensagem de erro
        mensagem = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.error"))
        )
        self.assertIn("Your password is invalid!", mensagem.text)
        print("✓ Mensagem de erro exibida corretamente")

    def test_3_logout(self):
        """Teste de logout após login bem-sucedido."""
        print("\nExecutando teste de logout...")
        
        # Realiza login primeiro
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Clica no botão de logout
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.secondary.radius"))
        ).click()

        # Verifica se voltou para página de login
        mensagem = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.success"))
        )
        self.assertIn("You logged out", mensagem.text)
        print("✓ Logout realizado com sucesso")

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes."""
        print("\nFinalizando testes de autenticação...")
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)