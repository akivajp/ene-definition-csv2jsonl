#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import csv
import json

from logzero import logger
#from tqdm import tqdm

paths = sys.argv[1:]

# 重複チェック用
set_id = set()
set_name_en = set()
set_name_ja = set()
set_def_en = set()
set_def_ja = set()

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

        if not strId:
            raise Exception('no id')        
        if strId in set_id:
            logger.debug('path: %s', path)
            logger.debug('row: %s', row)
            raise Exception('duplicate id: %s' % strId)
        set_id.add(strId)
        output['ENE_id'] = strId

        name_en = rec['ENE英語表記']
        if row[6]:
            name_ja = row[6]
        elif row[5]:
            name_ja = row[5]
        else:
            name_ja = row[4]
        #logger.debug('name ja: %s', name_ja)
        if not name_en:
            raise Exception('no name_en')
        if not name_ja:
            raise Exception('no name_ja')
        if name_en in set_name_en:
            raise Exception('duplicate name_en: %s' % name_en)
        if name_ja in set_name_ja:
            raise Exception('duplicate name_ja: %s' % name_ja)
        set_name_en.add(name_en)
        set_name_ja.add(name_ja)
        output['name'] = {}
        output['name']['en'] = name_en
        output['name']['ja'] = name_ja
        
        def_en = rec['Definition']
        def_ja = rec['定義文']
        if not def_en:
            raise Exception('no def_en')
        if not def_ja:
            raise Exception('no def_ja')
        if def_en in set_def_en:
            raise Exception('duplicate def_en: %s' % def_en)
        if def_ja in set_def_ja:
            raise Exception('duplicate def_ja: %s' % def_ja)
        set_def_en.add(def_en)
        set_def_ja.add(def_ja)
        output['definition'] = {}
        output['definition']['en'] = def_en
        output['definition']['ja'] = def_ja
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
        