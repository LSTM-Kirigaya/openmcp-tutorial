<script setup lang="ts">
import { ref } from 'vue'
import data from '../summary_statistic.json'

// 计算相当于多少本《纯粹理性批判》
// 《纯粹理性批判》大约有65万字，这里取中间值650000字作为计算基准
const pureReasonBookWords = 650000
const booksEquivalent = ref(0)

// 格式化数字显示
const formatNumber = (num: number): string => {
    if (num < 0) return '0'
    return num.toLocaleString()
}

// 计算书籍等效数量
const calculateBooksEquivalent = () => {
    if (data.total_characters < 0) return '0'
    return (data.total_characters / pureReasonBookWords).toFixed(5)
}

booksEquivalent.value = parseFloat(calculateBooksEquivalent())
</script>

<template>
    <section class="statistics-section margin-bottom">
        <h2>📊 群聊数据统计</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{{ formatNumber(data.message_count) }}</div>
                <div class="stat-label">消息条数</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{{ formatNumber(data.total_characters) }}</div>
                <div class="stat-label">总字数</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{{ formatNumber(data.participant_count) }}</div>
                <div class="stat-label">参与人数</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{{ data.most_active_period }}</div>
                <div class="stat-label">最活跃时段</div>
            </div>

            <div class="stat-card books-stat">
                <div class="stat-value">≈{{ booksEquivalent }}本</div>
                <div class="stat-label">《纯粹理性批判》</div>
            </div>
        </div>

        <div class="fun-fact">
            <p>📚 <strong>有趣的事实：</strong>
                今天我们创造的文字量相当于 {{ booksEquivalent }} 本康德的《纯粹理性批判》！
                这么多文字足够堆成一座小山了！继续加油水群，让知识的海洋更加波澜壮阔！
            </p>
        </div>
    </section>
</template>

<style scoped>
.statistics-section {
    padding: 24px;
    border-radius: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.statistics-section h2 {
    margin-top: 0;
    text-align: center;
    font-size: 1.8rem;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 20px;
    margin: 24px 0;
}

.stat-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: transform 0.3s ease, background 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.25);
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 8px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.stat-label {
    font-size: 1rem;
    opacity: 0.9;
}

.books-stat {
    background: rgba(255, 215, 0, 0.25);
}

.books-stat:hover {
    background: rgba(255, 215, 0, 0.4);
}

.fun-fact {
    margin-top: 24px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    text-align: center;
    font-size: 1.1rem;
    line-height: 1.6;
}

.fun-fact strong {
    color: #FFD700;
}

@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .stat-value {
        font-size: 1.5rem;
    }

    .statistics-section {
        padding: 16px;
    }
}

@media (max-width: 480px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .stat-value {
        font-size: 1.8rem;
    }
}
</style>