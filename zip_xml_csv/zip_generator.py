import logging
import os
import random
from uuid import uuid4

from xml.dom import minidom
from zipfile import ZipFile

XML_TO_ZIP_QUANTITY = 100
ZIP_QUANTITY = 50

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_xml():
    '''Сгенерировать xml документ.'''
    doc = minidom.Document()
    root = doc.createElement('root')
    doc.appendChild(root)
    level = random.randint(1, 100)

    id_unit = doc.createElement('var')
    id_unit.setAttribute('name', 'id')
    id_unit.setAttribute('value', str(uuid4().hex))
    root.appendChild(id_unit)

    level_unit = doc.createElement('var')
    level_unit.setAttribute('name', 'level')
    level_unit.setAttribute('value', str(level))
    root.appendChild(level_unit)

    objects_unit = doc.createElement('objects')
    root.appendChild(objects_unit)

    objects_num = random.randint(1, 10)
    for item in range(objects_num):
        child_obj = doc.createElement('object')
        child_obj.setAttribute('name', str(uuid4().hex))
        objects_unit.appendChild(child_obj)

    xml_str = doc.toprettyxml(indent="\t")

    return xml_str


def generate_zip(path, quantity=XML_TO_ZIP_QUANTITY):
    '''
    Создать zip архив в текущей деректории
    :param str path: путь c именем файла.
    :param int quantity: количество генерируемых для одного архива xml файлов.
    '''
    try:
        with ZipFile(path, 'w') as zip_archive:
            for i in range(quantity):
                xml_content = create_xml()
                zip_archive.writestr(f'{i}.xml', xml_content)
                logging.info(f' added {i}.xml file to zip archive {path}')
    except Exception as ex:
        logging.error(ex)


def archives_creation(quantity=ZIP_QUANTITY):
    '''
    Создать zip архивы  в текущей деректории. Количество которых равно ZIP_QUANTITY (50)
    :param int quantity: количество генерируемых zip файлов.
    '''
    for i in range(quantity):
        archive_name = str(uuid4().hex) + '.zip'
        zip_path = ''.join([os.getcwd(), '/', archive_name])
        generate_zip(zip_path)
        logging.info(f' added archive - {archive_name}')
