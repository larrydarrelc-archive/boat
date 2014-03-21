
                        // Core //

          Core 模块为程序提供了基础服务的支持。

        ~ 文件说明

          config.py     用作配置读取。

          dispatch.py   为服务器端程序提供事件分发的支持。
                        需要继承 BaseDispatcher 并定义相应
                        parse 方法来实现数据处理。

          items.py      检测点的模型定义。

          sqlstore.py   数据库访问的抽象接口。
