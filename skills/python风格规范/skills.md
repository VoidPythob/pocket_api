命名规则应该用蛇形命名法
导包格式规则应该是

1. 官方包
2. 第三方依赖
3. 本地包
   如果模块相互处于一个包里面应该用相对导入

项目结构pyproject.toml配置项目的元数据和依赖
项目版本号放在**init**.py的**version** 变量里面
pyproject.toml用setuptools动态加载而不是写死

scripts 放脚本文件
src 放源代码文件
tests 放测试文件

src\项目名 一般项目写在这里
src\项目名\config 放配置文件
src\项目名\model 放orm model代码
src\项目名\service 放业务服务代码
src\项目名\utils 放工具类代码
src\项目\main.py 为项目入口

数据对象尽量用类不用dict传参
如果一个函数参数过多可用Context的形式传参

常量用大写蛇形写法
函数应该使用动词写法
如果是设置属性可以选择使用名词命名

http请求只用post和get，不用其他方法
