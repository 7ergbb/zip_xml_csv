import csv
import logging
import multiprocessing as mp
import os

from xml.dom import minidom
from zipfile import ZipFile

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_id_level_csv(data):
    '''
    формирует csv файл - c id, level
    :param list data: данные из xml файлов в виде списка словарей.
    '''
    if data and len(data) > 0:
        csv_path = ''.join([os.getcwd(), '/id_level.csv'])
        try:
            with open(csv_path, 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(('id', 'level'))
                for xml_data in data:
                    for item in xml_data:
                        writer.writerow((item['id'], item['level']))
        except IOError as er:
            logger.error(er)

        logger.info(f'created - {csv_path}')
    else:
        logger.error('no data for csv file')
        return


def create_id_object_csv(data):
    '''
    формирует csv файл - c id, object
    :param list data: данные из xml файлов в виде списка словарей.
    '''
    if data and len(data) > 0:
        csv_path = ''.join([os.getcwd(), '/id_objects.csv'])
        try:
            with open(csv_path, 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(('id', 'object'))
                for xml_data in data:
                    for item in xml_data:
                        for obj in item['objects']:
                            writer.writerow((item['id'], obj))

        except IOError as er:
            logger.error(er)
        logger.info(f'created - {csv_path}')
    else:
        logger.error('no data for csv file')
        return


def parse_xml(xml):
    '''
    Получить в виде словаря значения id, level элементов var и name элементов object из xml файла.
    :param xml: xml файл.
    '''
    res = {'id': '', 'level': '', 'objects': []}

    doc = minidom.parse(xml)
    var_elements = doc.getElementsByTagName('var')
    for item in var_elements:
        if item.getAttribute('name') == 'id':
            res['id'] = item.getAttribute('value')
        elif item.getAttribute('name') == 'level':
            res['level'] = item.getAttribute('value')

    objects = doc.getElementsByTagName('object')
    for item in objects:
        res['objects'].append(item.getAttribute('name'))

    return res


def parse_zip(zip):
    '''
     Получить в виде списка словарей с ключами id, level, object  - для всех хмл из архива .
    :param str zip: путь к zip файлу .
    '''
    res = []
    try:
        with ZipFile(zip, 'r') as zipfile:
            files = zipfile.namelist()
            for file in files:
                if file.endswith('.xml') is False:
                    logging.error('no xml files in archive')
                    return
                else:
                    with zipfile.open(file, 'r') as xml:
                        xml_content = parse_xml(xml)
                        res.append(xml_content)
    except Exception as ex:
        logging.error(ex)

    return res


def processing_files():
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.zip'):
            files.append(''.join([os.getcwd(), '/', filename]))
    results = []
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(parse_zip, files)

    create_id_level_csv(results)
    create_id_object_csv(results)
