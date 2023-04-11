# 示例代码

> 因为数据并未得到授权，所以数据集并未上传到github，请替换为你想处理的数据

## 目录

- `server` 服务端代码
- `data_import` 数据导入代码

## 前期准备

本服务需要使用milvus向量数据库，所以需要先安装milvus，为了方便可以使用docker启动：
`wget https://github.com/milvus-io/milvus/releases/download/v2.2.5/milvus-standalone-docker-compose.yml -O docker-compose.yml`
`sudo docker-compose up -d`

## 关于milvus 向量数据库

你可以查看milvus的官方文档：https://milvus.io/docs
