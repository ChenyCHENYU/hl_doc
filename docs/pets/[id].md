---
title: 宠物详情
aside: false
---

<script setup>
import { useData } from "vitepress";
const { params } = useData();
</script>

<PetDetail :id="params.id" />
