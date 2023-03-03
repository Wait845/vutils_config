# vutils 系列 - CONFIG
## YAML格式配置文件管理
- 基于watchdog实现的配置文件修改自动更新
- 获取到空配置时，自动将默认配置写到配置文件

## 使用
```Python3
from vutils_config import Config


config = Config("config.yaml")

# 设置一个值
config.set(
    name="main",
    key="mysql",
    value="127.0.0.1"
)

# 读取一个存在的值
db = config.get(
    name="main",
    key="mysql"
)
print(db)
# 127.0.0.1

# 读取一个不存在的值
db = config.get(
    name="main",
    key="redis"
)
print(db)
# None

# 读取一个不存在的值,使用默认值
db = config.get(
    name="main",
    key="redis",
    default="127.0.0.1"
)
print(db)
# 127.0.0.1

# 再次读取该值
db = config.get(
    name="main",
    key="redis"
)
print(db)
# 127.0.0.1
```
