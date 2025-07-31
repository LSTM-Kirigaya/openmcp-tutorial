<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
    version: {
        type: String,
        default: '0.1.9'
    },
    changelogs: {
        type: Array as () => string[],
        default: () => [
            'Brand new VSCode WebView adaptation, smoother experience https://example.com/image1.png',
            'Support for AI Mock, toolchain visualization https://example.com/diagram.jpg and automatic topology detection',
            'Multi-model concurrency, enhanced plugin capabilities https://example.com/arch.svg'
        ]
    }
});

// 处理变更日志，提取文本和图片
const processedChangelogs = computed(() => {
    return props.changelogs.map(log => {
        // 提取所有https图片链接
        const imageRegex = /(https:\/\/[^\s]+?\.(?:png|jpg|jpeg|gif|svg|webp))/gi;
        const images = [];
        let match;

        // 从文本中提取所有匹配的图片URL
        while ((match = imageRegex.exec(log)) !== null) {
            images.push(match[1]);
        }

        // 从原始文本中移除图片URL
        const text = log.replace(imageRegex, '').replace(/\s{2,}/g, ' ').trim();

        return { text, images };
    });
});
</script>

<template>
    <section class="news-section">
        <div class="news-title">
            <span>📣 What's New in <span class="highlight">{{ props.version }}</span></span>
        </div>
        <div class="news-content">
            <ul class="news-list">
                <li v-for="(item, index) in processedChangelogs" :key="index">
                    <span class="news-badge">{{ '/' }}</span>
                    <div class="log-content">
                        <span>{{ item.text }}</span>
                        <div v-if="item.images.length" class="image-container">
                            <a v-for="(img, imgIndex) in item.images" :key="imgIndex" :href="img" target="_blank"
                                rel="noopener">
                                <img :src="img" alt="Changelog image" class="changelog-image" />
                            </a>
                        </div>
                    </div>
                </li>
            </ul>
            <br>
            <a class="release-link" href="https://openmcp.kirigaya.cn/preview/changelog.html" target="_blank"
                rel="noopener">View History Changelog →</a>
        </div>
    </section>
</template>

<style>
.news-section {
    margin-bottom: 20px;
}

.news-title {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: #B988D1;
    margin-bottom: 10px;
}

.news-title .logo {
    width: 38px;
    height: 38px;
    margin-right: 12px;
    vertical-align: middle;
}

.news-title .highlight {
    color: #B988D1;
}

.news-content {
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
    background-color: var(--vscode-sideBar-background);
    box-shadow: 0 2px 8px var(--vscode-widget-shadow);
}

.news-content li {
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-start;
}

.news-badge {
    display: inline-block;
    margin-right: 10px;
    color: #B988D1;
    font-weight: bold;
}

.log-content {
    flex: 1;
}

.image-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
}

.changelog-image {
    max-width: 100%;
    max-height: 350px;
    border-radius: 6px;
    border: 1px solid var(--vscode-widget-border);
    object-fit: contain;
    background-color: var(--vscode-editor-background);
    padding: 4px;
    box-sizing: border-box;
    transition: transform 0.2s ease;
}


.release-link {
    color: #B988D1;
    text-decoration: none;
    font-weight: 500;
    display: inline-block;
    margin-top: 10px;
}

.release-link:hover {
    text-decoration: underline;
}
</style>