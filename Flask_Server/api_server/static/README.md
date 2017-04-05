# Front-end
Angularjs and bootstrap
## Version
angular--1.6.0
## Functions and structure
First, 进入游客模式，游客可以查询item，可以注册，可以登录。如果选择注册，注册完回到登录界面；如果登录，进入查询主页面。管理员可以查询用户，删除用户等，他也可以进行普通用户的任何操作。普通用户可以选择查询item，登出，查看历史，更新信息，以及转到currency部分。如果查看历史，返回历史查询记录，如果更新信息，则输入更新信息，如果进入currency部分，可以选择搜索currency，post currency或者查看自己的post，选择查看自己的post则返回已经post的条目然后可以选择管理自己的post，选择管理之后可以更新或者删除已有条目。
## Api needed from back-end
Listed all: 查询item，注册，登录，管理员的一套牛逼操作，历史查看，更新用户信息，搜索currency，post currency，查看自己的post, 更新and删除自己的post。<br>
## Specific data structure needed go/back to/from api
● (from)历史查看：时间，查询内容<br>
● (to)搜索currency：需要，拥有<br>
● (from)搜索currency：卖主游戏id，需要，拥有，价格1，价格2<br>
● (to)发布currency：po主游戏id，拥有，需要，价格1，价格2<br>
● (from)查看自己的发布：transid，拥有，需要，价格1，价格2<br>
● (to)更新自己的发布：transid，拥有，需要，价格1，价格2<br>
● (to)删除自己的发布：transid<br>
back-end需生成独特的userid和transid
## To do
list: 验证，鉴权，监听，装包/拆包，通信，页面修改，样式修改，localstorage
