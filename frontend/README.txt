
                        // Frontend //

          Frontend 模块主要用作托管 web 客户端的静态文件、
          转发 backend 提供的信息到客户端处。

          Frontend 和 backend 模块之间分别采用 TCP / HTTP
          协议进行通讯。从 backend 到 frontend 是使用 HTTP
          协议，从 frontend 到 backend 使用 TCP 协议。两种
          通信的数据格式都采用 EventMessage。

          Frontend 模块通过 websocket 协议和 web 客户端进行
          实时通信。通信数据格式采用 EventMessage。


        ~ 文件说明

          compat.py 对 tornado.web.RequestHandler 和
                    tornado.websocket.WebSocketHandler 进行
                    封装以和当前使用的 stream reader 保持
                    兼容。

          events.py 定义了 frontend 模块会处理的时间。

          server.py Frontend 服务器的程序定义。可以通过修改
                    FRONTEND_PORT 和 FRONTEND_DEST 来分别指定
                    服务器的监听端口和地址。

          utils.py  助手函数。

          views 文件夹内：

           backend.py 定义了处理 backend 发来的信息的 handler。

           clients.py 定义了和 web 客户端进行通信的 handler。

           main.py    定义了托管静态文件的 handler。

           test.py    定义了测试页面的 handler。
