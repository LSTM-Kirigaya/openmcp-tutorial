## go 实现 neo4j 的只读模式的 mcp 服务器

快速开始你的项目，创建 neo4j.json，填写 neo4j 数据库的连接信息：

```json
{
    "url" : "neo4j://101.43.239.71:7687",
    "name" : "neo4j",
    "password" : "neo4j"
}
```

> 关于如何快速配置和安装 neo4j 数据库的教程：https://kirigaya.cn/blog/article?seq=199

然后运行项目：

```bash
go mod tidy
go run main.go
```