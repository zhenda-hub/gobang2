# 使用 Node.js 16 作为基础镜像
FROM node:16-alpine

# 设置工作目录
WORKDIR /app

# 安装基本工具
RUN apk add --no-cache vim nano less procps

# 复制并设置 entrypoint 脚本
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# 暴露端口
EXPOSE 5173

# 设置 entrypoint
# ENTRYPOINT ["./docker-entrypoint.sh"]

# 保持容器运行（如果 entrypoint 失败）
CMD ["sh", "-c", "tail -f /dev/null"]
