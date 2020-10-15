



# 0. Common

- `name` | string
  - 设置trace的名字，会出现在legend和hover上
- `showlegend` | boolean
  - Default: True
  - 虽然default为True, 但当只有一个trace的时候需要写出才能显示legend, 两个及以上trace自动显示legend

- `hoverinfo` | string
  - Default:'all'
  - 用来判断hover显示的内容包扩什么(x轴、y轴、text内容、name内容)
  - 将`x`,  `y`,  `z`, `text`, `name` 通过 `+` 各自拼接到一起,判断显示什么内容；或者直接用`all`, `none`, `skip`中的一个
  - e.g. `x+text`; `y+text+name`
- `hoverlabel` | dict
  - `bgcolor`
    - 用来设置hover的背景颜色
  - `bordercolor`
    - 用来设置hover边框的颜色
  - `font` | dict
    - 用来设置 `hoverlabel` 的字体属性
    - `size` 
      - 需要大于等于1
    - `color` 
      - 可以使用'green' / 'rgb(255,255,255)' 
  - `namelength` | int 
    - Default: 15
    - 用于确认`name` 的长度
    - 当为-1时，则show the whole name regardless of length
- `hovertext` | string / array
  - Default = ''
  - 用来显示hover里的文字
  - 为string时则所有点都显示同一个`hovertext`; 为array时则各点有自己的`hovertext`
  - 可被`hoverinfo`控制是否显示

- `text` | string / array
  - Default = ''
  - 当为string时，图上每一个点都会带上这个`text`
  - 当为array时，图上每一个点都会带上对应index在array里的string
  - 可以通过`mode` 来决定是否使用text



# 1. Scatter / Line Charts

`import plotly.graph_objs as go`

`go.Scatter()`



- `x`| list / array / pandas / string / datetime
  - 输入x轴的数据
- `y` | list / array / pandas / string / datetime
  - 输入y轴的数据

- `mode` | flaglist string
  - 可以将`'lines'`, `'markers'`,` 'text'` 通过 `'+'` join到一起，或者使用`'none'`
  - 用于图像是否用线相连、是否带上数据点、是否带上text
  - 如果要Line Charts就使用 `'lines'` / 如果要用Scatter 就使用`'markers'`
- `line` | dict
  - `color`
    - 设置线的颜色
  - `width` | int
    - Default: 2
    - 设置线的粗细
  - `shape`  | enumerated: `'linear'` / `'spline'` / `'hv'` / `'vh'` / `'hvh'` / `'vhv'`
    - Default: `'linear'`
    - 线的形状
  - `smoothing` | number between 0 and 1,3
    - Default = 1
    - 只有当`shape = 'spline'` 时才生效, 值越大线约平滑
  - `dash` | string
    - Default = `'solid'`
    - 用于描述线的风格，比如直接实线连接，还是通过和密集的点去描绘线
    - `'solid'` / `'dot'` / `'dash'` / `'longdash'` / `'dashdot'` / `'longdashdot'`
- `fill`  | enumerated : `'none'` / `'tozeroy'` / `'tozerox'` / `'tonexty'` / `'tonextx'` / `'toself'` / `'tonext'`
  - Default = `'none'`
  - 将线的上/下方用颜色填充并且选择填充方式
- `fillcolor` | color
  - 只有在`fill != 'none'` 的时候才生效
  - 选择填充颜色
- `marker` | dict
  - `symbol` | 特别多
    - Default = `'circle'`
    - 用于控制图内数据点的形状 | 具体请参考reference
  - `opacity` | number between 0 to 1
    - 透明度
  - `size` | number greater or equal to 0
    - Default = 6
    - 标记大小
  - `color` | color
    - 设置标识颜色
- `stackgroup` | string
  - Default = ''
  - 将多个scatter在x轴/y轴上相互叠加; 例如两个折线图，当x为0时y值均为100, 则第一个折线图的起点在100, 第二个折线图的起点在200
  - 使用`stackgroup` 默认会启用`fill =  'tonexty'('toonextx')` if `orientation` is 'h'('v')
- `orientation` | 'v' / 'h'
  - Default = 'v'
  - 只有在`stackgroup`启用的时候才会生效
  - 当值为'h'的时候，x轴和y轴互换







# 2. Bar

`import plotly.graph_objs as go`
`go.Bar()`



- `x`| list / array / pandas / string / datetime
  - 输入x轴的数据
- `y` | list / array / pandas / string / datetime
  - 输入y轴的数据
- `text` | string / array
  - Default = ''
  - 当为string时，图上每一个点都会带上这个`text`
  - 当为array时，图上每一个点都会带上对应index在array里的string
  - 可以通过`mode` 来决定是否使用text
- `textposition` | enumerated: `'indside'` / `'outside'` / `'auto'` / `'none'`
  - Default = `'none'`
  - 用于确认text在柱状图里的显示位置
- `textfont` | dict
  - 用于确认text的字体属性
  - `size`
  - `color`
- `orientation` | `'v'` `'h'`
  - 用于设置柱状图是竖着还是横着
- `width` | float
  - 用于设置柱的大小
- `marker` | dict
  - `line` | dict
    - `width`
      - 用于设置柱边框大小
    - `color`
      - 用于设置柱边框颜色
  - `color`
    - 用于设置柱本身颜色
- `还有其他许多关于柱的设置未写`







# 3. Pie

`import plotly.graph_objs as go`
`go.Pie()`



- `values` | list / array / series/ strings / datetimes
  - 用于设置饼图每个区域的值
- `domain` | dict
  - `x` | list
    - Default:[0, 1]
    - 用来设置x轴的占比
    - 可以看成x轴上的[左坐标值，右坐标值]
  - `y` | list
    - Default:[0, 1]
    - 用来设置y轴的占比
    - 可以看成y轴上的[左坐标值，右坐标值]

- `hole` | number between 0  and 1
  - Default:0
  - 用来设置饼图中间空洞的大小
- `rotation` | number between -360 to 360
  - Default:0
  - 用来设置饼图的旋转角度



# 4. Histogrm

`go.Histogram`



- `x`| list / array / pandas / string / datetime
  - 输入x轴的数据
- `y` | list / array / pandas / string / datetime
  - 输入y轴的数据
- `orientation` | 'v'/'h'
  - 用来设置histogram的朝向
- `histnorm` | enumerated: `' '` / `'percent'` / `'probability'` / `'density'` / `'probability density'`
  - Default: ' '
  - 用来判断到底是输出什么柱状图；如果是`'percent'` / `'probability'`则显示x值出现的percentage/fraction；如果是`density` 则为在一个bin里出现的次数除以bin之间的inerval；如果是`probability density` 概率密度直方图(pdf)
- `xbins` | dict
  - `start` | number greater than 0
    - 用来指定直方图的起点x坐标
  - `end` | number greater than 0
    - 用来指定直方图的终点x坐标
  - size | number
    - 用来指定直方图的个数
- `ybins` | 同xbins



# 5. BoxPlot

- `whiskerwidth` | number between 0 and 1
  - Default: 0.5
  - 用来描述箱线图上下两条线的长度
- `boxpoints` | enumerated: `'all'` / `'outliers'` / `'suspectedoutliers'` / `False`
  - Default: `'outliers'`
  - 用来描述在箱线图上显示哪些点

- `boxmean` | enumerated: `True` / `'sd'` / `False`
  - Default : False
  - 用来判断是否要显示均值/标准差 | 以虚线形式显示
- `orientation` | enumerated: `v` / `h`
  - 判断朝向
- `marker` | dict
  - `color` 
    - rgba / green
  - `symbol`
    - 用来显示boxpoints里面显示的点，究竟用什么形式
  - `opacity`
  - `size`
- `line` | dict
  - 均用来描述box外一圈线的性质
  - `color`
  - `width`



