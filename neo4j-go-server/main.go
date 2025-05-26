package main

import (
	"context"
	"fmt"
	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"neo4j-go-server/util"
)

var (
	neo4jPath string = "./neo4j.json"
	addr string = "localhost:8083"
)

func main() {
	_, err := util.CreateNeo4jDriver(neo4jPath)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Neo4j driver created successfully")

	// server.NewMCPServer(
	// 	"只读 Neo4j 服务器",
	// 	"0.0.1",
	// 	server.WithToolCapabilities(true),
	// 	server.WithHTTPContextFunc()
	// )

	s := server.NewMCPServer(
		"只读 Neo4j 服务器",
		"0.0.1",
		server.WithToolCapabilities(true),
	)

	srv := server.NewSSEServer(s)

	// 定义 schema
	executeReadOnlyCypherQuery := mcp.NewTool("executeReadOnlyCypherQuery",
		mcp.WithDescription("执行只读的 Cypher 查询"),
		mcp.WithString("cypher",
			mcp.Required(),
			mcp.Description("Cypher 查询语句，必须是只读的"),
		),
	)

	getAllNodeTypes := mcp.NewTool("getAllNodeTypes",
		mcp.WithDescription("获取所有的节点类型"),
	)

	getAllRelationTypes := mcp.NewTool("getAllRelationTypes",
		mcp.WithDescription("获取所有的关系类型"),
	)

	getNodeField := mcp.NewTool("getNodeField",
		mcp.WithDescription("获取节点的字段"),
		mcp.WithString("nodeLabel",
			mcp.Required(),
			mcp.Description("节点的标签"),
		),
	)

	// 注册对应的工具到 schema 上
	s.AddTool(executeReadOnlyCypherQuery, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		cypher := request.Params.Arguments["cypher"].(string)
		result, err := util.ExecuteReadOnlyCypherQuery(cypher)

		fmt.Println(result)

		if err != nil {
			return mcp.NewToolResultText(""), err
		}

		return mcp.NewToolResultText(fmt.Sprintf("%v", result)), nil
	})


	s.AddTool(getAllNodeTypes, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		result, err := util.GetAllNodeTypes()

		fmt.Println(result)
		
		if err != nil {
			return mcp.NewToolResultText(""), err
		}
		
		return mcp.NewToolResultText(fmt.Sprintf("%v", result)), nil
	})

	s.AddTool(getAllRelationTypes, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		result, err := util.GetAllRelationshipTypes()
		fmt.Println(result)

		if err!= nil {
			return mcp.NewToolResultText(""), err
		}

		return mcp.NewToolResultText(fmt.Sprintf("%v", result)), nil
	})

	s.AddTool(getNodeField, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		nodeLabel := request.Params.Arguments["nodeLabel"].(string)
		result, err := util.GetNodeFields(nodeLabel)
		
		fmt.Println(result)
		
		if err!= nil {
			return mcp.NewToolResultText(""), err
		}
		
		return mcp.NewToolResultText(fmt.Sprintf("%v", result)), nil
	})


	fmt.Printf("Server started at http://%s/sse\n", addr)
	srv.Start(addr)
}
