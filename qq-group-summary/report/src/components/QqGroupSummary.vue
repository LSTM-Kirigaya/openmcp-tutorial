<script setup lang="ts">
import UserTitles from './UserTitles.vue'
import ChatTopics from './ChatTopics.vue'
import Statistics from './Statistics.vue'
</script>

<template>
    <section class="qq-group-summary margin-bottom">
        <div class="summary-content">
            <UserTitles />
            <ChatTopics />
            <Statistics />
        </div>
    </section>
</template>

<style scoped>
.summary-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
}
</style>