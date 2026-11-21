<script setup lang="ts">
import { computed, ref } from "vue";
import { items } from "../../data/items";

const keyword = ref("");
const limit = ref(50);

const filtered = computed(() => {
  const k = keyword.value.trim();
  if (!k) return items;
  return items.filter((i) => i.name.includes(k) || i.note.includes(k) || i.inventer.includes(k));
});

const visible = computed(() => filtered.value.slice(0, limit.value));
const withInventer = items.filter((i) => i.inventer && i.inventer !== "无").length;
const withNote = items.filter((i) => i.note && i.note.length > 4).length;
</script>

<template>
  <div class="dash-cards">
    <div class="dash-card"><b>{{ items.length }}</b><span>物品条目</span></div>
    <div class="dash-card"><b>{{ withInventer }}</b><span>含出处 NPC</span></div>
    <div class="dash-card"><b>{{ withNote }}</b><span>含描述</span></div>
  </div>
  <input
    v-model="keyword"
    class="item-search"
    type="search"
    placeholder="搜索物品名称 / 描述 / 出处 NPC"
  />
  <p class="item-count">
    命中 {{ filtered.length }} 条 / 共收录 {{ items.length }} 条，当前显示 {{ visible.length }} 条
  </p>
  <table>
    <thead>
      <tr>
        <th style="width: 48px">ID</th>
        <th style="width: 140px">名称</th>
        <th style="width: 140px">出处</th>
        <th>描述</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="i in visible" :key="i.id">
        <td>{{ i.id }}</td>
        <td>{{ i.name }}</td>
        <td>{{ i.inventer }}</td>
        <td>{{ i.note }}</td>
      </tr>
    </tbody>
  </table>
  <p v-if="filtered.length > limit" class="item-count">
    <a @click.prevent="limit += 100" href="#">显示更多（还剩 {{ filtered.length - limit }} 条）</a>
  </p>
  <p v-else class="item-count">已显示全部结果</p>
</template>
