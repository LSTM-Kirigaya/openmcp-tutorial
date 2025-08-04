<script setup lang="ts">
import { ref, onMounted } from 'vue'
import summarizeUser from '../summarize_user.json'

interface UserTitle {
    name: string
    title: string
    qq: number
    mbti: string
}

const userTitles = ref<UserTitle[]>([])

onMounted(() => {
    userTitles.value = summarizeUser.titles
})
</script>

<template>
    <div class="user-titles">
        <h3>🏅 本日战绩</h3>
        <div class="title-grid">
            <div v-for="(user, index) in userTitles" :key="index" class="user-card">
                <div class="user-avatar">
                    <img :src="`https://q1.qlogo.cn/g?b=qq&nk=${user.qq}&s=640`" :alt="user.name" />
                </div>
                <div class="user-name">{{ user.name }}</div>
                <div class="user-title">{{ user.title }}</div>
                <div class="user-mbti">{{ user.mbti }}</div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.user-titles h3 {
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
    margin-bottom: 8px;
}

.user-mbti {
    font-size: 0.8em;
    color: #666;
    font-weight: bold;
}

@media screen and (max-width: 600px) {
    .title-grid {
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }

    .user-avatar {
        width: 60px;
        height: 60px;
    }
}
</style>