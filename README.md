# bilibili
# B站爬虫、API和一些常用URI分析与记录
## 个人信息
* 基础信息

http://space.bilibili.com/ajax/member/GetInfo

* 

http://space.bilibili.com/ajax/member/getTags

* 投稿
* 订阅
* 关注
* 粉丝
* 兴趣圈

## 视频信息
* cid与aid

B站每部作品都有cid，也就是一般而言的av号，但是如果作品内部又分P，就会占用多个aid，aid是每个视频的唯一标识。

在后面涉及到评论和弹幕的时候我们会发现两者的区别，每部作品的评论区只有一个，所以获取评论用到的是cid；每个分P视频的弹幕池是单独的，所以获取弹幕用到的是aid。

cid可以在分P视频页源码中找到。（目前没有发现可以一次获取所有分P视频cid的办法。查看[you-get/bilibili.py](https://github.com/soimort/you-get/blob/a1a6ebf0361aff83792c9c8869d31d4e96e3acad/src/you_get/extractors/bilibili.py)发现也是这么做的。）
如http://www.bilibili.com/video/av637684/ 共有12个分P，可以在页面源码中找到：
<pre><code>&lt;option value=&#x27;/video/av637684/index_1.html&#x27;&gt;1、Episode 1~「最棒的也是最烂的律师，爱和法律都说谎？！」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_2.html&#x27;&gt;2、Episode 2~「赚著作权诉讼的钱？！」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_3.html&#x27;&gt;3、Episode 3~「是初恋还是跟踪狂？号泣的恋爱审判？」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_4.html&#x27;&gt;4、Episode 4~「把太阳还给我们公寓审判仁义的较量！」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_5.html&#x27;&gt;5、Episode 5~「时限7天！要钱要命！？守护恶德的政治家」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_6.html&#x27;&gt;6、Episode 6~「家庭暴力？有小三？流血的离婚判决刺客是前妻」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_7.html&#x27;&gt;7、Episode 7~「骨肉相争！潜藏在酱油家族的秘密与谎言」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_8.html&#x27;&gt;8、Episode 8~「夺取抚养权！天才童星与母亲断绝关系的判决」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_9.html&#x27;&gt;9、Episode 9~「恩仇的村民们，取回美丽的故乡」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_10.html&#x27;&gt;10、Episode 10~「要破产还是要五亿！？夸张的羁绊之乡」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_11.html&#x27;&gt;11、Episode 11~大结局「将内部告发者从不当解雇中拯救！！最强律师居然败北！？」&lt;/option&gt;
&lt;option value=&#x27;/video/av637684/index_12.html&#x27;&gt;12、SP1~「学校提出诉讼 和解费用一亿圆！！被隐瞒的事实及法官的不为人知的秘密」&lt;/option&gt;</code></pre>

然后对于每个/video/av.../index_..html，在页面源码可以获取cid：
<pre><code>&lt;script type=&#x27;text/javascript&#x27;&gt;EmbedPlayer(&#x27;player&#x27;, &quot;http://static.hdslb.com/play.swf&quot;, &quot;cid=5042719&amp;aid=637684&amp;pre_ad=0&quot;);&lt;/script&gt;</code></pre>


* 基础信息
* 评论
http://api.bilibili.com/x/reply?oid=637684&type=1&pn=1

获取到的评论是json格式，结构比较清楚，可以自己格式化以后分析。每页可以从replies中获取20条评论。

* 弹幕
http://comment.bilibili.com/5042719.xml

获取到的弹幕是xml格式。需要注意的是用户发送的弹幕中如果有特殊字符，会导致整个xml文件解析失败（我刚开始用etree遇到某几个弹幕文件报错，后来改用BeautifulSoup以后没有再解析失败）。

对于其中某一条弹幕作分析：

<pre><code>&lt;d p=&quot;312.71899414062,1,25,16777215,1466397636,0,0cb4e8ca,1978038095&quot;&gt;服部叔技能满分&lt;/d&gt;</code></pre>

d标签内容即为弹幕内容，其中p属性内部的含义依次如下：
<pre><code>p="时间,模式,字体大小,颜色,时间戳,弹幕池,用户ID的CRC32b加密,弹幕ID"</code></pre>
>第一个参数是弹幕出现的时间 以秒数为单位。

>第二个参数是弹幕的模式1..3 滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕

>第三个参数是字号， 12非常小,16特小,18小,25中,36大,45很大,64特别大

>第四个参数是字体的颜色 以HTML颜色的十位数为准

>第五个参数是Unix格式的时间戳。基准时间为 1970-1-1 08:00:00

>第六个参数是弹幕池 0普通池 1字幕池 2特殊池 【目前特殊池为高级弹幕专用】

>第七个参数是发送者的ID，用于“屏蔽此弹幕的发送者”功能

>第八个参数是弹幕在弹幕数据库中rowID 用于“历史弹幕”功能。

## 弹幕反查

B站默认无法查看弹幕发送者，而是对用户真是id做了一层hash（没有加salt），网上有人通过彩虹表做出了反查工具，如下（最后一个链接提供了反查的API）：

* http://biliquery.typcn.com/
* http://blog.eqoe.cn/posts/bilibili-comment-sender-digger.html
* http://bilifind.bili2233.com/
* https://www.fuckbilibili.com/bilidanmaku.html
* http://biliquery.typcn.com/api/user/hash/用户Hash

## 视频下载

参考you-get中的bilibili.py
