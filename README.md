<div align="center">


# IronsBot
赛尔号信息查询机器人👊🤖🔥

[![Python](https://img.shields.io/badge/python->=3.10-blue.svg)](https://python.org) [![GPL-3.0](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![SeerAPI](https://img.shields.io/badge/SeerAPI-v104-blue.svg)](https://github.com/SeerAPI)
</div>

> 本项目原作是 [**@火火**] 开发的西塔伦Bot，谨以此项目向 [**@火火**] 致敬，感谢他为赛尔号玩家社区所做的贡献，愿火种永存。
> 
> 本项目继承了西塔伦Bot的数据查询功能，不包含配置投稿/推荐功能，这些功能请查看[这个链接]()获取更多信息。

## 部署
与西塔伦Bot不同，本项目不提供托管服务，用户需要自行部署。

硬性需求：
- 一台可运行操作系统并可以访问网络的计算机
- 一个QQ账号


### 在 Linux 上部署（推荐）

#### 前置要求

- [Docker Engine](https://docs.docker.com/engine/install/) 和 [Docker Compose](https://docs.docker.com/compose/install/)
- 一个 OneBot 实现端

我们使用[NapCat](https://github.com/NapNeko/NapCatQQ)作为OneBot实现端为例。
#### 1. 创建工作目录

```bash
mkdir -p ~/ironsbot && cd ~/ironsbot
```

#### 2. 创建 docker-compose.yml

创建 `docker-compose.yml` 文件，将以下示例配置粘贴进去，并根据注释修改对应的值：

```yaml
version: "3"

services:
  ironsbot:
    image: ghcr.io/nattsu39/ironsbot:latest
    environment:
      # === 表情包插件必填配置，当缺少时相关命令将被禁用 ===
      MEMES_CNB_TOKEN: "你的CNB令牌"
      
      # === 表情包插件可选配置 ===
      # MEMES_CNB_REPO: "Nattsu39/tudou"
      
      # === 赛尔号数据查询插件必填配置 ===
      DATABASE_URL: "sqlite:///seerapi-data.sqlite"

      # === db_sync 插件必填配置 ===
      DB_SYNC_URL: "https://github.com/SeerAPI/api-data/releases/download/latest/seerapi-data.sqlite"
      # === db_sync 插件可选配置 ===
      # DB_SYNC_INTERVAL_MINUTES: "60"
      # DB_SYNC_PATH: "seerapi-data.sqlite"
      # DB_SYNC_ON_STARTUP: "true"

      # --- 机器人配置（以下均为默认值，按需修改） ---
      # HOST: "0.0.0.0"
      # PORT: "8080"                  # 修改后需同步更新上方 ports 映射
      # COMMAND_START: '[""]'
      # SUPERUSERS: '[]'

    restart: always

  napcat:
    image: mlikiowa/napcat-docker:latest
    container_name: napcat
    restart: always
    mac_address: 02:42:ac:11:00:02 # 自行设置

    environment:
      - NAPCAT_UID=${NAPCAT_UID}
      - NAPCAT_GID=${NAPCAT_GID}
    
    ports:
      - 6099:6099

    volumes:
      - ./napcat/config:/app/napcat/config
      - ./ntqq:/app/.config/QQ
```

完整的变量说明请参考仓库中的 [`.env.example`](.env.example)。

#### 3. 启动服务

```bash
docker compose up -d
```

查看日志确认启动成功：

```bash
docker compose logs -f
```

#### 4. 初始化 NapCat

两个容器处于同一 Compose 网络中，可以通过服务名互相访问。在 NapCat 的配置中，将反向 WebSocket 地址设置为：

```
ws://ironsbot:8080/onebot/v11/ws
```

> `ironsbot` 是 `docker-compose.yml` 中定义的服务名，Compose 会自动将其解析为对应容器的内部 IP。

### 在 Windows 上部署
待补充

## 协议
本项目采用 GPL-3.0 协议，请遵守协议内容。

## ❤️ 特别鸣谢

- [@聿聿](https://github.com/WhY15w)
- [@火火](https://github.com/Yogurt114514)
- [@星空](https://github.com/sptsaixiaoxi)

[**@火火**]: https://github.com/Yogurt114514
