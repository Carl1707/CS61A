#基本学习流程
## python环境

1. 打开 Windows PowerShell。
    
2. 运行 conda activate CS61A 进入你的学习环境。 #使用anoconda为CS61A创建一个环境
    
3. cd 到你存放作业的目录。
    
4. 运行 python ok 来测试作业。
    
5. 所有命令（python, pip 等）都会在这个纯净的 cs61a 环境中执行，与系统和其他项目完全隔离。


## 工作流程

#### 1. 先看课程视频 利用b站精翻版的资源

#### 2. 再做discussion,把官网上的 disc 问题存在py文件里面，写完代码之后使用终端进行测试
* 在官网阅读题目要求
- 切换到你的 VS Code，在 disc01.py 文件里开始写这个函数。
- **如何测试你的代码？**
    1. **简单 print 测试**：在文件末尾写 print(is_prime(10))，然后在终端运行 python disc01.py，看输出是不是你想要的。
        
    2. **使用交互式解释器 (推荐!)**：在终端里运行 python -i disc01.py。这个 -i 参数非常强大，它会先执行你的文件，然后进入一个包含了你文件中所有函数和变量的交互式环境。这时你可以手动调用 is_prime(7)，is_prime(10) 等来测试。

#### 3.再做lab
1. 从课程官网下载lab的zip文件
2. 使用  Expand-Archive -Path <source> -DestinationPath <destination> 命令进行解压
3. 在IDE中对py文件进行编辑
4. 在IDE终端里运行测试脚本（在lab01目录下）
   运行所有公开的测试用例
    python ok
   关于ok，详见[ok](https://cs61a.org/articles/using-ok/)

#### 4.最后完成HW、proj
   所有步骤与lab相同

#### 5.disc,lab,HW的讲解
1. disc 和 lab 都有 Solution来讲解，
2. disc还有walkthrough视频来讲解
3. HW、proj可以看往年题解以获取思路
