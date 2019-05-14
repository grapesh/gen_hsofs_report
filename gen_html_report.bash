#!/bin/bash

## Load Python 2.7.13
#module use /usrx/local/dev/modulefiles
#module load python/2.7.13

export pyPath="/usrx/local/dev/python/2.7.13/bin"
export platform=""

export myModules=${platform}"/gpfs/hps3/nos/noscrub/nwprod/csdlpy-1.5.1"
export pythonCode=${platform}"/gpfs/hps3/nos/noscrub/nwprod/gen_html_report/gen_report.py"

export hsofsDir=${platform}"/gpfs/hps/nco/ops/com/hsofs/para/"
export stormID="al832019"
export stormCycle="2019051412"
export postfix="/"

export template=${platform}"/gpfs/hps3/nos/noscrub/nwprod/hsofs-1.5.1/scripts/hsofs.template.htm"

export ftpLogin="svinogradov@emcrzdm"
export ftpPath="/home/www/polar/estofs/hsofs/nhc/"${stormID}"."${stormCycle}${postfix}"/index.htm"

PYTHONPATH=${myModules} ${pyPath}/python -W ignore ${pythonCode} -i ${hsofsDir} -s ${stormID} -x ${postfix} -z ${stormCycle} -t ${template} -u ${ftpLogin} -f ${ftpPath} #> ${logFile}

