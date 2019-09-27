# 网络传输分析、服务设计与实现

## 要求
- 所有解答源码请放入公开 github 仓库，并给出可访问的 url

1. 网络传输分析: wireshark 抓包文件 mysterious_networking_behavior.pcapng/mysterious_networking_behavior.txt 内容描述了一次客户端/服务端架构下的网络行为产生的网络传输数据 (.pcapng 与 .txt 文件内容等价), 请根据抓包文件回答以下问题，细节越多越好
    - 详细描述客户端发起的每一次 DNS 请求和结果
    - 说明客户端与服务端建立了多少个 TCP channel，分别是哪些 frame，分别完成了什么传输任务，为什么存在多个 TCP channel
    - 选择几个 frame 详细说明一次 TCP 握手流程，需要包含具体 frame 内容
    - 请说明服务端程序可以如何优化，以提升单个用户访问延迟，以及并发吞吐量

2. 服务设计与实现: 仅使用 TCP socket 库，实现一个 HTTP 服务程序，监听 localhost:8080 端口，使用任意网页浏览器 (Chrome/Firefox/Safari等) 打开 http://localhost:8080，显示用户名/密码和对应输入框，以及登录按钮，点击后跳转页面，显示刚刚输入的用户名及密码
   - 不限编程语言
   - 整个服务程序为单个文件，不能包含资源文件
   - 登录一次后，下次访问直接跳转至显示用户名密码的页面

##answer:
- 1:  
  DNS请求有编号为1-7，25，
  客户端本地127.0.0.1访问本地DNS服务器127.0.1.1请求mirror.azure.cn域名的dns信息，首先检查缓存是否有数据，未有。
   客户端10.11.29.131 请求本地dns服务器 210.22.70.3, 210.22.84.3 114.114.114.114，
   询问mirror.azure.cn的解析返回CNAME记录：mirror.trafficmanager.cn
   询问mirror.trafficmanager.cn的解析返回CNAME记录：eastmirror.chinacloudapp.cn
   询问eastmirror.chinacloudapp.cn的解析返回A记录：139.217.146.62
- 2   
   根据题目内容，个人理解的tcp channel是一个tcp从建立到关闭过程中的连接状态。从抓包记录来看，只有一次建立连接的过程，所以，我认为这是一次http的长连接，所以只有一个TCP channel，建立连接之后的所有tcp包都是这个channel的连接过程，其主要传输内容是http请求的主页及相关的静态文件。
   
- 3  tcp三次握手的frame分别是8，9，10：其中，frame8是客户端从60686端口向服务器80端口发起建立连接请求，标志位是【SYN】=1,Seq=0; 之后服务器收到客户端发来的建立连接的请求，返回给客户端frame9，【SYN】=1, 【ACK】=1,seq=0,ack=0+1=1, 这里的ack是对第一次建立连接是seq=0的确认。 客户端收到请求后，再次进行回答frame10,【ACK】=1, seq=1是对第二次连接中的ack的确认, ack=1是对第二次连接中seq=0的确认。至此tcp连接建立。

- 4 优化访问延迟，提高并发性能的方法
 - 1 选择性能较好的dns服务器，优化网络环境。
 - 2 优化代码，减少服务器响应时间。
 - 3 增加高速缓存层，进一步减少服务器时间
 - 4 对于静态文件，可以使用减少文件数量，对文件压缩，合并文件等方法减少传输内容，采用gzip压缩，同时使用cdn分发的技术等可以提高访问效率。
 - 5 增加带宽，服务器硬件性能，等方法
  