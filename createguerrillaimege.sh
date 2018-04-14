#!/bin/bash

alias python=/usr/local/bin/python3.5

FTP="ftp://hmwr829gr.cr.chiba-u.ac.jp/gridded/FD/V20151105"

#python csv.py
#python datetime.py

# Set band type
for CHN in VIS ; do  #VIS TIR SIR EXT;do
    for chn in vis ; do
	for NUM in 01 ; do  #2 3 4 5 6 7 8 9 10 ;do #band number

	    cat datetime.txt | while read line ; do
		YYYY=`echo ${line} | cut -c 1-4`
		MM=`echo ${line} | cut -c 5-6`
		DD=`echo ${line} | cut -c 7-8`
		HH=`echo ${line} | cut -c 9-10`
		MN=`echo ${line} | cut -c 11-12`

		echo "Download file"
		echo "${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss.bz2"
		wget ${FTP}/${YYYY}${MM}/${CHN}/${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss.bz2
		echo "Extract file"
		bzip2 -d ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss.bz2

		#Create image
		if [ ${CHN} = "TIR" -o ${CHN} = "SIR" ];then
		    python count2tbb20.py ${chn}.${NUM} ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.png
		elif [ ${CHN} = "VIS" ];then
		    python count2tbb10.py ${chn}.${NUM} ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.png
		elif [ ${CHN} = "EXT" ];then
		    python count2tbb05.py ${chn}.${NUM} ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.png
		fi
	    done
	done
    done
done

