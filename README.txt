
                        // Boat //

          本文档主要介绍服务器端程序的技术细节。

          文档最后修订时间： 2014 年 3 月 21 日
 
        ~ 目录

          - 名词解释
          - 模块说明
          - 安装运行方法
          - 部署方案

        ~ 名词解释

          Backend: 指服务器端程序中的后端模块。
        
          Controller：指底层真正控制、监控船只状态的模块。

          EventMessage: 指形如 event_name:event_data 的
                        数据格式，主要用作各模块间的内部
                        通信。

          Frontend： 指服务器端程序中提供静态文件托管服务、
                     websocket 服务的模块。

          Web: 指浏览器端的人机交互部分程序。


        ~ 模块说明

          服务器程序由：

            - 客户端（web）
            - 前端服务器（frontend）
            - 后端服务器（backend）
            - 核心模块（core）
            - 公用助手模块（common）
            - 配置（configs）
            - 测试模块（tests）

          等几个模块组成。各个模块的详细说明可以参考
          各自模块目录下的 README.txt 以及各程序文件
          内的注释文档。


        ~ 安装运行方法

          TODO


        ~ 部署方案

          TODO
