

<p align="center">
  <img src="./openmcp.png" alt="MCP Logo" width="200">
</p>

<h1 align="center">OpenMCP Tutorial</h1>

<div style="text-align: center;">

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green)](https://modelcontextprotocol.io)
![GitHub](https://img.shields.io/github/license/LSTM-Kirigaya/openmcp-tutorial)
</div>

<p align="center">
  A comprehensive collection of Model Context Protocol (MCP) server examples in multiple languages
</p>

## 📋 Table of Contents

- [Overview](#overview)
- [What is MCP?](#what-is-mcp)
- [Projects](#projects)
  - [Python Examples](#python-examples)
  - [TypeScript Examples](#typescript-examples)
  - [Go Examples](#go-examples)
- [Getting Started](#getting-started)
- [How to Build MCP Servers in Different Languages](#how-to-build-mcp-servers-in-different-languages)
- [Contributing](#contributing)
- [License](#license)

## Overview

This repository contains a collection of example implementations of Model Context Protocol (MCP) servers in various programming languages. These examples demonstrate how to build MCP servers that can provide different capabilities to AI applications, such as web browsing, database access, file operations, and more.

Whether you're new to MCP or looking to extend your AI applications with contextual data, these examples will help you get started quickly.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that allows AI systems to securely connect to external data sources and tools through a standardized interface. 

Key benefits of MCP:
- 🔒 **Secure**: Provides a secure way for AI models to access external resources
- 🌐 **Standardized**: Unified protocol for connecting to various data sources and tools
- ⚡ **Efficient**: Eliminates the need for custom integrations for each data source
- 🛠️ **Extensible**: Easy to build custom servers for specific use cases

MCP enables AI applications to:
- Access local files and databases
- Interact with web services and APIs
- Execute tools and commands
- Retrieve real-time information

## Projects

### Python Examples

| Project | Description |
|---------|-------------|
| [simple-mcp](./simple-mcp) | A minimal example of an MCP server in Python using the `mcp` package |
| [bing-images](./bing-images) | An MCP server that searches for images using the Bing Images API |
| [crawl4ai-mcp](./crawl4ai-mcp) | An MCP server using Crawl4AI for web crawling and data extraction |
| [qq-group-summary](./qq-group-summary) | An MCP server that summarizes QQ group conversations |

### TypeScript Examples

| Project | Description |
|---------|-------------|
| [my-browser](./my-browser) | An MCP server that provides browser automation capabilities using Puppeteer |
| [smithery-my-browser](./smithery-my-browser) | Another browser automation MCP server using Smithery framework |

### Go Examples

| Project | Description |
|---------|-------------|
| [neo4j-go-server](./neo4j-go-server) | An MCP server that provides read-only access to Neo4j graph databases |

## Getting Started

### Prerequisites

- Python 3.x (for Python examples)
- Node.js (for TypeScript examples)
- Go (for Go examples)
- [uv](https://docs.astral.sh/uv/) (recommended for Python projects)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LSTM-Kirigaya/openmcp-tutorial.git
cd openmcp-tutorial
```

2. Navigate to any project directory and follow the specific instructions in that project's README.

## How to Build MCP Servers in Different Languages

### Python

```bash
cd ~/project/your-mcp-project
uv init
uv add mcp "mcp[cli]"
```

### TypeScript

```bash
# Navigate to your project directory
cd my-browser  # or any TypeScript MCP project

# Install dependencies
npm install

# Build the project
npm run build
```

### Go

```bash
# Navigate to your project directory
cd neo4j-go-server

# Get dependencies
go mod tidy

# Run the project
go run main.go
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve these examples or add new ones.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by the OpenMCP community
</p>

[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/lstm-kirigaya-openmcp-tutorial-badge.png)](https://mseep.ai/app/lstm-kirigaya-openmcp-tutorial)
