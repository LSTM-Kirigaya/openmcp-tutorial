<template>
    <section class="qq-group-summary margin-bottom">
        <div class="summary-content">
            <div class="user-titles">
                <h3>🏅 本日战绩</h3>
                <div class="title-grid">
                    <div v-for="(user, index) in userTitles" :key="index" class="user-card">
                        <div class="user-avatar">
                            <img :src="`https://q1.qlogo.cn/g?b=qq&nk=${user.qq}&s=640`" :alt="user.name" />
                        </div>
                        <div class="user-name">{{ user.name }}</div>
                        <div class="user-title">{{ user.title }}</div>
                    </div>
                </div>
            </div>

            <div class="chat-topics">
                <h3>🔥 热门话题</h3>
                <div class="topics-list">
                    <div v-for="(topic, index) in chatTopics" :key="index" class="topic-card">
                        <div class="topic-header">
                            <h4 class="topic-title">{{ topic.topic }}</h4>
                            <div class="contributors">
                                <span v-for="(contributor, cIndex) in topic.contributors" :key="cIndex"
                                    class="contributor">
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
        </div>
    </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import summarizeChat from '../summarize_chat.json'
import summarizeUser from '../summarize_user.json'

const userTitles = ref<Array<{ name: string, title: string, qq: number }>>([])
const chatTopics = ref<Array<{ topic: string, contributors: string[], detail: string }>>([])

onMounted(() => {
    userTitles.value = summarizeUser.params.titles
    chatTopics.value = summarizeChat.params.messages
})
</script>

<style scoped>

.summary-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
}

.user-titles h3,
.chat-topics h3 {
    margin-top: 0;
    color: #B988D1;
}

.title-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
}

.user-card {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    background: #f9f9f9;
    transition: all 0.2s ease;
}

.user-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-color: #B988D1;
}

.user-avatar {
    width: 80px;
    height: 80px;
    margin: 0 auto 12px;
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 0 3px 1px rgba(0, 0, 0, 0.1);
}

.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.user-name {
    font-weight: bold;
    margin-bottom: 8px;
    color: #333;
}

.user-title {
    font-size: 0.85em;
    color: #B988D1;
    background: rgba(185, 136, 209, 0.1);
    border-radius: 12px;
    padding: 4px 8px;
    display: inline-block;
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
    .title-grid {
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }

    .topic-header {
        flex-direction: column;
    }

    .user-avatar {
        width: 60px;
        height: 60px;
    }
}
</style>