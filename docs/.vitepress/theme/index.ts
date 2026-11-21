import DefaultTheme from "vitepress/theme";
import type { Theme } from "vitepress";
import { defineAsyncComponent } from "vue";
import Layout from "./Layout.vue";
import NotFound from "./components/NotFound.vue";
import "./custom.css";
import "./field.css";
import Home from "./home/index.vue";
import PetShowcase from "./components/PetShowcase.vue";
import GuideCategories from "./components/GuideCategories.vue";
import AdvChart from "./components/AdvChart.vue";
import TitleLadder from "./components/TitleLadder.vue";
import AscensionGuide from "./components/AscensionGuide.vue";
import TopicHeader from "./components/TopicHeader.vue";
import TermDefs from "./components/TermDefs.vue";
import ForgeGuide from "./components/ForgeGuide.vue";
import CommentBox from "./components/CommentBox.vue";
import AuthorCard from "./components/AuthorCard.vue";

export default {
  extends: DefaultTheme,
  Layout,
  NotFound,
  enhanceApp: ({ app }) => {
    app.component("Home", Home);
    app.component("PetShowcase", PetShowcase);
    app.component("ItemTable", defineAsyncComponent(() => import("./components/ItemTable.vue")));
    app.component("GuideCategories", GuideCategories);
    app.component("HeroWall", defineAsyncComponent(() => import("./components/HeroWall.vue")));
    app.component("PetCodex", defineAsyncComponent(() => import("./components/PetCodex.vue")));
    app.component("AdvChart", AdvChart);
    app.component("PetPrices", defineAsyncComponent(() => import("./components/PetPrices.vue")));
    app.component("TowerTable", defineAsyncComponent(() => import("./components/TowerTable.vue")));
    app.component("ResourcesPage", defineAsyncComponent(() => import("./components/ResourcesPage.vue")));
    app.component("EvolutionShowcase", defineAsyncComponent(() => import("./components/EvolutionShowcase.vue")));
    app.component("EvolutionExplorer", defineAsyncComponent(() => import("./components/EvolutionExplorer.vue")));
    app.component("TitleLadder", TitleLadder);
    app.component("TopicRelated", defineAsyncComponent(() => import("./components/TopicRelated.vue")));
    app.component("AscensionGuide", AscensionGuide);
    app.component("PetDetail", defineAsyncComponent(() => import("./components/PetDetail.vue")));
    app.component("TopicHeader", TopicHeader);
    app.component("LibraryList", defineAsyncComponent(() => import("./components/LibraryList.vue")));
    app.component("TermDefs", TermDefs);
    app.component("HelpCards", defineAsyncComponent(() => import("./components/HelpCards.vue")));
    app.component("MuseumHall", defineAsyncComponent(() => import("./components/MuseumHall.vue")));
    app.component("ForgeGuide", ForgeGuide);
    app.component("QuestFlow", defineAsyncComponent(() => import("./components/QuestFlow.vue")));
    app.component("FireQuestGuide", defineAsyncComponent(() => import("./components/FireQuestGuide.vue")));
    app.component("PortalSearch", defineAsyncComponent(() => import("./components/PortalSearch.vue")));
    app.component("TrainingMaps", defineAsyncComponent(() => import("./components/TrainingMaps.vue")));
    app.component("CommentBox", CommentBox);
    app.component("AuthorCard", AuthorCard);
  },
} satisfies Theme;
