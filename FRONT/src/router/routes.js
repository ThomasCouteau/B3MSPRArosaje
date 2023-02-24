const routes = [
  {
    path: "/",
    component: () => import("layouts/LoginLayout.vue"),
    children: [{ path: "", component: () => import("pages/LoginPage.vue") }],
  },
  {
    path: "/profile",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/ProfilePage.vue") }],
  },
  {
    path: "/create-post",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/CreatePostPage.vue") },
    ],
  },
  {
    path: "/box",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/MessagesBoxPage.vue") },
    ],
  },
  {
    path: "/conversation/:id",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/ConvPage.vue") }],
  },
  {
    path: "/search",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/MapPage.vue") }],
  },
  {
    path: "/home",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/IndexPage.vue") }],
  },
  {
    path: "/subscribe",
    component: () => import("layouts/LoginLayout.vue"),
    children: [
      { path: "", component: () => import("pages/SubscribePage.vue") },
    ],
  },

  {
    path: "/post/:id",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/PostPage.vue") }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
