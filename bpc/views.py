import json
import time

import requests
import os

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import BpcExecution, BpcAtendimento
from taxpayers.models import Payer

@login_required
def consultar_bpc(request, payer_id):
    try:
        payer = Payer.objects.get(id=payer_id)
        execution = BpcExecution.objects.create(payer=payer)

        # Configurar o Selenium
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')

        selenium_profile_dir = os.path.join(os.path.expanduser('~'), 'selenium_profile')
        # Criar o diretório se não existir
        if not os.path.exists(selenium_profile_dir):
            os.makedirs(selenium_profile_dir)

        options.add_argument(f'--user-data-dir={selenium_profile_dir}')  # Define o perfil persistente
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')  # Abre o navegador maximizado
        options.add_argument('--disable-gpu')  # Pode melhorar a estabilidade em alguns sistemas
        options.add_argument('--ignore-certificate-errors')  # Evita erros de certificado
        options.add_argument('--disable-popup-blocking')  # Evita bloqueio de pop-ups
        options.add_argument('--remote-allow-origins=*')  # Evita erro em algumas versões do Chrome
        # Configurações experimentais para evitar detecção do Selenium
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(options=options)

        # Modificar o navigator.webdriver para evitar detecção
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            # Acessar o site do INSS
            driver.get('https://atendimento.inss.gov.br/')

            # Preencher CPF
            cpf_input = WebDriverWait(driver, 90).until(
                EC.element_to_be_clickable((By.ID, 'filtro-entidade-conveniada-cpf'))
            )

            time.sleep(0.5)
            cpf_input.clear()  # Limpar o campo antes de inserir
            cpf_input.send_keys(payer.cpf)

            time.sleep(1)
            # Clicar no botão de pesquisa
            search_button = driver.find_element(By.XPATH, '//*[@id="requerimento"]/div/div[3]/div[5]/button')
            search_button.click()

            # Aguardar resultados
            time.sleep(1)
            WebDriverWait(driver, 180).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.dtp-block-ui.unblocked'))
            )

            # Extrair dados da tabela de resultados
            time.sleep(0.5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            resultados = soup.find_all('tr', class_='dtp-table-wrapper-row')

            for resultado in resultados:
                protocolo = resultado.find_all('td')[0].text.strip()
                xpath_linha = f"//table[@class='table']//tr[./td[1][text()='{protocolo}']]"
                linha = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_linha))
                )
                button_details = linha.find_element(By.XPATH,'//button[@aria-label="Detalhar tarefa"]')

                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button_details)

                print(f"Botão 'Detalhar tarefa' do protocolo' {protocolo}' foi clicado")

                # Aguardar resultados
                time.sleep(0.5)
                WebDriverWait(driver, 180).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.dtp-block-ui.unblocked'))
                )

                # Extrair detalhes adicionais
                detalhes_soup = BeautifulSoup(driver.page_source, 'html.parser')
                detalhes = {}

                detalhamento = detalhes_soup.find('div', {'id': 'detalhamento'})

                # 1. Atendimento à Distância
                atendimento_section = detalhamento.find('section', {'class': 'dtp-datagrid'})
                if atendimento_section:
                    detalhes['atendimento'] = {
                        'servico': atendimento_section.find('label', text='Serviço').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'status': atendimento_section.find('label', text='Status').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'unidade_responsavel': atendimento_section.find('label', text='Unidade Responsável').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'unidade_protocolo': atendimento_section.find('label', text='Unidade de Protocolo').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip()
                    }

                # 2. Protocolo de Requerimento
                protocolo_section = atendimento_section.find_next('section', {'class': 'dtp-datagrid'})
                if protocolo_section:
                    detalhes['protocolo'] = {
                        'numero': protocolo_section.find('label', text='Protocolo').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'canal_requerente': protocolo_section.find('label', text='Canal do Requerente').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'data_solicitacao': protocolo_section.find('label', text='Data da Solicitação').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'data_protocolo': protocolo_section.find('label', text='Protocolado em').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'solicitante': protocolo_section.find('label', text='Solicitante').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'cpf_solicitante': protocolo_section.find('label', text='CPF do Solicitante').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip()
                    }

                # 3. Dados do Requerente
                requerente_section = protocolo_section.find_next('section', {'class': 'dtp-datagrid'})
                if requerente_section:
                    detalhes['requerente'] = {
                        'nome': requerente_section.find('label', text='Nome Completo').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'cpf': requerente_section.find('label', text='CPF').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'nascimento': requerente_section.find('label', text='Nascimento').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'email': requerente_section.find('label', text='E-mail').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'telefone_fixo': requerente_section.find('label', text='Telefone Fixo').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'celular': requerente_section.find('label', text='Celular').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip(),
                        'acompanha_processo': requerente_section.find('label', text='Acompanha processo?').find_next('span', {'class': 'dtp-datagrid-value'}).text.strip()
                    }

                # 4. Campos Adicionais
                campos_adicionais_section = requerente_section.find_next('section', {'class': 'dtp-datagrid'})
                if campos_adicionais_section:
                    campos_adicionais = {}
                    for item in campos_adicionais_section.find_all('div', {'class': 'dtp-datagrid-columns-item'}):
                        label = item.find('label', {'class': 'dtp-datagrid-label'})
                        value = item.find('span', {'class': 'dtp-datagrid-value'})
                        if label and value:
                            campos_adicionais[label.text.strip()] = value.text.strip()
                    detalhes['campos_adicionais'] = campos_adicionais

                # Extrair anexos
                anexos = []
                anexos_section = detalhes_soup.find('div', {'id': 'anexos'})
                if anexos_section:
                    for arquivo in anexos_section.find_all('div', {'class': 'get-painel-arquivo'}):
                        nome_arquivo = arquivo.find('div', {'class': 'get-painel-arquivo-apenas-nome'}).text.strip()
                        tipo_arquivo = arquivo.find('div', {'class': 'get-painel-arquivo-title'}).text.strip()
                        tamanho = arquivo.find('div', {'class': 'get-painel-arquivo-tamanho'}).text.strip()

                        anexos.append({
                            'nome': nome_arquivo,
                            'tipo': tipo_arquivo,
                            'tamanho': tamanho
                        })

                detalhes['anexos'] = anexos


                # Criar registro do atendimento
                BpcAtendimento.objects.create(
                    execution=execution,
                    protocolo=detalhes['protocolo']['numero'],
                    servico=detalhes['atendimento']['servico'],
                    situacao=detalhes['atendimento']['status'],
                    unidade_responsavel=detalhes['atendimento']['unidade_responsavel'],
                    unidade_protocolo=detalhes['atendimento']['unidade_protocolo'],
                    canal_requerente=detalhes['protocolo']['canal_requerente'],
                    data_solicitacao=datetime.strptime(detalhes['protocolo']['data_solicitacao'], '%d/%m/%Y'),
                    data_protocolo=datetime.strptime(detalhes['protocolo']['data_protocolo'], '%d/%m/%Y'),
                    solicitante=detalhes['protocolo']['solicitante'],
                    cpf_solicitante=detalhes['protocolo']['cpf_solicitante'],
                    nome_requerente=detalhes['requerente']['nome'],
                    cpf_requerente=detalhes['requerente']['cpf'],
                    data_nascimento=datetime.strptime(detalhes['requerente']['nascimento'], '%d/%m/%Y'),
                    email=detalhes['requerente']['email'],
                    telefone_fixo=detalhes['requerente']['telefone_fixo'],
                    celular=detalhes['requerente']['celular'],
                    acompanha_processo=detalhes['requerente']['acompanha_processo'].upper() == 'SIM',
                    campos_adicionais=detalhes['campos_adicionais'],
                    anexos=detalhes['anexos']
                )

                print(f"Criado BPC Atendimento do ' {protocolo}'")
                driver.back()

            execution.success = True
            execution.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            execution.success = False
            execution.error_message = str(e)
            execution.save()
            return JsonResponse({'status': 'error', 'message': str(e)})

        finally:
            driver.quit()

    except Payer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Contribuinte não encontrado'})