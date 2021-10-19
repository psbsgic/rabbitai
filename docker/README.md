# 使用 Docker 入门指南

Docker是开始 Rabbitai 的一个简单方法。

## 先决条件

1. Docker! [link](https://www.docker.com/get-started)
2. Docker-compose [link](https://docs.docker.com/compose/install/)

## 配置

`/app/pythonpath` 文件夹是从 [`./docker/pythonpath_dev`](./pythonpath_dev) 挂接的。
它包含用于本地开发的基本配置 [`./docker/pythonpath_dev/rabbitai_config.py`](./pythonpath_dev/rabbitai_config.py)。

### 本地重写

为了在本地重写配置选项，简单地复制 [`./docker/pythonpath_dev/rabbitai_config_local.example`](./pythonpath_dev/rabbitai_config_local.example)
为 `./docker/pythonpath_dev/rabbitai_config_docker.py`，并填写相关配置项。

### 本地软件包

如果您想添加Python包以便在本地测试数据库之类的东西，只需添加一个本地 requirements.txt (`./docker/requirements-local.txt`)并重建docker堆栈。

步骤:

1. 创建 `./docker/requirements-local.txt`
2. 添加新软件包
3. 重建 docker-compose
    1. `docker-compose down -v`
    2. `docker-compose up`

## 初始化数据库

数据库将在启动时通过init容器初始化自身 ([`rabbitai-init`](./docker-init.sh))。这可能需要一分钟。

## 正常运行

要运行容器，只需运行：`docker-compose up`

等待几分钟 Rabbitai 初始化完成后，您可以打开浏览器并查看[`http://localhost:8088`](http://localhost:8088)
开始你的旅程。

## 研发

运行时，在修改Rabbitai的Python和JavaScript源代码时容器服务器将重新加载。不过，别忘了重新加载页面以考虑新的前端。

## 生产

可以使用 [`docker-compose-non-dev.yml`](../docker-compose-non-dev.yml)在非开发模式下运行Rabbitai。
此文件不包括开发所需的卷，并使用 [`./docker/.env-non-dev`](./.env-non-dev) 将变量 `RABBITAI_ENV` 设置为 `production`。

## 资源限制

如果您试图在macOS上构建，并且它以137退出，那么您需要增加Docker资源。
参见[此处](https://docs.docker.com/docker-for-mac/#advanced) 的说明（搜索内存）。
