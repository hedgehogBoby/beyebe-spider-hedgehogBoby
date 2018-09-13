# Hedgehog-Spider(小刺猬爬虫框架)

<center>
<img align="center" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1536756813560&di=bf502510162fb57faec768f080c9d01d&imgtype=0&src=http%3A%2F%2Fpic.qbaobei.com%2FUploads%2FEditor%2F2016-11-25%2F5837fd5078b8b.jpg" width="200" hegiht=Auto align=center />
</center>


 **小刺猬爬虫框架** 基于python-scrapy开发使用,旨在解决爬虫业务高速横向扩展中的一系列问题。


## 痛点及解决方案
####痛点:混乱

**业务横向扩展混乱** 

    当业务横向拓展的过程中，随着爬取站点增加，重复开发越来越多，带宽/IO资源和数据存储资源分配效率低下。
    
**存储混乱** 

    当众多业务结构不一致时,存储与检索十分困难。
    
**中间件服务混乱** 

	 IP池服务\验证码服务\模板等中间件在业务之间不能共享,提高成本。
	 
####解决方案
	
	1、下载集群与与业务分发隔离，以Scrapy中间件的形式调用下载集群。完成负载均衡。
	2、采用基于继承的ORM结构，按层次继承标准。这样存储有理可查。
	3、中间件单独启动服务，使用redis/HTTP进行通信，提供Scrapy中间件以供使用。
	


![MacDown Screenshot](http://dyt1.oss-cn-shenzhen.aliyuncs.com/dianyou/data/circle/img/20180815/22d500f607f1f8dfeaef30a18e1a6508.png)
****


## 与Scrapy的关系
scrapy是基于业务层, Hedgehog是基于业务的抽象，基于scrapy二次开发。

scrapy解决了爬虫开发的问题,而Hedgehog是用来解决业务拓展中的问题。

其中,你需要使用scrapy做分发机嵌入Hedgehog的下载中间件来替代单节点下载。这意味着你的分发机甚至无需外网环境。

你还可以实现其他的下载形式(在下载层), Hedgehog内置了scrapy、普通request、webdriver、以及annie视频下载。这有点像你用中间件重写scrapy-Request,在Hedgehog中你需要在下载层定义下载枚举并实现,这样天生就有就具有分布式属性。

如果你完全不懂scrapy,那你可能后面使用的时候会非常棘手。

点击这里了解scrapy [github-scrapy](https://github.com/scrapy/scrapy)

## 下载层架构
下载层架构主要是由用户、下载层、中间件层、数据层和支持层构成。

| 名称  | 代码位置  | 具体功能 |
|:------------- |:---------------:|:-------------:|
| 数据层   | hedgehog\_base\_core |     redis/mongo dao层 |
| 下载层     | hedgehog\_base\_download        |     下载机的部署,下载方法的继承实现 |
| 中间件层 | hedgehog\_base\_middleware        |      中间件的开发及调用 |
| 支持层 | hedgehog\_base\_support        |        监控系统、后台、日志分析|

![MacDown Screenshot](http://dyt1.oss-cn-shenzhen.aliyuncs.com/dianyou/data/circle/img/20180912/1d6b132db63d951d3f96d774b5966243.jpg
)


### 配置与部署
TODO
### 细节
TODO
### 订正
TODO

## 分发层架构
分发层架构就是一个Scrapy项目，只不过它不再与下载有关，你使用多协程也没有任何意义，最终下载队列长度在redis上会有上限max。该下载分发架构基于redis是一个纯异步模型，所以每个任务应该全程携带所有信息，避免与其他任务

或者全局变量交互产生线程安全问题。


### 配置与部署
TODO
### 细节
TODO
### 订正
TODO


## 其他

### Strong and Emphasize

**Strong**: `**Strong**` or `__Strong__` (Command-B)  
*Emphasize*: `*Emphasize*` or `_Emphasize_`[^emphasize] (Command-I)

### Headers (like this one!)

	Header 1
	========

	Header 2
	--------

or

	# Header 1
	## Header 2
	### Header 3
	#### Header 4
	##### Header 5
	###### Header 6



### Links and Email
#### Inline
Just put angle brackets around an email and it becomes clickable: <uranusjr@gmail.com>  
`<uranusjr@gmail.com>`  

Same thing with urls: <http://macdown.uranusjr.com>  
` <http://macdown.uranusjr.com>`  

Perhaps you want to some link text like this: [Macdown Website](http://macdown.uranusjr.com "Title")  
`[Macdown Website](http://macdown.uranusjr.com "Title")` (The title is optional)  


#### Reference style
Sometimes it looks too messy to include big long urls inline, or you want to keep all your urls together.  

Make [a link][arbitrary_id] `[a link][arbitrary_id]` then on it's own line anywhere else in the file:  
`[arbitrary_id]: http://macdown.uranusjr.com "Title"`
  
If the link text itself would make a good id, you can link [like this][] `[like this][]`, then on it's own line anywhere else in the file:  
`[like this]: http://macdown.uranusjr.com`  

[arbitrary_id]: http://macdown.uranusjr.com "Title"
[like this]: http://macdown.uranusjr.com  


### Images
#### Inline
`![Alt Image Text](path/or/url/to.jpg "Optional Title")`
#### Reference style
`![Alt Image Text][image-id]`  
on it's own line elsewhere:  
`[image-id]: path/or/url/to.jpg "Optional Title"`


### Lists

* Lists must be preceded by a blank line (or block element)
* Unordered lists start each item with a `*`
- `-` works too
	* Indent a level to make a nested list
		1. Ordered lists are supported.
		2. Start each item (number-period-space) like `1. `
		42. It doesn't matter what number you use, I will render them sequentially
		1. So you might want to start each line with `1.` and let me sort it out

Here is the code:

```
* Lists must be preceded by a blank line (or block element)
* Unordered lists start each item with a `*`
- `-` works too
	* Indent a level to make a nested list
		1. Ordered lists are supported.
		2. Start each item (number-period-space) like `1. `
		42. It doesn't matter what number you use, I will render them sequentially
		1. So you might want to start each line with `1.` and let me sort it out
```



### Block Quote

> Angle brackets `>` are used for block quotes.  
Technically not every line needs to start with a `>` as long as
there are no empty lines between paragraphs.  
> Looks kinda ugly though.
> > Block quotes can be nested.  
> > > Multiple Levels
>
> Most markdown syntaxes work inside block quotes.
>
> * Lists
> * [Links][arbitrary_id]
> * Etc.

Here is the code:

```
> Angle brackets `>` are used for block quotes.  
Technically not every line needs to start with a `>` as long as
there are no empty lines between paragraphs.  
> Looks kinda ugly though.
> > Block quotes can be nested.  
> > > Multiple Levels
>
> Most markdown syntaxes work inside block quotes.
>
> * Lists
> * [Links][arbitrary_id]
> * Etc.
```
  
  
### Inline Code
`Inline code` is indicated by surrounding it with backticks:  
`` `Inline code` ``

If your ``code has `backticks` `` that need to be displayed, you can use double backticks:  
```` ``Code with `backticks` `` ````  (mind the spaces preceding the final set of backticks)


### Block Code
If you indent at least four spaces or one tab, I'll display a code block.

	print('This is a code block')
	print('The block must be preceded by a blank line')
	print('Then indent at least 4 spaces or 1 tab')
		print('Nesting does nothing. Your code is displayed Literally')

I also know how to do something called [Fenced Code Blocks](#fenced-code-block) which I will tell you about later.

### Horizontal Rules
If you type three asterisks `***` or three dashes `---` on a line, I'll display a horizontal rule:

***


## <a name="markdown-pane"></a>The Markdown Preference Pane
This is where I keep all preferences related to how I parse markdown into html.  
![Markdown preferences pane](http://d.pr/i/RQEi+)

### Document Formatting
The ***Smartypants*** extension automatically transforms straight quotes (`"` and `'`) in your text into typographer’s quotes (`“`, `”`, `‘`, and `’`) according to the context. Very useful if you’re a typography freak like I am. Quote and Smartypants are syntactically incompatible. If both are enabled, Quote takes precedence.


### Block Formatting

#### Table

This is a table:

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

You can align cell contents with syntax like this:

| Left Aligned  | Center Aligned  | Right Aligned |
|:------------- |:---------------:| -------------:|
| col 3 is      | some wordy text |         $1600 |
| col 2 is      | centered        |           $12 |
| zebra stripes | are neat        |            $1 |

The left- and right-most pipes (`|`) are only aesthetic, and can be omitted. The spaces don’t matter, either. Alignment depends solely on `:` marks.

#### <a name="fenced-code-block">Fenced Code Block</a>

This is a fenced code block:

```
print('Hello world!')
```

You can also use waves (`~`) instead of back ticks (`` ` ``):

~~~
print('Hello world!')
~~~


You can add an optional language ID at the end of the first line. The language ID will only be used to highlight the code inside if you tick the ***Enable highlighting in code blocks*** option. This is what happens if you enable it:

![Syntax highlighting example](http://d.pr/i/9HM6+)

I support many popular languages as well as some generic syntax descriptions that can be used if your language of choice is not supported. See [relevant sections on the official site](http://macdown.uranusjr.com/features/) for a full list of supported syntaxes.


### Inline Formatting

The following is a list of optional inline markups supported:

Option name         | Markup           | Result if enabled     |
--------------------|------------------|-----------------------|
Intra-word emphasis | So A\*maz\*ing   | So A<em>maz</em>ing   |
Strikethrough       | \~~Much wow\~~   | <del>Much wow</del>   |
Underline [^under]  | \_So doge\_      | <u>So doge</u>        |
Quote [^quote]      | \"Such editor\"  | <q>Such editor</q>    |
Highlight           | \==So good\==    | <mark>So good</mark>  |
Superscript         | hoge\^(fuga)     | hoge<sup>fuga</sup>   |
Autolink            | http://t.co      | <http://t.co>         |
Footnotes           | [\^4] and [\^4]: | [^4] and footnote 4   |

[^4]: You don't have to use a number. Arbitrary things like `[^footy note4]` and `[^footy note4]:` will also work. But they will *render* as numbered footnotes. Also, no need to keep your footnotes in order, I will sort out the order for you so they appear in the same order they were referenced in the text body. You can even keep some footnotes near where you referenced them, and collect others at the bottom of the file in the traditional place for footnotes. 




## <a name="rendering-pane"></a>The Rendering Preference Pane
This is where I keep preferences relating to how I render and style the parsed markdown in the preview window.  
![Rendering preferences pane](http://d.pr/i/rT4d+)

### CSS
You can choose different css files for me to use to render your html. You can even customize or add your own custom css files.

### Syntax Highlighting
You have already seen how I can syntax highlight your fenced code blocks. See the [Fenced Code Block](#fenced-code-block) section if you haven’t! You can also choose different themes for syntax highlighting.

### TeX-like Math Syntax
I can also render TeX-like math syntaxes, if you allow me to.[^math] I can do inline math like this: \\( 1 + 1 \\) or this (in MathML): <math><mn>1</mn><mo>+</mo><mn>1</mn></math>, and block math:

\\[
    A^T_S = B
\\]

or (in MathML)

<math display="block">
    <msubsup><mi>A</mi> <mi>S</mi> <mi>T</mi></msubsup>
    <mo>=</mo>
    <mi>B</mi>
</math>



### Task List Syntax
1. [x] I can render checkbox list syntax
	* [x] I support nesting
	* [x] I support ordered *and* unordered lists
2. [ ] I don't support clicking checkboxes directly in the html window


### Jekyll front-matter
If you like, I can display Jekyll front-matter in a nice table. Just make sure you put the front-matter at the very beginning of the file, and fence it with `---`. For example:

```
---
title: "Macdown is my friend"
date: 2014-06-06 20:00:00
---
```

### Render newline literally
Normally I require you to put two spaces and a newline (aka return) at the end of a line in order to create a line break. If you like, I can render a newline any time you end a line with a newline. However, if you enable this, markdown that looks lovely when I render it might look pretty funky when you let some *other* program render it.





## <a name="general-pane"></a>The General Preferences Pane

This is where I keep preferences related to application behavior.  
![General preferences pane](http://d.pr/i/rvwu+)

The General Preferences Pane allows you to tell me how you want me to behave. For example, do you want me to make sure there is a document open when I launch? You can also tell me if I should constantly update the preview window as you type, or wait for you to hit `command-R` instead. Maybe you prefer your editor window on the right? Or to see the word-count as you type. This is also the place to tell me if you are interested in pre-releases of me, or just want to stick to better-tested official releases.  

## <a name="editor-pane"></a>The Editor Preference Pane
This is where I keep preferences related to the behavior and styling of the editing window.  
![Editor preferences pane](http://d.pr/i/6OL5+)


### Styling

My editor provides syntax highlighting. You can edit the base font and the coloring/sizing theme. I provided some default themes (courtesy of [Mou](http://mouapp.com)’s creator, Chen Luo) if you don’t know where to start.

You can also edit, or even add new themes if you want to! Just click the ***Reveal*** button, and start moving things around. Remember to use the correct file extension (`.styles`), though. I’m picky about that.

I offer auto-completion and other functions to ease your editing experience. If you don’t like it, however, you can turn them off.





## Hack On

That’s about it. Thanks for listening. I’ll be quiet from now on (unless there’s an update about the app—I’ll remind you for that!).

Happy writing!


[^emphasize]: If **Underlines** is turned on, `_this notation_` will render as underlined instead of emphasized 

[^under]: If **Underline** is disabled `_this_` will be rendered as *emphasized* instead of being underlined.

[^quote]: **Quote** replaces literal `"` characters with html `<q>` tags. **Quote** and **Smartypants** are syntactically incompatible. If both are enabled, **Quote** takes precedence. Note that **Quote** is different from *blockquote*, which is part of standard Markdown.

[^math]: Internet connection required.


