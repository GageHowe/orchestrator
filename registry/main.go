package main

import (
	"fmt"
	"log"
	"os"

	"github.com/BurntSushi/toml"
)

func main() {

	authenticate_agents()
	// e := echo.New()
	// e.Use(middleware.RequestLogger())

	// e.GET("/", func(c *echo.Context) error {
	// 	return c.String(200, "server is up")
	// })

	// // orchestrator requests authentication
	// e.GET("/auth", func(c *echo.Context) error {

	// 	// agent := c.QueryParam("agent")

	// 	return c.String(200, "todo")
	// })

	// if err := e.Start(":1323"); err != nil {
	// 	e.Logger.Error("failed to start server", "error", err)
	// }
}

// defines an agent TOML config file, e.g. agent1.toml
type AgentConfig struct {
	Name        string
	Host        string
	Port        int
	Description string
}

func (c AgentConfig) String() string {
	return fmt.Sprintf("Name: %s\nHost: %s\nPort: %d\nDescription: %s", c.Name, c.Host, c.Port, c.Description)
}

func authenticate_agents() {
	entries, err := os.ReadDir("./config/agents/")
	if err != nil {
		log.Fatal(err)
	}
	// agents := []string()

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}

		fmt.Println("File found: %s", entry.Name())
		var conf AgentConfig
		_, err = toml.DecodeFile("./config/agents/"+entry.Name(), &conf)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println("Config file read successfully:\n" + conf.String())

	}
}
