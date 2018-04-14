#!/bin/bash

alias python=/usr/local/bin/python

FTP="ftp://hmwr829gr.cr.chiba-u.ac.jp/gridded/FD/V20151105"

# Set DATE
for YYYY in 2016 ; do  # Year (from 2015)
  for MM in 08 ; do  # Month
    for DD in 03 ; do  # Day
      for HH in 04 ; do  # Hour
      for MN in 00 10 20 30 40 50 ; do  # 00 10 20 30 40 50 # Minute
# Set band type
      for CHN in SIR ; do  #VIS TIR SIR EXT;do
      for chn in sir ; do
      for NUM in 01 ; do  #2 3 4 5 6 7 8 9 10 ;do #band number

	  echo "Download file"
	  echo "${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss.bz2"
	  wget ${FTP}/${YYYY}${MM}/${CHN}/${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss.bz2
	  echo "Extract file"
	  bzip2 -d ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss.bz2

#Create image
	   if [ ${CHN} = "TIR" -o ${CHN} = "SIR" ];then
               python3 count2tbb20.py ${chn}.${NUM} ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.png
	   elif [ ${CHN} = "VIS" ];then
               python3 count2tbb10.py ${chn}.${NUM} ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.png
	   elif [ ${CHN} = "EXT" ];then
	       python3 count2tbb05.py ${chn}.${NUM} ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.fld.geoss ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.png
	   fi

	   # python3 croppingextinshell.py ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.png ${YYYY}${MM}${DD}${HH}${MN}.${chn}.${NUM}.cropped.hokuriku.png
# delete downloaded file
rm *.geoss

      done
      done
      done
      done
      done
    done
  done
done
