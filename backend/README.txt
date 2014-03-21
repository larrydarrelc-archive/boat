
                        // Backend //

          Backend 模块主要用作和底层 controller 的通信、
          维护各检测点的状态以及和 frontend 模块的通信。

          Backend 模块通过 TCP 协议和 controller 进行数据
          通信。其中 backend 作为 TCP 通信的服务器端。通信
          数据格式采用 EventMessage。

          Backend 和 frontend 模块之间分别采用 TCP / HTTP
          协议进行通讯。从 backend 到 frontend 是使用 HTTP
          协议，从 frontend 到 backend 使用 TCP 协议。两种
          通信的数据格式都采用 EventMessage。


        ~ 文件说明

          compat.py  对 tornado.iostream.IOStream 进行封装，
                     使之和当前使用的 stream reader 兼容。

          events.py  定义了 backend 模块会处理的事件。

          message.py 提供了对 EventMessage 的处理函数。

          server.py  后端服务器的程序定义。可以通过 BACKEND_PORT
                     和 BACKEND_DEST 来分别指定服务器的
                     监听端口和地址。

          utils.py   助手函数。
