<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { items } from "../../data/items";

const keyword = ref("");
const limit = ref(50);
onMounted(() => {
  keyword.value = new URLSearchParams(window.location.search).get("q") ?? "";
});

const filtered = computed(() => {
  const k = keyword.value.trim();
  if (!k) return items;
  return items.filter((i) => [i.name, i.note, i.inventer, String(i.id)].some((value) => value?.includes(k)));
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
    aria-label="搜索物品"
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
        <td>{{ i.name || "未记录名称" }}</td>
        <td>{{ i.inventer || "—" }}</td>
        <td>{{ i.note }}</td>
      </tr>
    </tbody>
  </table>
  <p v-if="filtered.length > limit" class="item-count">
    <a @click.prevent="limit += 100" href="#">显示更多（还剩 {{ filtered.length - limit }} 条）</a>
  </p>
  <p v-else class="item-count">{{ filtered.length ? "已显示全部结果" : "未找到相关物品" }}</p>
</template>
