#!/bin/bash

csv_input_dir=inputs/ENE_Definition_CSV_20230314
output_dir=outputs/20230314

echo "[exec] python3 convert-csv2jsonl.py ${csv_input_dir}/{0_concepts,1_names,2_times,3_numbers,9_ignored}.csv | pv -cl > ${output_dir}/ENE_Definition_v9.0.0.jsonl"
python3 convert-csv2jsonl.py ${csv_input_dir}/{0_concepts,1_names,2_times,3_numbers,9_ignored}.csv | pv -cl > ${output_dir}/ENE_Definition_v9.0.0.jsonl
