#!/usr/bin/env bash

set -e

#
# 始终首先安装本地覆盖
#
/app/docker/docker-bootstrap.sh

STEP_CNT=4

echo_step() {
cat <<EOF

######################################################################


Init Step ${1}/${STEP_CNT} [${2}] -- ${3}


######################################################################

EOF
}
ADMIN_PASSWORD="admin"
# 如果 Cypress 运行 – 重写管理员密码，导出环境变量
if [ "$CYPRESS_CONFIG" == "true" ]; then
    ADMIN_PASSWORD="general"
    export RABBITAI_CONFIG=tests.rabbitai_test_config
    export RABBITAI_TESTENV=true
    export ENABLE_REACT_CRUD_VIEWS=true
    export RABBITAI__SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://rabbitai:rabbitai@db:5432/rabbitaidb
fi
# 初始化数据库
echo_step "1" "Starting" "Applying DB migrations"
rabbitai db upgrade
echo_step "1" "Complete" "Applying DB migrations"

# 创建管理员用户
echo_step "2" "Starting" "Setting up admin user ( admin / $ADMIN_PASSWORD )"
rabbitai fab create-admin \
              --username admin \
              --firstname Peng \
              --lastname Songbo \
              --email pengsongbo@hotmail.com \
              --password $ADMIN_PASSWORD
echo_step "2" "Complete" "Setting up admin user"
# 创建默认角色和权限
echo_step "3" "Starting" "Setting up roles and perms"
rabbitai init
echo_step "3" "Complete" "Setting up roles and perms"

if [ "$RABBITAI_LOAD_EXAMPLES" = "yes" ]; then
    # 加载示例及其数据
    echo_step "4" "Starting" "Loading examples"
    # 如果 Cypress 配置运行 – 加载必须的测试数据
    if [ "$CYPRESS_CONFIG" == "true" ]; then
        rabbitai load_test_users
        rabbitai load_examples --load-test-data
    else
        rabbitai load_examples
    fi
    echo_step "4" "Complete" "Loading examples"
fi
