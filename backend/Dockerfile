FROM python:3.11-slim

WORKDIR /app

# 安装基本工具
RUN apt-get update && \
    apt-get install -y vim nano less procps && \
    rm -rf /var/lib/apt/lists/*

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY ./app ./app

# 复制并设置 entrypoint 脚本
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# 暴露端口
EXPOSE 8000

# 设置 entrypoint
# ENTRYPOINT ["./docker-entrypoint.sh"]

# 保持容器运行（如果 entrypoint 失败）
CMD ["sh", "-c", "tail -f /dev/null"]
