<script setup lang="ts">
</script>

<template>
	<section class="troubleshoot-section">
		<div class="section-title">🔧 Troubleshooting</div>
		<ul class="troubleshoot-list">
			<li>
				If the interface displays abnormally, try restarting VSCode or report an <a href="https://github.com/LSTM-Kirigaya/openmcp-client/issues" target="_blank">Issue</a>.
			</li>
			<li>
				For more questions, refer to the <a href="https://openmcp.kirigaya.cn/" target="_blank">official
					documentation</a> or join the community.</li>

			<li>Contant Jinhui via <a href="mailto:1193466151@qq.com">1193466151@qq.com</a> to seek technical consultation or business cooperation.</li>
		</ul>
	</section>
</template>

<style>
.troubleshoot-section {
	margin-bottom: 20px;
	padding-bottom: 16px;
}

.troubleshoot-list {
	list-style: disc inside;
	padding-left: 18px;
	color: var(--foreground, #444);
}

.troubleshoot-list li {
	margin-bottom: 0.75rem;
}

.troubleshoot-list a {
	color: #B988D1;
	text-decoration: underline;
}

.troubleshoot-list a:hover {
	color: #8e5bbf;
}
</style>