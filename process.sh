#!/bin/bash

csv_input_dir=inputs/ENE_Definition_CSV_20230314
attribute_definitions_file=inputs/attribute-definitions-20220711.jsonl
output_dir=outputs/20230314

python3 convert-csv2jsonl.py ${csv_input_dir}/{0_concepts,1_names,2_times,3_numbers,9_ignored}.csv | pv -cl > ${output_dir}/ENE_Definition_v9.0.0.jsonl

python3 integrate-ene-and-attribute-definitions.py \
    --ene-definition-path ${output_dir}/ENE_Definition_v9.0.0.jsonl \
    --attribute-definition-path ${attribute_definitions_file} \
    | pv -cl > ${output_dir}/ene_definition_v9.0.0-with-attributes-and-shinra-tasks.jsonl

python3 integrate-ene-and-attribute-definitions.py \
    --ene-definition-path ${output_dir}/ENE_Definition_v9.0.0.jsonl \
    --attribute-definition-path ${attribute_definitions_file} \
    --remove-shinra-task-information \
    | pv -cl > ${output_dir}/ene_definition_v9.0.0-with-attributes.jsonl
