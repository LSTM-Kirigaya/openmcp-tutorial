## 前言

本篇教程，演示一下如何使用 go 语言写一个可以访问 neo4j 数据库的 mcp 服务器。实现完成后，我们不需要写任何 查询代码 就能通过询问大模型了解服务器近况。

---

## 1. 准备

项目结构如下：

```bash
📦neo4j-go-server
 ┣ 📂util
 ┃ ┗ 📜util.go      # 工具函数
 ┣ 📜main.go        # 主函数
 ┗ 📜neo4j.json     # 数据库连接的账号密码
```

我们先创建一个 go 项目：

```bash
mkdir neo4j-go-server
cd neo4j-go-server
go mod init neo4j-go-server
```

创建 neo4j.json，填写 neo4j 数据库的连接信息：

```json
{
    "url" : "neo4j://101.43.239.71:7687",
    "name" : "neo4j",
    "password" : "neo4j"
}
```

## 2. 验证数据库连通性

首先，根据我的教程在本地或者服务器配置一个 neo4j 数据库：[neo4j 数据库安装与配置](https://kirigaya.cn/blog/article?seq=199)

为了验证数据库的连通性，我们需要先写一段数据库访问的最小系统。

先安装 neo4j 的 v5 版本的 go 驱动：
```bash
go get github.com/neo4j/neo4j-go-driver/v5
```

在 `util.go` 中添加以下代码：

```go
package util

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

var (
	Neo4jDriver neo4j.DriverWithContext
)

// 创建 neo4j 服务器的连接
func CreateNeo4jDriver(configPath string) (neo4j.DriverWithContext, error) {
	jsonString, _ := os.ReadFile(configPath)
	config := make(map[string]string)

	json.Unmarshal(jsonString, &config)
	// fmt.Printf("url: %s\nname: %s\npassword: %s\n", config["url"], config["name"], config["password"])

	var err error
	Neo4jDriver, err = neo4j.NewDriverWithContext(
		config["url"], 
		neo4j.BasicAuth(config["name"], config["password"], ""),
	)
	if err != nil {
		return Neo4jDriver, err
	}
	return Neo4jDriver, nil
}


// 执行只读的 cypher 查询
func ExecuteReadOnlyCypherQuery(
	cypher string,
) ([]map[string]any, error) {
	session := Neo4jDriver.NewSession(context.TODO(), neo4j.SessionConfig{
		AccessMode: neo4j.AccessModeRead,
	})

	defer session.Close(context.TODO())

	result, err := session.Run(context.TODO(), cypher, nil)
	if err != nil {
		fmt.Println(err.Error())
		return nil, err
	}

	var records []map[string]any
	for result.Next(context.TODO()) {
		records = append(records, result.Record().AsMap())
	}

	return records, nil
}
```

main.go 中添加以下代码：

```go
package main

import (
	"fmt"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
	"neo4j-go-server/util"
)

var (
	neo4jPath    string = "./neo4j.json"
)

func main() {
	_, err := util.CreateNeo4jDriver(neo4jPath)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Neo4j driver created successfully")	
}
```

运行主程序来验证数据库的连通性：
```bash
go run main.go
```
如果输出了 `Neo4j driver created successfully`，则说明数据库的连通性验证通过。

## 3. 实现 mcp 服务器

go 的 mcp 的 sdk 最为有名的是 mark3labs/mcp-go 了，我们就用这个。

> mark3labs/mcp-go 的 demo 在 https://github.com/mark3labs/mcp-go，非常简单，此处直接使用即可。

```bash
go get github.com/mark3labs/mcp-go
```

在 `main.go` 中添加以下代码：q