import os
import re
import subprocess
from optparse import OptionParser
import logging

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="Files to Find", metavar="FILE")
parser.add_option("-q", "--quiet", dest="quiet",action="store_true",
                  help="Quiet Mode", metavar="Bool",default=False)
(options, args) = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Starting converter')
# read database here

if options.filename is None:
    parser.print_help()
    exit(1)

if options.quiet == True:
    logging.basicConfig(level=logging.ERROR)

highQ="--preset=\"High Profile\" --two"
for root, dirs, files in os.walk('.'):
      for f in files:
        if re.search(options.filename,f):
            filename=str.format('{}/{}',root,f)
            filetype=re.search("[\.][a-zA-Z]{3}$",filename)
            if filetype:
                sfx=filetype.group()
                logger.info(str.format('Matched File suffix as {}',sfx))
                newfilename=filename.replace(sfx,'.mp4')

                cmd=str.format("HandBrakeCLI -i '{}' -o '{}' {}",filename,newfilename,highQ)
                logger.info(str.format('Executing {}',cmd))
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
                #for line in p.stdout.readlines():
                #    print(str.format('{}',line)
            else:
                logger.error(str.format('Unfound Filetype in {}',filename))

logger.info('Finish updating records')
