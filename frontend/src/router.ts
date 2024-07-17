import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './pages/Home.vue'
import { verifyUser } from './apis';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children: [
        {
          path: "",
          name: "Tweets",
          component: () => import("@/components/Tweets.vue")
        },
        {
          path: "/resume",
          name: "Resume",
          component: () => import("@/components/Resume.vue")
        }
      
      ]
    },
    {
      path: "/info-form",
      name: "InfoForm",
      component: () => import("@/pages/InfoForm.vue"),
      meta: {
        loginRequired: true
      }
    },
    {
      path: "/sign-up",
      name: "SignUp",
      component: () => import("@/pages/SignUp.vue")
    },
    {
      path: "/sign-in",
      name: "SignIn",
      component: () => import("@/pages/SignIn.vue")
    }
  ]
})
router.beforeEach(async (to, from) => {
    if (to.meta.loginRequired) {
      const isAuthenticated = await verifyUser();
      if (!isAuthenticated && to.name !== "SignIn") {
        return { name: "SignIn" };
      } else {
        if (to.name === "SignIn") {
          alert("You have logged in.");
        }
      }
    }
	}
);
export default router
