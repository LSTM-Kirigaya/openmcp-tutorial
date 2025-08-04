<script setup lang="ts">
import { ref, onMounted } from 'vue'
import summarizeChat from '../summarize_chat.json'

interface ChatTopic {
    topic: string
    contributors: string[]
    detail: string
}

const chatTopics = ref<ChatTopic[]>([])

onMounted(() => {
    chatTopics.value = summarizeChat.messages
})
</script>

<template>
    <div class="chat-topics">
        <h3>🔥 热门话题</h3>
        <div class="topics-list">
            <div v-for="(topic, index) in chatTopics" :key="index" class="topic-card">
                <div class="topic-header">
                    <h4 class="topic-title">{{ topic.topic }}</h4>
                    <div class="contributors">
                        <span v-for="(contributor, cIndex) in topic.contributors" :key="cIndex" class="contributor">
                            {{ contributor }}
                        </span>
                    </div>
                </div>
                <div class="topic-detail">
                    {{ topic.detail }}
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.chat-topics h3 {
    margin-top: 0;
    color: #B988D1;
}

.topics-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.topic-card {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 20px;
    background: #fafafa;
}

.topic-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
    flex-wrap: wrap;
    gap: 10px;
}

.topic-title {
    margin: 0;
    color: #333;
    flex: 1;
}

.contributors {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.contributor {
    background: #B988D1;
    color: white;
    border-radius: 12px;
    padding: 4px 10px;
    font-size: 0.8em;
}

.topic-detail {
    color: #666;
    line-height: 1.6;
}

@media screen and (max-width: 600px) {
    .topic-header {
        flex-direction: column;
    }
}
</style>