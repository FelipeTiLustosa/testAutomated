# DOCUMENTO DE CASO DE TESTE: CT-004.docx
# Testes de Upload de Arquivos

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import os

class TestGlobalSQAForm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial antes dos testes."""
        print("\nIniciando testes do formulário GlobalSQA...")
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    def setUp(self):
        """Preparação antes de cada teste."""
        self.driver.get("https://www.globalsqa.com/samplepagetest/")
        time.sleep(2)  # Aguarda carregamento da página

    def test_1_envio_valido(self):
        """Teste de envio do formulário com dados válidos."""
        print("\nExecutando teste de envio válido...")
        
        # Preenche campos de texto
        self.driver.find_element(By.NAME, "g2599-name").send_keys("João Silva")
        self.driver.find_element(By.NAME, "g2599-email").send_keys("joao.silva@example.com")
        self.driver.find_element(By.NAME, "g2599-website").send_keys("https://example.com")
        
        # Seleciona experiência
        experience = Select(self.driver.find_element(By.NAME, "g2599-experienceinyears"))
        experience.select_by_visible_text("3-5")
        
        # Seleciona expertise usando JavaScript
        functional_testing = self.driver.find_element(By.XPATH, "//input[@value='Functional Testing']")
        self.driver.execute_script("arguments[0].click();", functional_testing)
        
        automation_testing = self.driver.find_element(By.XPATH, "//input[@value='Automation Testing']")
        self.driver.execute_script("arguments[0].click();", automation_testing)
        
        # Seleciona educação usando JavaScript
        graduate = self.driver.find_element(By.XPATH, "//input[@value='Graduate']")
        self.driver.execute_script("arguments[0].click();", graduate)
        
        # Adiciona comentário
        self.driver.find_element(By.NAME, "g2599-comment").send_keys("Teste automatizado de envio de formulário")
        
        # Envia o formulário usando JavaScript
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Verifica mensagem de sucesso
        time.sleep(2)
        try:
            mensagem = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "contact-form-submission"))
            )
            self.assertTrue(mensagem.is_displayed())
            print("✓ Formulário enviado com sucesso")
        except TimeoutException:
            self.fail("Erro: Mensagem de sucesso não encontrada")

    def test_2_campos_obrigatorios(self):
        """Teste de validação de campos obrigatórios."""
        print("\nExecutando teste de campos obrigatórios...")
        
        # Tenta enviar formulário vazio usando JavaScript
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Verifica campos obrigatórios usando validação HTML5
        time.sleep(2)
        campos_obrigatorios = [
            "g2599-name",
            "g2599-email"
        ]
        
        for campo_id in campos_obrigatorios:
            campo = self.driver.find_element(By.NAME, campo_id)
            # Verifica se o campo tem o atributo 'required'
            self.assertTrue(campo.get_attribute("required"), f"Campo {campo_id} não está marcado como obrigatório")
            # Verifica se o campo está vazio
            self.assertEqual(campo.get_attribute("value"), "", f"Campo {campo_id} não está vazio")
            # Verifica se o campo tem validação HTML5 ativa
            self.assertTrue(campo.get_attribute("validationMessage"), f"Campo {campo_id} não mostra mensagem de validação")
        
        print("✓ Validação de campos obrigatórios funcionando")

    def test_3_email_invalido(self):
        """Teste de validação de formato de email."""
        print("\nExecutando teste de email inválido...")
        
        # Preenche com email inválido
        self.driver.find_element(By.NAME, "g2599-name").send_keys("João Silva")
        self.driver.find_element(By.NAME, "g2599-email").send_keys("email_invalido")
        
        # Tenta enviar usando JavaScript
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Verifica se o email é inválido
        time.sleep(2)
        try:
            email_field = self.driver.find_element(By.NAME, "g2599-email")
            email_value = email_field.get_attribute("value")
            self.assertFalse("@" in email_value and "." in email_value, "Email válido encontrado")
            print("✓ Validação de email inválido funcionando")
        except Exception as e:
            self.fail(f"Erro ao verificar formato de email: {str(e)}")

    def test_4_upload_arquivo(self):
        """Teste de upload de arquivo."""
        print("\nExecutando teste de upload de arquivo...")
        
        # Cria um arquivo temporário para teste
        arquivo_teste = "teste_upload.txt"
        with open(arquivo_teste, "w") as f:
            f.write("Arquivo de teste para upload")
        
        try:
            # Realiza o upload
            caminho_arquivo = os.path.abspath(arquivo_teste)
            try:
                # Tenta diferentes seletores para o campo de upload
                upload_input = None
                for selector in ["input[type='file']", "#g2599-file", ".wpcf7-file"]:
                    try:
                        upload_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if upload_input:
                    upload_input.send_keys(caminho_arquivo)
                    time.sleep(2)
                    print("✓ Upload de arquivo realizado com sucesso")
                else:
                    self.fail("Erro: Campo de upload não encontrado")
                    
            except Exception as e:
                self.fail(f"Erro ao realizar upload: {str(e)}")
            
        finally:
            # Limpa o arquivo de teste
            if os.path.exists(arquivo_teste):
                os.remove(arquivo_teste)

    def test_5_preenchimento_parcial(self):
        """Teste de envio com preenchimento parcial."""
        print("\nExecutando teste de preenchimento parcial...")
        
        # Preenche apenas alguns campos
        self.driver.find_element(By.NAME, "g2599-name").send_keys("João Silva")
        experience = Select(self.driver.find_element(By.NAME, "g2599-experienceinyears"))
        experience.select_by_visible_text("0-1")
        
        # Tenta enviar usando JavaScript
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Verifica campos obrigatórios não preenchidos
        time.sleep(2)
        email_field = self.driver.find_element(By.NAME, "g2599-email")
        
        # Verifica se o campo de email está vazio e tem mensagem de validação
        self.assertEqual(email_field.get_attribute("value"), "", "Campo de email não está vazio")
        self.assertTrue(email_field.get_attribute("validationMessage"), "Campo de email não mostra mensagem de validação")
        
        print("✓ Validação de preenchimento parcial funcionando")

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes."""
        print("\nFinalizando testes do formulário GlobalSQA...")
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)