#!/bin/bash

file="/home/berkeleylab/Repository/beam/instanceconfpath.txt"

conf_file=$(cat "$file")

gradle :run -PappArgs="['--config', '$conf_file']"





