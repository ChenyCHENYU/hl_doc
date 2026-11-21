<script setup lang="ts">
import { evolutionChains, petRules } from "../../data/pets";
</script>

<template>
  <div class="chain-flow">
    <template v-for="(c, i) in evolutionChains" :key="c.tier">
      <div class="node">
        <span class="tier">{{ c.tier }}</span>
        <div v-for="p in c.examples" :key="p" class="pet">{{ p }}</div>
      </div>
      <span v-if="i < evolutionChains.length - 1" class="arrow">&#8594;</span>
    </template>
  </div>
  <div class="rule-list">
    <ul>
      <li v-for="r in petRules" :key="r.title">
        <b>{{ r.title }}：</b>{{ r.detail }}
      </li>
    </ul>
  </div>
</template>
