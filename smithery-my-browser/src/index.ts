import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { handleToolCall, TOOLS } from "./browser";

// Optional: Define configuration schema to require configuration at connection time
export const configSchema = z.object({
	debug: z.boolean().default(false).describe("Enable debug logging"),
});

export default function createStatelessServer({
	config,
}: {
	config: z.infer<typeof configSchema>;
}) {
	const server = new McpServer({
		name: "Browser MCP",
		version: "1.0.0",
	});

	// Add a tool
	server.tool(
		"hello",
		"Say hello to someone",
		{
			name: z.string().describe("Name to greet"),
		},
		async ({ name }) => {
			return {
				content: [{ type: "text", text: `Hello, ${name}!` }],
			};
		}
	);


	// Register all browser tools
	TOOLS.forEach(tool => {
		server.tool(
			tool.name,
			tool.description || '',
			tool.inputSchema,
			async (args: any) => {
				return handleToolCall(tool.name, args);
			}
		);
	});

	return server.server;
}
