### 后端概述
后端开发使用的主要框架是 [Flask](https://flask.palletsprojects.com/en/3.0.x/) ，除此以外使用的第三方库还包括 Flask-SQLAlchemy（用于操作数据库）、cryptography（用于加密用户数据）、Flask-Cors（用于跨域链接）等。

`src/apis/` 目录下有两个子目录分别是 `v1` 和 `v2`，这代表两个接口版本，其中第一个是已经遗弃的版本，它可以勉强正常使用。当前使用的是 `v2` 版本的接口。运行该项目需要自行补充 `.env` 文件，该文件下只有一个必须的参数 `VERSION`, 该参数的值为 `1` 或者 `2`，代表使用哪个版本的接口，如果想使用 `v2` 的接口可以设置为 `2`。`data/` 文件夹下是两个接口版本的存储数据，也分为了 `v1` 和 `v2` 两个子文件夹。

### V2 接口详情

| url                 | 请求方法   | 响应内容                               |
| ------------------- | ------ | ---------------------------------- |
| /token              | POST   | 获取 accessToken                   |
| /verify             | GET    | 验证用户身份                       |
| /me                 | POST   | 创建新用户（也就是自己）           |
| /resume             | PUT    | 更新用户简历                       |
| /me                 | PATCH  | 更新自己的作者名、简介等信息       |
| /tweets             | POST   | 创建新推文                         |
| /tweets/<tweet_id>  | PATCH  | 更新推文的文本信息（无法更新图片） |
| /tweets/<tweet_id>  | DELETE | 删除指定推文                       |
| /photos             | PSOT   | 添加图片                           |
| /resume             | GET    | 下载简历                           |
| /photo/<file_name>   | GET    | 下载图片                           |
| /my-profile         | GET    | 获取自己的个人概要信息             |
| /my-detail          | GET    | 获取自己的详细信息                 |
| /page-tweets/<page> | GET    | 获取某一页的推文列表               |
| /tweets             | GET    | 获取最新一条推文信息               |

### 本地安装与使用

将 `gaotianchi/backend` 下载到自己的计算机后使用终端进入该文件夹下，创建 `Python` 虚拟环境并安装 `requirements.txt` 内的所有第三方库。注意，前面已经提到该项目缺失 `.env` 文件，请自行创建并配置好前面提到的参数，最好将参数值设置为 `2`，激活虚拟环境后使用命令：
```bash
flask initdb
```
初始化后端数据库，结束后 `data/v2/` 文件夹下会生成一个 `.db` 结尾的数据库文件。一切准备就绪使用命令：
```bash
flask run
```
启动应用。
```
PS D:\Documents\gaotianchi\backend> flask initdb
完成数据格式化！
PS D:\Documents\gaotianchi\backend> flask run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
 接下来你就可以使用上面的接口测试数据了。