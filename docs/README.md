文档源码地址：
<a href="https://rabbitai.sgic.net.cn">rabbitai.sgic.net.cn</a>

该站点运行在 Gatsby 框架下并使用 `Documentation` 节。

## 入门

```bash
cd docs/
npm install
npm run start
# navigate to localhost:8000`
```

## 发布

Github Actions CI在将更改合并到主站点后自动发布站点。

要手动发布，需要推送 Gatsby 生成的静态站点
至[psbsgic/rabbitai-site](https://github.com/psbsgic/rabbitai-site/)库的 `asf-site` 分支，
不需要PR，只需 `git push`。

```bash
# 在主 repo 中获取 docs/ 文件夹
cd ~/repos/rabbitai/docs
# Gatsby 构建静态网站，网站目录：`docs/public`
npm run build

# 跳转到 docs repo
cd ~/repos/rabbitai-site
# 签出正确的分支
git checkout asf-site

# BE CAREFUL WITH THIS COMMAND
# wipe the content of the repo
rm -rf *

# 在这里复制静态站点
cp -r ~/repos/rabbitai/docs/public/ ./

# git push
git add .
git commit -m "relevant commit msg"
git push origin asf-site

# 成功-需要几分钟才能在rabbitai.sgic.net.cn上生效
```
