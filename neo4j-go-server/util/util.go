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