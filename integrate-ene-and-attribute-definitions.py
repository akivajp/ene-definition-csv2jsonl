#!/usr/bin/env python3

'''
    ENE定義書および属性定義書のJSON Linesファイルを統合する
'''

import argparse
import json
#import sys

from logzero import logger
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--ene-definition-path', '-E', type=str, required=True)
parser.add_argument('--attribute-definition-path', '-A', type=str, required=True)
parser.add_argument('--remove-shinra-task-information', '-R', action='store_true', required=False)

#ene_definition_path = sys.argv[1]
#attribute_definition_path = sys.argv[2]

args = parser.parse_args()
logger.debug('args: %s', args)

ene_id_to_attribute_definition = {}
#with open(attribute_definition_path) as f:
with open(args.attribute_definition_path) as f:
    for i, line in enumerate(tqdm(f)):
        d = json.loads(line)
        category = d['category']
        ene_id = category['ENE']
        if args.remove_shinra_task_information:
            attributes = d['attributes']
            for attribute in attributes:
                del attribute['extraction_task']
                del attribute['linking_task']
        ene_id_to_attribute_definition[ene_id] = d

#with open(ene_definition_path) as f:
with open(args.ene_definition_path) as f:
    for i, line in enumerate(tqdm(f)):
        d = json.loads(line)
        ene_id = d['ENE_id']
        if ene_id in ene_id_to_attribute_definition:
            attribute_definition = ene_id_to_attribute_definition[ene_id]
            attributes = attribute_definition['attributes']
            d['attributes'] = attributes
        print(json.dumps(d, ensure_ascii=False))
