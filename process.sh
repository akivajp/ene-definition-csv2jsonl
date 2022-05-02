#!/bin/bash

echo "[exec] python3 convert.py inputs/{0_concepts,1_names,2_times,3_numbers,9_ignored}.csv | pv -cl > outputs/ENE_Definition_v9.0.0.json"
python3 convert.py inputs/{0_concepts,1_names,2_times,3_numbers,9_ignored}.csv | pv -cl > outputs/ENE_Definition_v9.0.0.json
