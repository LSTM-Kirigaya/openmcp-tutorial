<script setup lang="ts">
import OmIcon from './OmIcon.vue';
const date = new Date();

</script>

<template>
	<header class="openmcp-header">
		<OmIcon />
		<div>
			<h1>
				📦 OpenMCP 群聊总结 {{ date.getFullYear() }}.{{ date.getMonth() + 1 }}.{{ date.getDate() }}
			</h1>
			<div class="links">
				<a href="https://github.com/LSTM-Kirigaya/openmcp-client" target="_blank" title="GitHub">
					<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"
						style="vertical-align: middle;">
						<path fill-rule="evenodd" clip-rule="evenodd"
							d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z">
						</path>
					</svg>
					GitHub
				</a>
				<a href="https://github.com/LSTM-Kirigaya/openmcp-client/releases" target="_blank" title="Releases">
					<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"
						style="vertical-align: middle;">
						<path
							d="M21 10.975V8a2 2 0 00-2-2h-6V4.688c.305-.274.5-.668.5-1.11a1.5 1.5 0 00-3 0c0 .442.195.836.5 1.11V6H5a2 2 0 00-2 2v2.998l-.072.005A.999.999 0 002 12v2a1 1 0 001 1v5a2 2 0 002 2h14a2 2 0 002-2v-5a1 1 0 001-1v-1.975a1 1 0 00-.928-.997L21 10.975zm-5 5.025H8v-3h8v3z">
						</path>
					</svg>
					Releases
				</a>
				<a href="https://openmcp.kirigaya.cn/" target="_blank" title="Website">
					<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"
						style="vertical-align: middle;">
						<path
							d="M12.001 1.993C6.486 1.994 2 6.48 2 11.994c0 5.514 4.486 9.999 10 10 5.515 0 10.001-4.485 10.001-10s-4.486-10-10-10.001zM12 19.994c-4.412 0-8.001-3.589-8.001-8s3.589-8 8-8.001C16.411 3.994 20 7.583 20 11.994c0 4.41-3.589 8-8 8z">
						</path>
						<path
							d="M12.001 8.994l-4.005 4.005 1.414 1.414 2.591-2.591 2.591 2.591 1.414-1.414-4.005-4.005z">
						</path>
					</svg>
					Website
				</a>
				<a href="https://discord.com/invite/SKTZRf6NzU" target="_blank" title="Discord">
					<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"
						style="vertical-align: middle;">
						<path
							d="M19.27 5.33C17.94 4.71 16.5 4.26 15 4a.09.09 0 00-.07.03c-.18.33-.39.76-.53 1.09a16.09 16.09 0 00-4.8 0c-.14-.34-.35-.76-.54-1.09-.01-.02-.04-.03-.07-.03-1.5.26-2.93.71-4.27 1.33-.01 0-.02.01-.03.02-2.72 4.07-3.47 8.03-3.1 11.95 0 .02.01.04.03.05 1.8 1.32 3.53 2.12 5.24 2.65.03.01.06 0 .07-.02.4-.55.76-1.13 1.07-1.74.02-.04 0-.08-.04-.09-.57-.22-1.11-.48-1.64-.78-.04-.02-.04-.08-.01-.11.11-.08.22-.17.33-.25.02-.02.05-.02.07-.01 3.44 1.57 7.15 1.57 10.55 0 .02-.01.05-.01.07.01.11.09.22.17.33.26.04.03.04.09-.01.11-.52.31-1.07.56-1.64.78-.04.01-.05.06-.04.09.32.61.68 1.19 1.07 1.74.03.01.06.02.09.01 1.72-.53 3.45-1.33 5.25-2.65.02-.01.03-.03.03-.05.44-4.53-.73-8.46-3.1-11.95-.01-.01-.02-.02-.04-.02zM8.52 14.91c-.99 0-1.8-.9-1.8-2s.79-2.01 1.8-2.01c1 0 1.81.9 1.81 2.01-.01 1.1-.8 2-1.81 2zm6.96 0c-.99 0-1.8-.9-1.8-2s.79-2.01 1.8-2.01c1 0 1.81.9 1.81 2.01-.01 1.1-.8 2-1.81 2z">
						</path>
					</svg>
					Discord
				</a>
				<a href="https://qm.qq.com/cgi-bin/qm/qr?k=C6ZUTZvfqWoI12lWe7L93cWa1hUsuVT0&jump_from=webapi&authKey=McW6B1ogTPjPDrCyGttS890tMZGQ1KB3QLuG4aqVNRaYp4vlTSgf2c6dMcNjMuBD"
					target="_blank" title="QQ Group">
					<svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor">
						<path d="M824.8 613.2c-16-51.4-34.4-94.6-62.7-165.3C766.5 262.2 689.3 112 511.5 112 331.7 112 256.2 265.2 261 447.9c-28.4 70.8-46.7 113.7-62.7 165.3-34 109.5-23 154.8-14.6 155.8 18 2.2 70.1-82.4 70.1-82.4 0 49 25.2 112.9 79.8 159-26.4 8.1-85.7 29.9-71.6 53.8 11.4 19.3 196.2 12.3 249.5 6.3 53.3 6 238.1 13 249.5-6.3 14.1-23.8-45.3-45.7-71.6-53.8 54.6-46.2 79.8-110.1 79.8-159 0 0 52.1 84.6 70.1 82.4 8.5-1.1 19.5-46.4-14.5-155.8z"></path>
					</svg>
					QQ Group
				</a>
			</div>
		</div>
	</header>

	<hr>
</template>

<style>
.openmcp-logo {
  display: inline-block;
  width: 84px;
  height: 84px;
  border-radius: 16px;
  vertical-align: middle;
}

hr {
    border: none;
    border-top: 1.5px solid #B988D1;
    height: 0;
    margin: 24px 0;
}

.openmcp-header h1 {
	font-size: 2.1rem;
	font-weight: bold;
	margin: 0 0 20px 0;
	display: flex;
	justify-content: center;
	color: #B988D1;
	line-height: 1.2;
}

.openmcp-header .links {
	display: flex;
	flex-wrap: wrap;
	gap: 16px;
	justify-content: center;
	margin-top: 4px;
}

.openmcp-header .links a {
	color: var(--vscode-textLink-foreground);
	font-weight: 500;
	text-decoration: none;
	display: flex;
    align-items: center;
    gap: 0.5rem;
	transition: color 0.18s;
}

.openmcp-header .links a:hover {
	color: #8e5bbf;
	text-decoration: underline;
}
</style>