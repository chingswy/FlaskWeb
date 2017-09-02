
### 构造函数 ###
Flask 类的构造函数只有一个必须指定的参数，即程序主模块或包的名字。在大多数程序
中，Python 的 `__name__` 变量就是所需的值。

	from flask import Flask
	app = Flask(__name__)

### 定义路由 ###
在Flask 程序中定义路由的最简便方式，是使用程序实例提供的`app.route` 修饰器，把修饰的函数注册为路由。下面的例子说明了如何使用这个修饰器声明路由：

	@app.route('/')
	def index():
		return '<h1>Hello World!</h1>'

动态路由实现

	@app.route('/user/<name>')
	def user(name):
		return '<h1>Hello, %s!</h1>' % name

路由中的动态部分默认使用字符串，不过也可使用类型定义。例如，路由`/user/<int:id>`
只会匹配动态片段`id` 为整数的URL。Flask 支持在路由中使用`int`、`float` 和`path 类型。
path 类型也是字符串，但不把斜线视作分隔符，而将其当作动态片段的一部分。

### 启动服务器 ###

程序实例用run 方法启动Flask 集成的开发Web 服务器：

	if __name__ == '__main__':
		app.run(debug=True)

### 上下文 ###
为了避免大量可有可无的参数把视图函数弄得一团糟，Flask 使用**上下文**临时把某些对象
变为全局可访问。有了上下文，就可以写出下面的视图函数：

	from flask import request
	@app.route('/')
	def index():
		user_agent = request.headers.get('User-Agent')
		return '<p>Your browser is %s</p>' % user_agent

注意在这个视图函数中我们如何把request 当作全局变量使用。事实上，request 不可能是全局变量。试想，在多线程服务器中，多个线程同时处理不同客户端发送的不同请求时，每个线程看到的request 对象必然不同。Falsk 使用上下文让特定的变量在一个线程中全局可访问，与此同时却不会干扰其他线程。

线程是可单独管理的最小指令集。进程经常使用多个活动线程，有时还会共
享内存或文件句柄等资源。多线程Web 服务器会创建一个线程池，再从线
程池中选择一个线程用于处理接收到的请求。

Flask 在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除。程序上下文被推送后，就可以在线程中使`current_app` 和`g` 变量。类似地，请求上下文被推送后，就可以使用`request` 和`session` 变量。如果使用这些变量时我们没有激活程序上下文或请求上下文，就会导致错误。

### 请求调度 ###
程序收到客户端发来的请求时，要找到处理该请求的视图函数。为了完成这个任务，Flask会在程序的URL 映射中查找请求的URL。URL 映射是URL 和视图函数之间的对应关系。Flask 使用`app.route` 修饰器或者非修饰器形式的`app.add_url_rule()` 生成映射。


## 模板 ##
模板是一个包含响应文本的文件，其中包含用占位变量表示的动态部分，其具体值只在请求的上下文中才能知道。使用真实值替换变量，再返回最终得到的响应字符串，这一过程称为渲染。为了渲染模板，Flask 使用了一个名为Jinja2 的强大模板引擎。

### 渲染模板 ###

默认情况下，Flask 在程序文件夹中的templates 子文件夹中寻找模板。在下一个hello.py版本中，要把前面定义的模板保存在templates 文件夹中，并分别命名为index.html 和user.html。

	from flask import Flask, render_template
	# ...
	@app.route('/')
	def index():
		return render_template('index.html')
	@app.route('/user/<name>')
	def user(name):
		return render_template('user.html', name=name)

Flask 提供的`render_template` 函数把Jinja2 模板引擎集成到了程序中。`render_template` 函数的第一个参数是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实值。在这段代码中，第二个模板收到一个名为`name` 的变量。

### 变量 ###
在模板中使用的{{ name }} 结构表示一个变量，它是一种特殊的占位符，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取。

Jinja2 能识别所有类型的变量，甚至是一些复杂的类型，例如列表、字典和对象。

### 控制结构 ###

条件控制语句

	{% if user %}
		Hello, {{ user }}!
	{% else %}
		Hello, Stranger!
	{% endif %}

for循环语句

	<ul>
	{% for comment in comments %}
		<li>{{ comment }}</li>
	{% endfor %}
	</ul>

使用宏

	{% macro render_comment(comment) %}
		<li>{{ comment }}</li>
	{% endmacro %}
	<ul>
	{% for comment in comments %}
		{{ render_comment(comment) }}
	{% endfor %}
	</ul>

另一种重复使用代码的强大方式是模板继承，它类似于Python 代码中的类继承。首先，创
建一个名为base.html 的基模板：

	<html>
	<head>
		{% block head %}
		<title>{% block title %}{% endblock %} - My Application</title>
		{% endblock %}
	</head>
	<body>
		{% block body %}
		{% endblock %}
	</body>
	</html>

block 标签定义的元素可在衍生模板中修改。在本例中，我们定义了名为head、title 和body 的块。注意，title 包含在head 中。下面这个示例是基模板的衍生模板：

	{% extends "base.html" %}
	{% block title %}Index{% endblock %}
	{% block head %}
	{{ super() }}
	<style>
	</style>
	{% endblock %}
	{% block body %}
	<h1>Hello, World!</h1>
	{% endblock %}

extends 指令声明这个模板衍生自base.html。在extends 指令之后，基模板中的3 个块被重新定义，模板引擎会将其插入适当的位置。注意新定义的head 块，在基模板中其内容不是空的，所以使用super() 获取原来的内容。

## 使用flask-bootstrap ##

Flask 扩展一般都在创建程序实例时初始化。

	from flask.ext.bootstrap import Bootstrap
	# ...
	bootstrap = Bootstrap(app)


## web表单 