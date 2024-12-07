#!/bin/sh

# 启动开发服务器在后台
npm run dev -- --host 0.0.0.0 &

# 将控制权交给 CMD
exec "$@"
