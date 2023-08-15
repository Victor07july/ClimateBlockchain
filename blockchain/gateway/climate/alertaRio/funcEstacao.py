from bs4 import BeautifulSoup
import requests

# https://www.reddit.com/r/learnpython/comments/f4v9ex/bs4_looping_through_table/
# https://python-forum.io/thread-27991.html
# https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup

def getEstacao(URL, idEstacao):

    # faz o request da url
    response = requests.get(URL)
    print(response.status_code)

    # pega o conteúdo e faz o parse
    soup = BeautifulSoup(response.content, 'lxml')

    # seletores CSS
    tabelaPrecipitacao = soup.select_one('body > table:nth-child(2) > tbody:nth-child(2)') 
    tabelaDados = soup.select_one('body > table:nth-child(3) > tbody:nth-child(2)')

    # horário de atualização
    ultimaAtualizacao = soup.select_one('body > p:nth-child(1) > font:nth-child(1)')
    #print(ultimaAtualizacao.text)

    #idEstacao = input("Insira o ID da estação: ")

    td_list = []
    linhaPrecipitacao = []
    linhaDados = []

    # flag para saber se o número foi encontrado
    flag = False

    for tr in tabelaPrecipitacao.find_all('tr'):
        #td_list.append(tr.find_all('td')[0].text.strip())

        if tr.find_all('td')[0].text.strip() == str(idEstacao):
            flag = True
            #linhaPrecipitacao.append(tr.get_text(", ", strip=True))                
            
            # pega todos os elementos <td> dentro de <tr>, itera sobre eles e insere em uma array
            tds = tr.find_all('td')     
            for td in tds:
                linhaPrecipitacao.append(td.get_text())
            print(f"Dados de precipitação para a estação {idEstacao}, {tr.find_all('td')[1].text.strip()}: ")
            print(linhaPrecipitacao)
            print(f"TESTE: {linhaPrecipitacao[2]}")


    if not flag:
        print("Esta estação não está disponível na tabela de dados de precipitação.")
        print("Os seguintes ID's estão disponíveis na tabela de precipitação: ")
        for tr in tabelaPrecipitacao.find_all('tr'):
           print(tr.find_all('td')[0].text.strip(), end=' | ')
        print(' ')


    print('----------' * 3)

    # reseta a flag e td_list
    flag = False
    td_list = []

    for tr in tabelaDados.find_all('tr'):

        if tr.find_all('td')[0].text.strip() == idEstacao:
            flag = True
            
            tds = tr.find_all('td')        
            for td in tds:
                linhaDados.append(td.get_text())
            print(f"Dados meteorológicos para a estação {idEstacao}, {tr.find_all('td')[1].text.strip()}")
            print(linhaDados)


    if not flag:
        print("Esta estação não está disponível na tabela de dados meteorológicos.")
        print("Os seguintes ID's estão disponíveis na tabela de dados meteorológicos: ")
        for tr in tabelaDados.find_all('tr'):
            print(tr.find_all('td')[0].text.strip(), end=' | ')
        print(' ')

    return(linhaPrecipitacao, linhaDados, ultimaAtualizacao.text)

#URL = "http://alertario.rio.rj.gov.br/upload/TempoReal.html"
#getEstacao(URL, 9)