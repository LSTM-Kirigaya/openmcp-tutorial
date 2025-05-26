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

// 获取所有的节点类型
func GetAllNodeTypes() ([]string, error) {
	cypher := "MATCH (n) RETURN DISTINCT labels(n) AS labels"
	result, err := ExecuteReadOnlyCypherQuery(cypher)
	if err!= nil {
		return nil, err
	}
	var nodeTypes []string
	for _, record := range result {
		labels := record["labels"].([]any)
		for _, label := range labels {
			nodeTypes = append(nodeTypes, label.(string))
		}
	}
	return nodeTypes, nil
}

// 获取所有的关系类型
func GetAllRelationshipTypes() ([]string, error) {
	cypher := "MATCH ()-[r]->() RETURN DISTINCT type(r) AS relationshipType"
	result, err := ExecuteReadOnlyCypherQuery(cypher)
	if err!= nil {
		return nil, err
	}
	var relationshipTypes []string
	for _, record := range result {
		relationshipTypes = append(relationshipTypes, record["relationshipType"].(string))
	}
	return relationshipTypes, nil
}

// 获取一个节点的字段示范
func GetNodeFields(nodeType string) ([]string, error) {
	cypher := fmt.Sprintf("MATCH (n:%s) RETURN keys(n) AS keys LIMIT 1", nodeType)
	result, err := ExecuteReadOnlyCypherQuery(cypher)
	if err!= nil {
		return nil, err
	}
	var fields []string
	for _, record := range result {
		keys := record["keys"].([]any)
		for _, key := range keys {
			fields = append(fields, key.(string))
		}
	}
	return fields, nil
}