# jiucai-dreame
区块链科学家本地化小工具

由于类似生成账号、转账等操作属于敏感操作，大家使用线上的工具总不会安全，所以在这提供一些实用工具的源码给大家使用和学习交流，同时也能一块共享区块链资讯

# 基础环境要求（建议都开着梯子）
1.安装python,安装包可到官方地址下载https://www.python.org/ 找，目前windows最新的是 3.10.0，https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe  

2.安装依赖包，windows系统，在目录下双击运行install_requirements.bat ，最后看见successfully字眼表明安装成功即可

# 工具说明

本仓库前期会提供兼容eth链的转账工具，账号生成，这些链包括eth,bsc,matic,fantom  
工具都是python脚本，运行的方法为在命令行下，python xxx.py
|  工具   | 功能  | 说明  |
|  ----  | ----  | ----  |
| gen_account.py  |生成账号| 主要用来生成账号，可以生成2种，一种带助记词(create_mnemonic)，另一个create_accounts不用带助记词，使用例子python gen_account.py,则会各生成10个账号在当前目录下:</br>result: mnemonic_accounts_2021_11_14 16_42_56.txt</br>result: accounts_2021_11_14 16_42_56.txt|


# TODO
1.批量转账

# 微信群
![Image text](https://github.com/hotbroker/jiucai-dreame/blob/master/img/c8f2ac99f9a326aaade146d89e66431.jpg)
