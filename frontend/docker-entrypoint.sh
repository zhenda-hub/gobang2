#!/bin/sh

npm install
npm run dev -- --host 0.0.0.0 &

# 将控制权交给 CMD
exec "$@"
