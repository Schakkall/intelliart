'''
    Este módulo transforma os dados em formato json para inserts sql
'''
#!/usr/bin/env python
import json

INPUT_FILE_NAME = 'votacoes_proposicoes.json'
# Logging file
LOGGING_FILE_NAME = 'output.txt'

OUTPUT_FILE = {
    'votacoes': 'votacoes.sql',
    'proposicoes': 'proposicoes.sql',
    'votos': 'votos.sql',
    'orientacao_bancada': 'orientacao_bancada.sql'}


def load_data(input_file_name):
    '''
        Returns a JSON object from a file
    '''
    with open(input_file_name, 'r') as input_file:
        stream = ''
        for line in input_file:
            stream += line
        input_file.close()
        database = json.loads(stream)
        del stream
        return database


def write_file(string, file_path):
    with open(file_path, 'w') as output_file:
        output_file.write(string)
        output_file.close()


def proposicoes_to_sql(database):
    '''
        Saves a SQL insert DML script into output_file and returns de number of elements
    '''

    sql = '''
INSERT INTO 
    public.tb_proposicoes(
           ano, numero, sigla)
    VALUES ({ano}, {numero}, \'{sigla}\');
'''
    votacoes_file = open(OUTPUT_FILE['votacoes'], 'w')
    votos_file = open(OUTPUT_FILE['votos'], 'w')
    orientacao_bancada_file = open(OUTPUT_FILE['orientacao_bancada'], 'w')
    with open(OUTPUT_FILE['proposicoes'], 'w') as output_file:
        prop_number = 0
        for prop in database:
            output_file.write(sql.format(
                ano=prop['ano'], numero=prop['numero'], sigla=prop['sigla']))
            votacoes_to_sql(prop['votacoes'], prop_number,
                            votacoes_file, votos_file)
            prop_number += 1
        output_file.close()
        votacoes_file.close()
        votos_file.close()
    return prop_number


def votacoes_to_sql(database, master_id, output_file, votos_file):
    '''
        Saves a SQL insert DML script into output_file and returns de number of elements
    '''

    sql = '''
INSERT INTO public.tb_votacoes(
            proposicao, cod_sessao, data, hora, obj_votacao, resumo)
    VALUES ({proposicao}, {cod_sessao}, \'{data}\', \'{hora}\', \'{obj_votacao}\', \'{resumo}\');
'''
    vot_number = 0
    for votacao in database:
        output_file.write(sql.format(proposicao=master_id, cod_sessao=votacao['cod_sessao'], data=votacao['data'], hora=votacao['hora'],
                                     obj_votacao=votacao['obj_votacao'], resumo=votacao['resumo']))
        vot_number += 1
    return vot_number


def orientacao_bancada_to_sql():
    '''
        Saves a SQL insert DML script into file_path and returns de number of elements
    '''



def votos_to_sql():
    '''
        Saves a SQL insert DML script into file_path and returns de number of elements
    '''



proposicoes_to_sql(load_data(INPUT_FILE_NAME))
