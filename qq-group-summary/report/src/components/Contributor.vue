<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import VanillaTilt from 'vanilla-tilt';

const props = defineProps<{
	contributors: {
		username: string;
		avatarUrl: string;
		homeUrl: string;
	}[];
}>();

const tiltElements = reactive<any[]>([]);

onMounted(() => {
    // 为每个元素应用Tilt效果
    tiltElements.forEach(el => {
        VanillaTilt.init(el, {
            max: 35,
            speed: 400,
            glare: true, 
            'max-glare': 0.2
        });
    });
});
</script>

<template>
	<section class="troubleshoot-section">
		<div class="section-title">👥 Contributors</div>
		<div class="contributors-grid">
			<div v-for="(contributor, idx) in props.contributors"
				:key="contributor.username" class="contributor-tilt" 
				:ref="el => tiltElements[idx] = el"
			>
				<a :href="contributor.homeUrl" target="_blank">
					<img :src="contributor.avatarUrl" :alt="contributor.username" class="contributor-avatar" />
					<span class="contributor-name">{{ contributor.username }}</span>
				</a>
			</div>
		</div>
	</section>
</template>


<style>
.contributors-container {
	max-width: 800px;
	margin: 0 auto;
	padding: 2rem;
	text-align: center;
}

.contributors-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
	gap: 1.5rem;
	margin-top: 2rem;
}

.contributor-tilt {
	background: rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	padding: 1rem;
	transition: transform 0.2s;
}

.contributor-tilt a {
	text-decoration: none;
	color: inherit;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.contributor-avatar {
	width: 80px;
	height: 80px;
	border-radius: 50%;
	object-fit: cover;
	display: block;
	margin: 0 auto 0.5rem;
	border: 3px solid #fff;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.contributor-name {
	display: block;
	font-weight: 500;
	color: #B988D1;
	text-decoration: none;
}

/* Tilt.js 生成的眩光效果自定义 */
.tilt-glare {
	border-radius: 12px !important;
}
</style>