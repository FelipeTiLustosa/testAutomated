# DOCUMENTO DE CASO DE TESTE: CT-003.docx
# Testes de Formulários (Preenchimento e Validação)

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class TestFormularios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial antes dos testes."""
        print("\nIniciando testes de formulários...")
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def setUp(self):
        """Preparação antes de cada teste."""
        self.driver.get("https://ultimateqa.com/filling-out-forms/")
        time.sleep(2)  # Aguarda carregamento da página

    def test_1_envio_correto(self):
        """Teste de envio de formulário com dados corretos."""
        print("\nExecutando teste de envio correto do formulário...")
        
        # Preenche o formulário com dados válidos
        self.driver.find_element(By.ID, "et_pb_contact_name_0").send_keys("João Silva")
        self.driver.find_element(By.ID, "et_pb_contact_message_0").send_keys("Mensagem de teste automatizado")
        
        # Clica no botão de enviar
        self.driver.find_element(By.NAME, "et_builder_submit_button").click()
        
        # Verifica mensagem de sucesso
        time.sleep(2)
        mensagem = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "et-pb-contact-message"))
        )
        self.assertIn("Thanks for contacting us", mensagem.text)
        print("✓ Formulário enviado com sucesso")

    def test_2_campos_vazios(self):
        """Teste de envio de formulário com campos vazios."""
        print("\nExecutando teste de envio com campos vazios...")
        
        # Tenta enviar formulário sem preencher nada
        self.driver.find_element(By.NAME, "et_builder_submit_button").click()
        
        # Verifica mensagens de erro
        time.sleep(2)
        campos_erro = self.driver.find_elements(By.CLASS_NAME, "et_contact_error")
        self.assertTrue(len(campos_erro) > 0, "Nenhum campo com erro encontrado")
        
        # Verifica se há mensagem específica para campos obrigatórios
        mensagem = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "et-pb-contact-message"))
        )
        self.assertIn("Please, fill in the following fields", mensagem.text)
        self.assertTrue("Name" in mensagem.text and "Message" in mensagem.text)
        print("✓ Validação de campos obrigatórios funcionando")

    def test_3_preenchimento_parcial(self):
        """Teste de envio com apenas um campo preenchido."""
        print("\nExecutando teste de preenchimento parcial...")
        
        # Preenche apenas o campo nome
        self.driver.find_element(By.ID, "et_pb_contact_name_0").send_keys("João Silva")
        
        # Envia o formulário
        self.driver.find_element(By.NAME, "et_builder_submit_button").click()
        
        # Verifica mensagem de erro
        time.sleep(2)
        mensagem = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "et-pb-contact-message"))
        )
        self.assertIn("Please, fill in the following fields", mensagem.text)
        self.assertIn("Message", mensagem.text)
        print("✓ Validação de preenchimento parcial funcionando")

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes."""
        print("\nFinalizando testes de formulários...")
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)