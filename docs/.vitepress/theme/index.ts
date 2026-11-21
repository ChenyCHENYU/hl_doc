import DefaultTheme from "vitepress/theme";
import type { Theme } from "vitepress";
import Layout from "./Layout.vue";
import NotFound from "./components/NotFound.vue";
import "./custom.css";
import Home from "./home/index.vue";
import PetShowcase from "./components/PetShowcase.vue";
import ItemTable from "./components/ItemTable.vue";
import GuideCategories from "./components/GuideCategories.vue";
import HeroWall from "./components/HeroWall.vue";
import PetCodex from "./components/PetCodex.vue";
import AdvChart from "./components/AdvChart.vue";
import PetPrices from "./components/PetPrices.vue";
import TowerTable from "./components/TowerTable.vue";
import ResourcesPage from "./components/ResourcesPage.vue";
import EvolutionShowcase from "./components/EvolutionShowcase.vue";
import EvolutionExplorer from "./components/EvolutionExplorer.vue";
import TitleLadder from "./components/TitleLadder.vue";
import TopicRelated from "./components/TopicRelated.vue";
import AscensionGuide from "./components/AscensionGuide.vue";
import PetDetail from "./components/PetDetail.vue";
import TopicHeader from "./components/TopicHeader.vue";
import LibraryList from "./components/LibraryList.vue";
import TermDefs from "./components/TermDefs.vue";
import HelpCards from "./components/HelpCards.vue";
import MuseumHall from "./components/MuseumHall.vue";
import ForgeGuide from "./components/ForgeGuide.vue";
import QuestFlow from "./components/QuestFlow.vue";
import CommentBox from "./components/CommentBox.vue";
import AuthorCard from "./components/AuthorCard.vue";

export default {
  extends: DefaultTheme,
  Layout,
  NotFound,
  enhanceApp: ({ app }) => {
    app.component("Home", Home);
    app.component("PetShowcase", PetShowcase);
    app.component("ItemTable", ItemTable);
    app.component("GuideCategories", GuideCategories);
    app.component("HeroWall", HeroWall);
    app.component("PetCodex", PetCodex);
    app.component("AdvChart", AdvChart);
    app.component("PetPrices", PetPrices);
    app.component("TowerTable", TowerTable);
    app.component("ResourcesPage", ResourcesPage);
    app.component("EvolutionShowcase", EvolutionShowcase);
    app.component("EvolutionExplorer", EvolutionExplorer);
    app.component("TitleLadder", TitleLadder);
    app.component("TopicRelated", TopicRelated);
    app.component("AscensionGuide", AscensionGuide);
    app.component("PetDetail", PetDetail);
    app.component("TopicHeader", TopicHeader);
    app.component("LibraryList", LibraryList);
    app.component("TermDefs", TermDefs);
    app.component("HelpCards", HelpCards);
    app.component("MuseumHall", MuseumHall);
    app.component("ForgeGuide", ForgeGuide);
    app.component("QuestFlow", QuestFlow);
    app.component("CommentBox", CommentBox);
    app.component("AuthorCard", AuthorCard);
  },
} satisfies Theme;
