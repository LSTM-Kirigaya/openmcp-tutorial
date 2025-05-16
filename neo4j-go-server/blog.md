##  前言

本篇教程，演示一下如何使用 go 语言写一个可以访问 neo4j 数据库的 mcp 服务器。实现完成后，我们不需要写任何 查询代码 就能通过询问大模型了解服务器近况。

不同于之前的连接方式，这次，我们将采用 SSE 的方式来完成服务器的创建和连接。

本期教程的代码：https://github.com/LSTM-Kirigaya/openmcp-tutorial/tree/main/neo4j-go-server

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

首先，根据我的教程在本地或者服务器配置一个 neo4j 数据库：[neo4j 数据库安装与配置](https://kirigaya.cn/blog/article?seq=199)。安装完成后，你可以通过 py 脚本的方式往数据库里面放置一些随机的数据。

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

先安装

```bash
go get github.com/mark3labs/mcp-go
```

然后在 `main.go` 中添加以下代码：

```go
// ... existing code ...

var (
	addr string = "localhost:8083"
)

func main() {
	// ... existing code ...

	s := server.NewMCPServer(
		"只读 Neo4j 服务器",
		"0.0.1",
		server.WithToolCapabilities(true),
	)

	srv := server.NewSSEServer(s)
	
    // 定义 executeReadOnlyCypherQuery 这个工具的 schema
	executeReadOnlyCypherQuery := mcp.NewTool("executeReadOnlyCypherQuery",
		mcp.WithDescription("执行只读的 Cypher 查询"),
		mcp.WithString("cypher",
			mcp.Required(),
			mcp.Description("Cypher 查询语句，必须是只读的"),
		),
	)
	
    // 将真实函数和申明的 schema 绑定
	s.AddTool(executeReadOnlyCypherQuery, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		cypher := request.Params.Arguments["cypher"].(string)
		result, err := util.ExecuteReadOnlyCypherQuery(cypher)

		fmt.Println(result)

		if err != nil {
			return mcp.NewToolResultText(""), err
		}

		return mcp.NewToolResultText(fmt.Sprintf("%v", result)), nil
	})
	
    // 在 http://localhost:8083/sse 开启服务
    fmt.Printf("Server started at http://%s/sse\n", addr)
	srv.Start(addr)
}

```

go run main.go 运行上面的代码，你就能看到如下信息：

```
Neo4j driver created successfully
Server started at http://localhost:8083/sse
```

说明我们的 mcp 服务器在本地的 8083 上启动了。

## 4. 通过 openmcp 来进行调试

接下来，我们来通过 openmcp 进行调试，先点击 vscode 左侧的 openmcp 图标进入控制面板，如果你是下载的 https://github.com/LSTM-Kirigaya/openmcp-tutorial/tree/main/neo4j-go-server 这个项目，那么你能看到【MCP 连接（工作区）】里面已经有一个创建好的调试项目【只读 Neo4j 服务器】了。如果你是完全自己做的这个项目，可以通过下面的按钮添加连接，选择 sse 后填入 http://localhost:8083/sse，oauth 空着不填即可。

<div align=center>
<img src="https://picx.zhimg.com/80/v2-31a01f1253dfc8c42e23e05b1869a932_1440w.png" style="width: 80%;"/>
</div>



进入 openmcp 后，我们来试着询问它一些问题，记得要循序渐进，比如不要直接询问复杂的查询操作，通过【列出所有节点类型】先让 agent 知道有哪些节点，通过：

<div align=center>
<img src="https://picx.zhimg.com/80/v2-5e8cb3986d01891718b5be3df73a0a61_1440w.png" style="width: 80%;"/>
</div>

直接询问【最新的5个评论】不行，先通过【罗列随便5个评论】让大模型知道【评论数据】的字段有哪些。摸索完成边界后，你就可以将这些你探索的流程写入 system prompt 中了，点击下图的红色箭头指向的按钮来打开【系统提示词】，然后管理你的 system prompt：

<div align=center>
<img src="https://pica.zhimg.com/80/v2-f4c8ae4f465062a37c2fefdd0bc28910_1440w.png" style="width: 100%;"/>
</div>