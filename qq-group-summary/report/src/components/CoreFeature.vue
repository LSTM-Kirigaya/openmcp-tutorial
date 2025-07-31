<template>
    <section class="core-section">
        <div class="section-title">✨ Core Features</div>
        <ul class="core-list">
            <li class="core-card">
                <span class="core-dot">🧩</span>
                <span>Full support for all MCP protocols, including <b>stdio</b>, <b>SSE</b>, and <b>streamable HTTP</b> connection modes.</span>
				<a href="https://openmcp.kirigaya.cn/plugin-tutorial/usage/debug.html" target="_blank">Learn more</a>
            </li>
            <li class="core-card">
                <span class="core-dot">🧩</span>
                <span>Connect Multiple MCP Servers and combine more mcp tools in just one instance.</span>
				<a href="https://openmcp.kirigaya.cn/plugin-tutorial/usage/multi-server.html" target="_blank">Learn more</a>
            </li>
            <li class="core-card">
                <span class="core-dot">🧩</span>
                <span>One-click AI Mock data generation & Automatic mcp tool testing width custom and flexible order.</span>
				<a href="https://openmcp.kirigaya.cn/sdk-tutorial/" target="_blank">Learn more</a>
            </li>
			<li class="core-card">
                <span class="core-dot">🧩</span>
                <span>Support function calling based on both <strong>XML</strong> and <strong>openai tools protocols.</strong></span>
				<a href="https://openmcp.kirigaya.cn/sdk-tutorial/" target="_blank">Learn more</a>
            </li>
            <li class="core-card">
                <span class="core-dot">🧩</span>
                <span>Export connection as mcpconfig.json and deploy in openmcp-sdk</span>
				<a href="https://openmcp.kirigaya.cn/sdk-tutorial/" target="_blank">Learn more</a>
            </li>
            <li class="core-card">
                <span class="core-dot">🧩</span>
                <span>Native VSCode experience, cross-platform support</span>
				<a href="https://openmcp.kirigaya.cn/plugin-tutorial/quick-start/acquire-openmcp.html" target="_blank">Learn more</a>
            </li>
        </ul>
    </section>
</template>

<style scoped>
.core-section {
    margin-bottom: 20px;
}

.core-list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    list-style: none;
    padding: 0;
    margin: 0;
}

@media (max-width: 950px) {
    .core-list {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 630px) {
    .core-list {
        grid-template-columns: 1fr;
    }
}

.core-card {
    display: flex;
    align-items: flex-start;
	flex-direction: column;
    gap: 12px;
    padding: 1.5rem;
    border-radius: 10px;
    background-color: var(--vscode-sideBar-background);
    transition: transform 0.2s ease, box-shadow 0.2s;
    box-shadow: 0 2px 8px var(--vscode-widget-shadow, rgba(0,0,0,0.08));
    font-size: 1.05em;
}

.core-card a {
	color: #B988D1;
}

.core-card:hover {
    transform: translateY(-4px) scale(1.025);
    box-shadow: 0 6px 18px var(--vscode-widget-shadow, rgba(0,0,0,0.14));
}

.core-dot {
    display: inline-block;
    border-radius: 50%;
	font-size: 30px;
    flex-shrink: 0;
}
</style>