#!/bin/bash

pkill -P runme.sh
pkill -P compare_diff.sh
pkill -P run_process.sh

kill -9 BEAM_TEMP_PID    
