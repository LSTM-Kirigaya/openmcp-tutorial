#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
	CallToolRequestSchema,
	ListResourcesRequestSchema,
	ListToolsRequestSchema,
	ReadResourceRequestSchema,
	CallToolResult,
	TextContent,
	ImageContent,
	Tool,
} from "@modelcontextprotocol/sdk/types.js";
import puppeteer, { Browser, Page } from "puppeteer";

// Define the tools once to avoid repetition
export const TOOLS: Tool[] = [
	{
		name: "k_navigate",
		description: "Navigate to a URL",
		inputSchema: {
			type: "object",
			properties: {
				url: { type: "string", description: "URL to navigate to" },
				launchOptions: { type: "object", description: "PuppeteerJS LaunchOptions. Default null. If changed and not null, browser restarts. Example: { headless: true, args: ['--no-sandbox'] }" },
				allowDangerous: { type: "boolean", description: "Allow dangerous LaunchOptions that reduce security. When false, dangerous args like --no-sandbox will throw errors. Default false." },
			},
			required: ["url"],
		},
	},
	{
		name: "k_screenshot",
		description: "Take a screenshot of the current page or a specific element",
		inputSchema: {
			type: "object",
			properties: {
				name: { type: "string", description: "Name for the screenshot" },
				selector: { type: "string", description: "CSS selector for element to screenshot" },
				width: { type: "number", description: "Width in pixels (default: 800)" },
				height: { type: "number", description: "Height in pixels (default: 600)" },
			},
			required: ["name"],
		},
	},
	{
		name: "k_click",
		description: "Click an element on the page",
		inputSchema: {
			type: "object",
			properties: {
				selector: { type: "string", description: "CSS selector for element to click" },
			},
			required: ["selector"],
		},
	},
	{
		name: "k_fill",
		description: "Fill out an input field",
		inputSchema: {
			type: "object",
			properties: {
				selector: { type: "string", description: "CSS selector for input field" },
				value: { type: "string", description: "Value to fill" },
			},
			required: ["selector", "value"],
		},
	},
	{
		name: "k_select",
		description: "Select an element on the page with Select tag",
		inputSchema: {
			type: "object",
			properties: {
				selector: { type: "string", description: "CSS selector for element to select" },
				value: { type: "string", description: "Value to select" },
			},
			required: ["selector", "value"],
		},
	},
	{
		name: "k_hover",
		description: "Hover an element on the page",
		inputSchema: {
			type: "object",
			properties: {
				selector: { type: "string", description: "CSS selector for element to hover" },
			},
			required: ["selector"],
		},
	},
	{
		name: "k_evaluate",
		description: "Execute JavaScript in the browser console",
		inputSchema: {
			type: "object",
			properties: {
				script: { type: "string", description: "JavaScript code to execute" },
			},
			required: ["script"],
		},
	},
	{
		name: "k_get_full_page_text",
		description: "获取页面所有文本内容",
		inputSchema: {
			type: "object",
			properties: {},
		},
	},
];

// Global state
let browser: Browser | null;
let page: Page | null;
const consoleLogs: string[] = [];
const screenshots = new Map<string, string>();
let previousLaunchOptions: any = null;

async function ensureBrowser(args: any = {}) {
	let {
		launchOptions = {},
		allowDangerous = true
	} = args;

	const DANGEROUS_ARGS = [
		'--no-sandbox',
		'--disable-setuid-sandbox',
		'--single-process',
		'--disable-web-security',
		'--ignore-certificate-errors',
		'--disable-features=IsolateOrigins',
		'--disable-site-isolation-trials',
		'--allow-running-insecure-content'
	];

	// Parse environment config safely
	let envConfig = {};
	try {
		envConfig = JSON.parse(process.env.PUPPETEER_LAUNCH_OPTIONS || '{}');
	} catch (error: any) {
		console.warn('Failed to parse PUPPETEER_LAUNCH_OPTIONS:', error?.message || error);
	}

	launchOptions = launchOptions || { headless: true };
	if (launchOptions.headless === undefined) {
		launchOptions.headless = true;
	}

	// Deep merge environment config with user-provided options
	const mergedConfig = deepMerge(envConfig, launchOptions || {});

	// Security validation for merged config
	if (mergedConfig?.args) {
		const dangerousArgs = mergedConfig.args?.filter?.((arg: string) => DANGEROUS_ARGS.some((dangerousArg: string) => arg.startsWith(dangerousArg)));
		if (dangerousArgs?.length > 0 && !(allowDangerous || (process.env.ALLOW_DANGEROUS === 'true'))) {
			throw new Error(`Dangerous browser arguments detected: ${dangerousArgs.join(', ')}. Fround from environment variable and tool call argument. ` +
				'Set allowDangerous: true in the tool call arguments to override.');
		}
	}

	try {
		if ((browser && !browser.connected) ||
			(launchOptions && (JSON.stringify(launchOptions) != JSON.stringify(previousLaunchOptions)))) {
			await browser?.close();
			browser = null;
		}
	}
	catch (error) {
		browser = null;
	}

	previousLaunchOptions = launchOptions;

	return page!;
}

// Deep merge utility function
function deepMerge(target: any, source: any): any {
	const output = Object.assign({}, target);
	if (typeof target !== 'object' || typeof source !== 'object') return source;

	for (const key of Object.keys(source)) {
		const targetVal = target[key];
		const sourceVal = source[key];
		if (Array.isArray(targetVal) && Array.isArray(sourceVal)) {
			// Deduplicate args/ignoreDefaultArgs, prefer source values
			output[key] = [...new Set([
				...(key === 'args' || key === 'ignoreDefaultArgs' ?
					targetVal.filter((arg: string) => !sourceVal.some((launchArg: string) => arg.startsWith('--') && launchArg.startsWith(arg.split('=')[0]))) :
					targetVal),
				...sourceVal
			])];
		} else if (sourceVal instanceof Object && key in target) {
			output[key] = deepMerge(targetVal, sourceVal);
		} else {
			output[key] = sourceVal;
		}
	}
	return output;
}

declare global {
	interface Window {
		mcpHelper: {
			logs: string[],
			originalConsole: Partial<typeof console>,
		}
	}
}

export async function handleToolCall(name: string, args: any): Promise<CallToolResult> {
	const page = await ensureBrowser(args);

	switch (name) {
		case "k_navigate":
			await page.goto(args.url, {
				waitUntil: 'networkidle2',
				timeout: 0
			});
			return {
				content: [{
					type: "text",
					text: `Navigated to ${args.url}`,
				}],
				isError: false,
			};

		case "k_screenshot": {
			const width = args.width ?? 800;
			const height = args.height ?? 600;
			await page.setViewport({ width, height });

			const screenshot = await (args.selector ?
				(await page.$(args.selector))?.screenshot({ encoding: "base64" }) :
				page.screenshot({ encoding: "base64", fullPage: false }));

			if (!screenshot) {
				return {
					content: [{
						type: "text",
						text: args.selector ? `Element not found: ${args.selector}` : "Screenshot failed",
					}],
					isError: true,
				};
			}

			screenshots.set(args.name, screenshot as string);

			return {
				content: [
					{
						type: "text",
						text: `Screenshot '${args.name}' taken at ${width}x${height}`,
					} as TextContent,
					{
						type: "image",
						data: screenshot,
						mimeType: "image/png",
					} as ImageContent,
				],
				isError: false,
			};
		}

		case "k_click":
			try {
				await page.click(args.selector);
				return {
					content: [{
						type: "text",
						text: `Clicked: ${args.selector}`,
					}],
					isError: false,
				};
			} catch (error) {
				return {
					content: [{
						type: "text",
						text: `Failed to click ${args.selector}: ${(error as Error).message}`,
					}],
					isError: true,
				};
			}

		case "k_fill":
			try {
				await page.waitForSelector(args.selector);
				await page.type(args.selector, args.value);
				return {
					content: [{
						type: "text",
						text: `Filled ${args.selector} with: ${args.value}`,
					}],
					isError: false,
				};
			} catch (error) {
				return {
					content: [{
						type: "text",
						text: `Failed to fill ${args.selector}: ${(error as Error).message}`,
					}],
					isError: true,
				};
			}

		case "k_select":
			try {
				await page.waitForSelector(args.selector);
				await page.select(args.selector, args.value);
				return {
					content: [{
						type: "text",
						text: `Selected ${args.selector} with: ${args.value}`,
					}],
					isError: false,
				};
			} catch (error) {
				return {
					content: [{
						type: "text",
						text: `Failed to select ${args.selector}: ${(error as Error).message}`,
					}],
					isError: true,
				};
			}

		case "k_hover":
			try {
				await page.waitForSelector(args.selector);
				await page.hover(args.selector);
				return {
					content: [{
						type: "text",
						text: `Hovered ${args.selector}`,
					}],
					isError: false,
				};
			} catch (error) {
				return {
					content: [{
						type: "text",
						text: `Failed to hover ${args.selector}: ${(error as Error).message}`,
					}],
					isError: true,
				};
			}

		case "k_evaluate":
			try {
				await page.evaluate(() => {
					window.mcpHelper = {
						logs: [],
						originalConsole: { ...console },
					};

					['log', 'info', 'warn', 'error'].forEach(method => {
						(console as any)[method] = (...args: any[]) => {
							window.mcpHelper.logs.push(`[${method}] ${args.join(' ')}`);
							(window.mcpHelper.originalConsole as any)[method](...args);
						};
					});
				});

				const result = await page.evaluate(args.script);

				const logs = await page.evaluate(() => {
					Object.assign(console, window.mcpHelper.originalConsole);
					const logs = window.mcpHelper.logs;
					delete (window as any).mcpHelper;
					return logs;
				});

				return {
					content: [
						{
							type: "text",
							text: `Execution result:\n${JSON.stringify(result, null, 2)}\n\nConsole output:\n${logs.join('\n')}`,
						},
					],
					isError: false,
				};
			} catch (error) {
				return {
					content: [{
						type: "text",
						text: `Script execution failed: ${(error as Error).message}`,
					}],
					isError: true,
				};
			}
		
		case "k_get_full_page_text":
			try {
				await page.evaluate(() => {
					window.mcpHelper = {
						logs: [],
						originalConsole: { ...console },
					};

					['log', 'info', 'warn', 'error'].forEach(method => {
						(console as any)[method] = (...args: any[]) => {
							window.mcpHelper.logs.push(`[${method}] ${args.join(' ')}`);
							(window.mcpHelper.originalConsole as any)[method](...args);
						};
					});
				});
				
				const result = await page.evaluate('document.body.innerText');

				const logs = await page.evaluate(() => {
					Object.assign(console, window.mcpHelper.originalConsole);
					const logs = window.mcpHelper.logs;
					delete (window as any).mcpHelper;
					return logs;
				});

				return {
					content: [
						{
							type: "text",
							text: `Execution result:\n${JSON.stringify(result, null, 2)}\n\nConsole output:\n${logs.join('\n')}`,
						},
					],
					isError: false,
				};
			} catch (error) {
				return {
					content: [{
						type: "text",
						text: `Failed to get full page text: ${(error as Error).message}`,
					}],
					isError: true,
				};
			}

		default:
			return {
				content: [{
					type: "text",
					text: `Unknown tool: ${name}`,
				}],
				isError: true,
			};
	}
}