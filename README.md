# OpenCV 部分的简介

## 前言

题目中的图像识别肯定要用到`OpenCV`，我这边是打算用`树莓派`来处理，并采用`Python`编写。

下面是原本的题目，我贴在这里。

## 题目： 环路检测飞行器

### 一、任务

设计制作一架四旋翼自主飞行器，飞行器上装有激光灯，能够对环形道路进行缺陷检测。飞行区域俯视图如图 1 所示。  
![图一](/1.jpg)  
俯视图说明：

- 起降点 A 为一红色实心圆，直径为`40cm`，缺陷点 B 为一绿色实心圆，直径为`40cm`。  
- AB 两圆放置在直线围成的正方形框上，直线宽度为 `3cm`，边长为 `250cm`。其中，A 圆放置在某一顶点上，B 圆随机放置在任意一条边的非顶点位置。  
- 停靠点 C 位于正方形中心位置（距离左右上下均为 1.25m），地图中的停靠点 C 仅做示意用，在地图中很小，无法通过图像识别，仅供判定成绩用。  

### 二、要求

#### 1、基本要求

1. 装有激光灯的四旋翼自主飞行器（以下简称飞行器）摆放在图 1 所示的起降点 A 中心，起飞并在 1.3m 高度悬停。（15 分）  
2. 飞行器能沿图 1 所示的矩形框完成闭合环路飞行并回到起降点 A，环绕方向任意。（35 分）  
3. 飞行器能够降落在起降点 A 中心。（10 分）  

#### 2．发挥部分

- 在基本要求（2）的前提下，飞行器能够在环路飞行过程中发现道路缺陷区域 B，同时打开激光笔标识缺陷区域中心位置，持续5s。(25 分)  
- 在基本要求（2）的前提下，飞行器完成环路飞行回到 A 点后，能够飞向场地中心停靠点 C 处，悬停 5s 后返回 A 点，再执行基本要求（3）。(15 分)  

### 三、说明

1. 飞行器不得遥控，飞行过程中不得人为干预。  
2. 飞行器飞行期间，触及地面或保护网后自行恢复飞行的，酌情扣分；触地触网后 5s 内不能自行恢复飞行视为失败，失败前完成的部分仍计分。  
3. 整个飞行过程中高度应始终保持在 1.3m 左右。  
4. 整个飞行过程中激光器光点落在圆 B 以外区域均酌情扣分。  
5. 要求图像处理对环境具有自适应性，能够适应不同光照强度、地面背景，不接受任何对光照的特殊要求。  

## 分析

这个题目对于图像识别的要求不是特别高，就像那个学长分析的那样，我们只需要做最简单的分析就行了。

首先是在红色位置起飞，定高1.3m。然后彩色摄像头在红色边框周围寻找黑色线条，应该会有两个。随便选择其中一个然后开始寻迹。找到一个直角边以后转弯，如果遇到绿色标记就执行发挥2的任务，直到再次找到红色点。根据之前的陀螺仪数据计算出整个矩形边框的长宽，然后到中央c点。然后返回A点降落。

### 细分成小的函数

红点任务函数，飞机起飞的时候会识别到，应该是寻找红色点边缘的黑色线条，应该有两条，我们按照顺时针绕黑线飞行的话就是顺时针第一个黑色线。然后开始执行沿着黑线运行的函数

需要一个能沿着摄像头的画面中黑线前进的函数，能自动纠正偏移并且能分辨出直角转弯和红绿点并执行红绿任务点的函数(这个任务相对简单，只有3个直角转弯的地方，可以写死转弯次数和大概的前进距离)

定高1.3m函数，飞控应该有提供相关功能

发挥部分，优先级低

- 绿点任务函数，在基本要求（2）的前提下，飞行器能够在环路飞行过程中发现道路缺陷区域 B，同时打开激光笔标识缺陷区域中心位置，持续5s

- 计算中心点位置，移动过去

## Windows下的配置

### 0. 安装python，并正确配置和安装环境

<details>
<summary>conda配置方法</summary>

---

#### 1. 安装和配置conda

1. 首先安装Python和Anaconda，参照上面的视频[如何搭建Python-OpenCV环境](https://cloud.lwqwq.com/s/vdoUQ/video?name=opencv%E9%85%8D%E7%BD%AE%E6%96%B9%E6%B3%95_x264.mp4&share_path=%2F%E8%A7%86%E9%A2%91%E8%B5%84%E6%BA%90%2Fopencv%E9%85%8D%E7%BD%AE%E6%96%B9%E6%B3%95_x264.mp4)

2. 配置conda环境变量，按照你conda安装的位置来，比如你安装在`D:\anaconda3\`则需要添加的path有下面四条

```commandline
D:\anaconda3\
D:\anaconda3\Scripts
D:\anaconda3\Library\bin
D:\anaconda3\Library\mingw-w64
```

3. 然后需要开启Powershell运行PS脚本的限制

**右键**`开始菜单按钮`，点击`Windows PowerShell(管理员)(A)`,然后输入

```commandline
set-executionpolicy remotesigned
```

会出现下面的信息

```commandline
执行策略更改
执行策略可帮助你防止执行不信任的脚本。更改执行策略可能会产生安全风险，如 https:/go.microsoft.com/fwlink/?LinkID=135170
中的 about_Execution_Policies 帮助主题所述。是否要更改执行策略?
[Y] 是(Y)  [A] 全是(A)  [N] 否(N)  [L] 全否(L)  [S] 暂停(S)  [?] 帮助 (默认值为“N”):
```

然后输入大写的`Y`，敲击回车

继续输入

```commandline
Get-ExecutionPolicy
```

如果显示的是 `RemoteSigned`说明设置成功了

4. 接下来需要初始化conda环境，在powershell中继续输入

```commandline
conda init powershell
```

然后关闭powershell

到这边你已经完成了conda环境的初始化

#### 2. 配置conda环境

首先创建一个conda环境,`<你的conda环境名称>`可以自定义，我这边是`opencv`,后面的python版本我选择的是3.10,conda会自动搜索3.10最新版本，所有代码都在3.10.4的环境下测试通过

```commandline
conda create -n <你的conda环境名称> python=3.10
```

#### 如果遇到conda下载速度慢，请查看这里

两种方法

1.如果你有代理服务器，在终端中输入

```commandline
$Env:http_proxy="http://127.0.0.1:7890";$Env:https_proxy="http://127.0.0.1:7890"
#改成你自己的端口号
```

2.如果你没有代理服务器，可以使用conda镜像

同时按下`windows徽标键`+`R`，在左下角弹出界面输入框内输入`powershell`

在powershell中输入`conda config --set show_channel_urls yes`

同时按下`windows徽标键`+`R`

在左下角弹出的窗口内输入`notepad %HOMEPATH%\.condarc`然后点击确定

在弹出的记事本中所有的文字删除，并以下面的文字替代

```
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

然后按`Ctrl`+`S`保存修改

安装环境的时候可能会提示是否安装，按照提示输入y就可以了

接下来进入`opencv`环境

```commandline
conda activate <你的conda环境名称>
```

这个时候你的终端最左侧应该会从`(base)`变成`(opencv)`或者`<你的conda环境名称>`

<!-- 接下来需要安装一些包，在安装之前你可能需要配置一下pip，不然速度会很慢

> - 如果你有代理软件并使用`Powershell`,输入`$env:HTTP_PROXY="http://127.0.0.1:改成你的端口"`和`$env:HTTPS_PROXY="http://127.0.0.1:改成你的端口"`设置终端代理
> - 如果你没有代理软件可以尝试[pip一行命令换源](https://www.cnblogs.com/137point5/p/15000954.html) -->

<!-- 我们需要安装下面这些包

```commandline
pip install opencv-python
pip install imutils
pip install opencv-contrib-python
pip install argparse
``` -->

---

</details>

### 1. 克隆仓库

哦，你或许需要先配置一下git，自己去b站搜教程吧，我就不多讲了

拿着[这个](https://www.runoob.com/git/git-tutorial.html)吧，可以当作cheatsheet

### 2. 配置你的IDE

<details>
<summary>Pycharm 配置</summary>

---

首先，我们安装的是社区版的Pycharm，当然你有专业版也没问题

然后看这个教程设置中文[[知乎]如何安装pycharm并设置为中文。](https://zhuanlan.zhihu.com/p/454935826)

然后点击左上方`文件-打开`，定位到`little-quadcopter`文件夹，点击**确定**

这个时候你已经打开了整个项目，main.py是整个程序的入口

点击下方的**终端**按钮，会打开一个熟悉的powershell窗口，输入 `conda activate <你的conda环境名称>` 来进入前面配置好的conda环境

接下来cd到项目文件夹，在终端输入`python .\setup.py`并回车运行，初始化环境

默认使用tuna镜像源下载，如果你有代理服务器可以加上代理服务器地址，例如`python .\setup.py --proxy http://127.0.0.1:7890`

这就准备完了，输入`python .\main.py -h` 查看帮助

---

</details>

<details>
<summary>VS Code 配置方法</summary>

---

首先打开项目文件夹，然后右下角会提示安装推荐插件，就全部安装就行，插件的配置前面视频里有讲

然后按`ctrl`+`shift`+`p`调出命令窗口，输入`python`,选择python解释器一项，选择你自己配置的环境

然后点击上方终端，新建终端，会自动帮你激活你的conda环境

接下来cd到项目文件夹，在终端输入`python .\setup.py`并回车运行，初始化环境

默认使用tuna镜像源下载，如果你有代理服务器可以加上代理服务器地址，例如`python .\setup.py --proxy http://127.0.0.1:7890`

这就准备完了，输入`python .\main.py -h` 查看帮助

---

</details>
