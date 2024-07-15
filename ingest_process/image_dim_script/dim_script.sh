#!/bin/bash

# This is a script to automate fetching image dimensions for each row in CSVs in the need dims folder
# USAGE: run the script by entereing sh dim-script.sh at the command prompt along with the batch you are processing

function loading_icon() {
    local load_interval="${1}"
    local loading_message="${2}"
    local elapsed=0
    local loading_animation=( '—' "\\" '|' '/' )

    echo "${loading_message}"

    # This part is to make the cursor not blink
    # on top of the animation while it lasts
    tput civis
    trap "tput cnorm" EXIT
    while [ "${load_interval}" -ne "${elapsed}" ]; do
        for frame in "${loading_animation[@]}" ; do
            printf "%s\b" "${frame}"
            sleep 0.25
        done
        elapsed=$(( elapsed + 1 ))
    done
    printf " \b\n"
}



echo "fetching dimensions for $1 csv files in ingest_process/need-dims/"
for filename in ingest_process/need-dims/$1/*.csv; do  
        echo "getting dimensions for $filename"
        echo "$filename" | python3 ingest_process/image_dim_script/get_hw_parallel.py
        loading_icon 60 "Waiting 1min run again and fix any errors"
        echo "$filename" | python3 ingest_process/image_dim_script/get_hw_parallel.py
        loading_icon 120 "Waiting 2min to fetch next csv"
    
       
done

echo "Finished fetching dimensions for $1"
