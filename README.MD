![screenshots](https://github.com/gaotianchi/gaotianchi/blob/main/screenshots/screenshot.jpg)

## 项目简介
这是一个简易的Twitter平台，用户可以在上面发布推文和图片，也可以发布自己的简历，所以这个网站可以用于展示自己的个人动态以及求职过程中让面试官更好地认识自己。我开发它的主要动机是复习一下前面一段时间所学的知识，主要包括两个方面，第一是后端的flask框架，另一个是前端的vue框架。这个过程中我尽可能不把那些功能复杂化，以便能够在三天之内完成它并且将其部署到服务器上。毫无疑问目前的代码是非常脆弱的，有许多地方缺乏容错能力，但是我的定位就是做一个完整的项目而不是做一个完美的项目，所以，今天也算是完成任务了吧。

## 接口说明

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

## 安装与使用

```bash
git clone https://github.com/gaotianchi/gaotianchi.git
cd gaotianchi/backend
// 在 gaotianchi/backend 内创建 .env 文件并配置必要的参数
// 详细操作请参阅 https://github.com/gaotianchi/gaotianchi/tree/main/backend#readme
```

```bash
cd gaotianchi/frontend
npm install
// 注意 ico 文件位于 frontend/public/favicon.ico 中，需要自行配置
// logo 文件也需要自行替换，位置是 frontend/src/assets/logo.jpg
npm run dev
```


## 使用视频



https://github.com/gaotianchi/gaotianchi/blob/main/screenshots/Record.mp4




