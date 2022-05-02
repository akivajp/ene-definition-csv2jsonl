#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import csv
import json

#from logzero import logger
#from tqdm import tqdm

paths = sys.argv[1:]
for path in paths:
    #path = sys.argv[1]
    reader = csv.reader(open(path, 'r', encoding='utf-8-sig'))
    head = next(reader)
    #logger.debug('head: %s', head)
    rows = list(reader)
    #logger.debug('rows: %s', rows)

    reader2 = csv.DictReader(open(path, 'r', encoding='utf-8-sig'))
    recs = list(reader2)
    #logger.debug('rec0: %s', recs[0])

    dict_id_to_category = {}
    list_ids = []

    for (i, (row, rec)) in enumerate(zip(rows, recs)):
        #logger.debug('row: %s', row)
        #logger.debug('rec: %s', rec)
        #if i == 0:
        #    continue
        output = {}
        id_fields = []
        for j in range(4):
            if row[j]:
                id_fields.append(row[j])
        if len(id_fields) == 0:
            raise Exception('no id fields')
        strId = '.'.join(id_fields)
        #logger.debug('strId: %s', strId)
        output['ENE_id'] = strId
        output['name'] = {}
        output['name']['en'] = rec['ENE英語表記']
        if 'NE' in rec:
            output['name']['ja'] = rec['NE']
        elif 'ENE' in rec:
            output['name']['ja'] = rec['ENE']
        else:
            raise Exception('no NE/ENE')
        output['definition'] = {}
        output['definition']['en'] = rec['Definition']
        output['definition']['ja'] = rec['定義文']
        output['children_category'] = []
        if strId.find('.') >= 0:
            parentId = strId[:strId.rfind('.')]
            #logger.debug('parentId: %s', parentId)
            output['parent_category'] = parentId
            parent = dict_id_to_category[parentId]
            parent['children_category'].append(strId)
        else:
            output['parent_category'] = None
        #print(json.dumps(output, ensure_ascii=False))
        list_ids.append(strId)
        dict_id_to_category[strId] = output

    for i, strId in enumerate(list_ids):
        output = dict_id_to_category[strId]
        print(json.dumps(output, ensure_ascii=False))
        