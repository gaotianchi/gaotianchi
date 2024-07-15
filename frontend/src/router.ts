import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './pages/Home.vue'
import { verifyUser } from '@/apis';
import { loginStatus } from '@/store';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: "/signup",
      component: () => import("./pages/SignUp.vue")
    },
    {
      path: "/signin",
      name: "Login",
      component: () => import("./pages/SignIn.vue")
    },
    {
      path: "/resume",
      component: () => import("./pages/Resumes.vue")
    }
  ]
})
router.beforeEach(async (to, from) => {
	if (to.meta.loginRequired) {
		const isAuthenticated = await verifyUser();
    loginStatus.value = isAuthenticated;
		if (!isAuthenticated && to.name !== "Login") {
			return { name: "Login" };
		} else {
			if (to.name === "Login") {
				alert("You have logged in.");
			}
		}
	}
});
export default router
