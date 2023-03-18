Version 1.0

文件说明
│  addInfo.py                                   // 自动添加信息的python脚本
│  data.csv                                     // 信息表格，用于后续批量添加，暂时未适配
│  readme.txt
│  数字生命卡.ai                                 // 水贴图的AI格式文件，可以自己打开编辑信息
│  水贴底图4K B.png                              // 导出的4K分辨率底图 B 面底图用于脚本批量生成
│  水贴成品 4K A.png                             // 导出的4K分辨率底图 A 面，大家通用
│
├─necessary fonts                               // 字体文件夹，使用 数字生命卡.AI 文件需要这两个字体
│      DINPro-Medium.otf
│      HarmonyOS_Sans_SC_Regular.ttf
│
└─output
        barcode.png                             // 根据文本生成的条形码，可以扫出信息
        barcode_bin.png                         // 条形码最终水贴图，已经变成白色，无法扫码，仅作对比
        barcode_crop.png                        // 条形码截取图，仅作对比
        刘培茄.png                               // 代码生成的透明图片，以代码中的 my_name 作为文件名，可以拿去创作
        刘培茄.tif                               // 代码生成的文件，以代码中的 my_name 作为文件名，水贴制作需要tif格式