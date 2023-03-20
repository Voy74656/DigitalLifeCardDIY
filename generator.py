# coding=UTF-8
import getopt
import sys

from lib.defaultConfig import DEFAULT_OUTPUT_PATH, TEST_CSV
from lib.dataFormat import DigitalLifeUVs, singleDigitalLifeUV

def generate_digital_lifecard(argv = sys.argv[1:]):
    opts, args = getopt.getopt(argv, '-h-c-g:-o:-v', ['help','cil','group', 'output', 'version'])
    def help():
        print(f'USAGE:\n\n    python {__file__} [opt]\n\nopts:\n'+
              '        -c / --cil:                   (DEFAULT) Generate DigitalLife Card UV in console.\n'+
              '        -g / --group [csv file]:      Auto generate DigitalLife Card UVs for group.\n'+
              '        -o / --output [output path]:  Set output dir, can work with -c and -g command\n'+
              '                                      Dafault: ./output/\n'
              '        -v / --version:               Display script version & developer\'s information\n'+
              '        -h / --help:                  Display this help file')
        sys.exit()
    def version():
        print(f'Version 2.0\nBy @Voy74654\nrefer: \n    [github] https://github.com/Voy74656/DigitalLifeCardDIY\n    [gitee]  https://gitee.com/Voy74656/DigitalLifeCardDIY')
        sys.exit()
    
    _output_path=DEFAULT_OUTPUT_PATH
    data = None

    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            help()
        if opt_name in ('-v', '--version'):
            version()
        if opt_name in ('-g', '--group'):
            data = DigitalLifeUVs(opt_value or TEST_CSV)
        if opt_name in ('-o', '--output'):
            _output_path = opt_value or DEFAULT_OUTPUT_PATH
        if opt_name in ('-c', '--cil'):
            data = singleDigitalLifeUV.from_cli()
    if not data:
        data = singleDigitalLifeUV.from_cli()
    data.export(outputPath=_output_path)


if __name__ =="__main__":

    generate_digital_lifecard()
    sys.exit()

    ####### __MAIN__ END #######



    ####### advance #######

    # expose api 
    # dl1 = rawDigitalLifeUV('爱莉希雅','EGO-ALYSIA','20211111','CM02','Qjxie1234567890efx','Miss Pink Elf ~')
    # dls = DigitalLifeUVs([dl1, dl1, dl1])
