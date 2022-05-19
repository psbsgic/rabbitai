# RabbitAI 简介
RabbitAI 的前端主要用到了 React 和 NVD3/D3，而后端则基于 Python 的 Flask 框架和 Pandas、SQLAlchemy 等依赖库，主要提供了这几方面的功能：

- 集成数据查询功能，支持多种数据库，包括 MySQL、PostgresSQL、Oracle、SQL Server、SQLite、SparkSQL 等，并深度支持 Druid。
- 通过 NVD3/D3 预定义了多种可视化图表，满足大部分的数据展示功能。如果还有其他需求，也可以自开发更多的图表类型，或者嵌入其他的 JavaScript 图表库（如 HighCharts、ECharts）。
- 提供细粒度安全模型，可以在功能层面和数据层面进行访问控制。支持多种鉴权方式（如数据库、OpenID、LDAP、OAuth、REMOTE_USER 等）。

# 运行 RabbitAI

1. 初始化数据库

```sh
rabbitai db upgrade
```

2. 创建一个系统管理员用户

```
rabbitai fab create-admin
```

3. 创建默认角色和权限

```sh
rabbitai init
```

4. 加载示例

```sh
rabbitai load_examples
```

5. 启动 Rabbitai

```sh
rabbitai run -p 8088 --with-threads --reload --debugger --host=0.0.0.0
rabbitai run -p 8088 --with-threads --reload --debugger --host=127.0.0.1
```

