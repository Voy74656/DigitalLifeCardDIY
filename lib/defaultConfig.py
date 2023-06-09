import lib.utils as utils

# 默认信息设置
DEFAULT_NAME_CN = '图丫丫'

DEFAULT_NAME_EN = 'TUYAYA'

DEFAULT_BIRTH_DATE = '20230320'

DEFAULT_SN_CODE = 'PN-R-DSM01 A513C'

DEFAULT_BARCODE = utils.generate_random_barcode()

DEFAULT_TOP_RIGHT_CODE = '2023'


# 输出设置

DEFAULT_OUTPUT_PATH = 'output/'



## 以下是高级配置项

# 默认底图
BASE_IMAGE = 'resources/水贴底图 4K B.png'

TEST_CSV = 'test/demo.csv'

MAXLEN_BARCODE = 18
MAXLEN_SNCODE = 20
MAXLEN_NAMECN = 4
MAXLEN_TRCODE = 4

BARCODE_COMPLEMENT_SYMBOL = '-'

# 拼音生成器
from xpinyin import Pinyin
DEAFULT_PINYIN = Pinyin()

DEFAULT_FONTFAMILY = utils.FontFamily()

BARCODE_TEMP = 'output/TEMP_BARCODE'

BARCODE_UUID_ENABLE_KEY = ''