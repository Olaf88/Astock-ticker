# A股实时数据 命令行显示A股实时价格
Python终端程序 获取实时股票数据；仅支持python3
在命令行终端获取股票实时数据，主要显示了当前价格、昨日收盘价以及对应价格涨跌，涨跌幅度。

使用了新浪财经数据接口，如果需要添加其他类型的数据，比如成交量，委比等数据可以研究下新浪数据接口进行改动。

依赖库：
requests
urwid

数据每5秒刷新一次。

![image](https://user-images.githubusercontent.com/9567881/109520975-c1a85280-7ae7-11eb-9a13-d9cbdccc31b4.png)

