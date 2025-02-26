# DOCUMENTO DE CASO DE TESTE: CT-005.docx
# Testes de Adicionar/Remover Elementos

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAddRemoveElements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configura o WebDriver, maximiza a janela e abre a página de teste."""
        print("Iniciando o navegador...")
        cls.driver = webdriver.Chrome()  # Certifique-se de que o chromedriver compatível esteja no PATH
        cls.driver.maximize_window()
        cls.driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
        cls.wait = WebDriverWait(cls.driver, 10)

    def test_add_elements(self):
        """Teste 1: Verificar a adição de elementos ao clicar no botão 'Add Element'."""
        driver = self.driver
        wait = self.wait

        # Localiza o botão "Add Element"
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
        
        # Número de cliques a realizar
        num_clicks = 5
        print(f"\nClicando {num_clicks} vezes no botão 'Add Element'...")
        for i in range(num_clicks):
            add_button.click()
            time.sleep(0.5)  # Pequena pausa para garantir que o elemento seja adicionado

        # Verifica se o número de botões "Delete" é igual a num_clicks
        delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Delete']")
        atual = len(delete_buttons)
        self.assertEqual(atual, num_clicks, f"Esperado {num_clicks} botões Delete, mas encontrado {atual}")
        print(f"✓ {num_clicks} botões 'Delete' foram adicionados com sucesso.")

    def test_remove_element(self):
        """Teste 2: Verificar a remoção de um elemento após clicar no botão 'Delete'."""
        driver = self.driver
        wait = self.wait

        # Reinicia a página para ter um estado limpo
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
        time.sleep(1)

        # Adiciona 3 elementos para o teste de remoção
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
        num_clicks = 3
        print(f"\nAdicionando {num_clicks} elementos para o teste de remoção...")
        for i in range(num_clicks):
            add_button.click()
            time.sleep(0.5)
        
        # Verifica quantos botões "Delete" existem
        delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Delete']")
        initial_count = len(delete_buttons)
        print(f"Inicialmente, {initial_count} botões 'Delete' estão presentes.")
        self.assertEqual(initial_count, num_clicks, f"Esperado {num_clicks} botões, mas encontrado {initial_count}")

        # Remove o primeiro botão "Delete"
        print("Clicando no primeiro botão 'Delete' para removê-lo...")
        delete_buttons[0].click()
        time.sleep(1)  # Aguarda um pouco para a remoção ser processada

        # Verifica a nova quantidade de botões "Delete"
        new_delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Delete']")
        new_count = len(new_delete_buttons)
        self.assertEqual(new_count, initial_count - 1, f"Após remoção, esperado {initial_count - 1} botões, mas encontrado {new_count}")
        print(f"✓ Um botão 'Delete' removido com sucesso, total agora: {new_count}.")

    @classmethod
    def tearDownClass(cls):
        """Fecha o navegador após a execução dos testes."""
        print("\nFechando o navegador...")
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2)