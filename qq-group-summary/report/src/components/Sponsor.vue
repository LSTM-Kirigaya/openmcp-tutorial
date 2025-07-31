<template>
	<section class="sponsor-section">
		<div class="section-title">❤️ How to Sponsor</div>
		<div class="sponsor-content">
			<p>If you like openmcp, please support our work!</p>

			<a class="sponsor-item" href="https://github.com/LSTM-Kirigaya/openmcp-client" target="_blank">
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle;">
					<path fill-rule="evenodd" clip-rule="evenodd"
						d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z">
					</path>
				</svg>
				Github
			</a>
			<br>
			<a class="sponsor-item" href="https://afdian.com/a/kirigaya" target="_blank">
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path
						d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.34-.87-2.57-2.49-2.97V5H10.9v1.69c-1.51.32-2.72 1.3-2.72 2.81 0 1.79 1.49 2.69 3.66 3.21 1.95.46 2.34 1.15 2.34 1.87 0 .53-.39 1.39-2.1 1.39-1.6 0-2.23-.72-2.32-1.64H8.04c.1 1.7 1.36 2.66 2.86 2.97V19h2.34v-1.67c1.52-.29 2.72-1.16 2.73-2.77-.01-2.2-1.9-2.96-3.66-3.42z">
					</path>
				</svg>
				爱发电</a>
		</div>
	</section>
</template>

<style>
.sponsor-section {
	margin-bottom: 20px;
	padding-bottom: 16px;
}

.sponsor-content {
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.sponsor-item {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 1rem;
	background-color: #B988D1;
	color: var(--vscode-button-foreground);
	border-radius: 4px;
	text-decoration: none;
	transition: transform 0.1s ease;
}

.sponsor-item:hover {
	background-color: #8e5bbf;
	transition: transform 0.1s ease;
}

.sponsor-item:active {
	transform: scale(0.95);
	transition: transform 0.1s ease;
}
</style>