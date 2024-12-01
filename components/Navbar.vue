<script lang="ts" setup>
import { routes, dynamicRoutes } from '@/utils/data';

const device = ref<'mobile' | 'laptop'>('mobile');
const searchValue = ref<string>('');
let suggestComics = ref<any>([]);
const searchInput = ref<any>(null);
const showSuggest = ref<boolean>(false);
const openSidebar = ref<boolean>(false);

const handleSelectComic = (comicId: string) => {
  navigateTo(`/truyen-tranh/${comicId}`);
  searchInput.value.blur();
};

const handleSearchComics = () => {
  if (!searchValue.value.trim()) return;
  openSidebar.value = false;
  searchInput.value.blur();
  navigateTo(`/search?keyword=${searchValue.value.replace(/\s+/g, '+')}`);
};

watch(openSidebar, (status) => {
  document.body.style.overflow = status ? 'hidden' : 'auto';
});

watch(searchValue, async (newValue) => {
  if (!newValue.trim()) {
    suggestComics.value = [];
    showSuggest.value = false;
    return;
  }

  // Tìm kiếm và lấy kết quả ngay lập tức
  const result = await useFetchData(
    `/tim-kiem?keyword=${newValue.replace(/\s+/g, '+')}`
  );

  suggestComics.value = result.data.items;
  showSuggest.value = suggestComics.value.length > 0;
});

const getScreenWidth = () => {
  const width = window.innerWidth;
  device.value = width >= 1024 ? 'laptop' : 'mobile';
};

onMounted(() => {
  getScreenWidth();
  window.addEventListener('resize', getScreenWidth);
});
onBeforeUnmount(() => {
  window.removeEventListener('resize', getScreenWidth);
});
</script>

<template>
  <header class="shadow bg-white relative z-50">
    <nav
      class="max-w-7xl h-12 md:h-14 mx-auto flex items-center justify-between px-3"
    >
      <div class="flex items-center gap-2 h-full">
        <NuxtLink to="/" class="flex items-center gap-2 h-full select-none">
          <img
            src="../assets/img/logo_header.jpeg"
            alt="STORIES"
            class="h-full"
            draggable="false"
            width="150px"
            height="70px"
          />
        </NuxtLink>
      </div>
      <div class="items-center gap-2 text-lg ml-6 text-base hidden lg:flex">
        <div v-for="route in routes.slice(0, 4)" :key="route.path">
          <NuxtLink
          :to="route.path"
          class="px-4 py-2 font-bold hover:duration-150 hover:bg-slate-500 hover:text-white items-center rounded-full  "
          active-class="bg-slate-500 rounded-full text-white"
          >
          <Icon :name="route.icon" size="24" 
          class=""
          active-class="bg-slate-500 rounded-full text-white " />
          {{ route.name }}
          </NuxtLink>
        </div>
      </div>
      <div v-if="device === 'laptop'" class="items-center gap-3 flex">
        <form
          class="flex items-center rounded-full border py-2 focus-within:border-slate-500 duration-100 mx-4 relative"
          @submit.prevent="handleSearchComics"
        >
          <input
            type="text"
            class="outline-none text-sm pl-3 rounded-full"
            placeholder="Search "
            v-model="searchValue"
            ref="searchInput"
            @focus="showSuggest = suggestComics.length > 0"
            @blur="showSuggest = false"
          />
          <button type="submit" class="flex items-center px-3">
            <Icon name="iconamoon:search-bold" />
          </button>
          <ul
            class="z-10 absolute top-11 left-1/2 -translate-x-1/2 w-72 h-max max-h-80 overflow-auto shadow rounded bg-white"
            v-show="showSuggest"
          >
            <li
              v-for="comic in suggestComics"
              :key="comic.id"
              @mousedown="handleSelectComic(comic.id)"
              class="flex gap-2 p-2 border-b hover:bg-gray-200 duration-100 cursor-pointer"
            >
              <img
                :src="'https://otruyenapi.com/uploads/comics/' + comic.thumb_url"
                :alt="comic.name"
                class="border border-slate-500 w-16 h-24 object-cover object-center rounded"
              />
              <div>
                <h6 class="font-bold text-sm">
                  {{ comic.name }}
                  <span class="font-normal">
                    ({{ comic.lastest_chapter }})
                  </span>
                </h6>
                <p
                  class="text-sm font-bold text-slate-500 flex items-center gap-1"
                >
                  <template v-if="comic.author === 'Đang cập nhật'">
                    <Icon name="mdi:dots-circle" size="16" />
                    Đang cập nhật
                  </template>
                  <template v-else>
                    {{ comic.author.join(' | ') }}
                  </template>
                </p>
                <p class="text-xs font-semibold flex items-center">
                  <template v-for="genre in comic.category">
                    {{ genre.name }} |
                  </template>
                </p>
              </div>
            </li>
          </ul>
        </form>
      </div>
      <div v-else>
        <button @click="openSidebar = true">
          <Icon name="carbon:menu" size="32" />
        </button>
        <div
          :class="`fixed inset-0 bg-[rgba(0,0,0,0.85)] duration-200 ${
            openSidebar
              ? 'opacity-100 pointer-events-auto'
              : 'opacity-0 pointer-events-none'
          }`"
          @click="
            (e) => {
              if (e.currentTarget !== e.target) return;
              openSidebar = false;
            }
          "
        >
          <div
            :class="`absolute right-0 inset-y-0 bg-white p-5 pt-3 w-11/12 max-w-sm duration-200 ${
              openSidebar ? 'translate-x-0' : 'translate-x-full'
            }`"
          >
              <button
                class="ml-auto block w-max mb-2"
                @click="openSidebar = false"
              >
                <Icon name="ep:close-bold" size="28" />
              </button>
            
              <form
                class="flex items-center rounded-full border py-2 focus-within:border-slate-500 duration-100 mx-4 relative justify-between"
                @submit.prevent="handleSearchComics"
              >
                <input
                  type="text"
                  class="outline-none text-sm pl-3 rounded-full"
                  placeholder="Search "
                  v-model="searchValue"
                  ref="searchInput"
                  @focus="showSuggest = suggestComics.length > 0"
                  @blur="showSuggest = false"
                />
                <button type="submit" class="flex items-center px-3">
                  <Icon name="iconamoon:search-bold" />
                </button>
                <ul
                  class="z-10 absolute top-11 left-1/2 -translate-x-1/2 w-72 h-max max-h-80 overflow-auto shadow rounded bg-white"
                  v-show="showSuggest"
                >
                  <li
                    v-for="comic in suggestComics"
                    :key="comic.id"
                    @mousedown="handleSelectComic(comic.id)"
                    class="flex gap-2 p-2 border-b hover:bg-gray-200 duration-100 cursor-pointer"
                  >
                    <img
                      :src="'https://otruyenapi.com/uploads/comics/' + comic.thumb_url"
                      :alt="comic.name"
                      class="border border-slate-500 w-16 h-24 object-cover object-center rounded"
                    />
                    <div>
                      <h6 class="font-bold text-sm">
                        {{ comic.name }}
                        <span class="font-normal">
                          ({{ comic.lastest_chapter }})
                        </span>
                      </h6>
                      <p
                        class="text-sm font-bold text-slate-500 flex items-center gap-1"
                      >
                        <template v-if="comic.author === 'Đang cập nhật'">
                          <Icon name="mdi:dots-circle" size="16" />
                          Đang cập nhật
                        </template>
                        <template v-else>
                          {{ comic.author.join(' | ') }}
                        </template>
                      </p>
                      <p class="text-xs font-semibold flex items-center">
                        <template v-for="genre in comic.category">
                          {{ genre.name }} |
                        </template>
                      </p>
                    </div>
                  </li>
                </ul>
              </form>

              <ul class="grid gap-3 text-lg font-semibold h-[500px] overflow-y-auto pt-3 boder-radius">
                <NuxtLink
                  to="/"
                  class="p-1 "
                  active-class="text-slate-500 bg-slate-300"
                  @click="openSidebar = false"
                >
                  <Icon name="ion:home-outline" size="20" class="mr-1" />
                  Home
                </NuxtLink>
                <NuxtLink
                  to="/genres"
                  class="p-1 "
                  active-class="text-slate-500 bg-slate-300"
                  @click="openSidebar = false"
                >
                  <Icon name="fa-solid:list" size="20" class="mr-1" />
                  Thể loại
                </NuxtLink>
                <NuxtLink
                  to="/danh-sach/truyen-moi"
                  class="p-1 "
                  active-class="text-slate-500 bg-slate-300"
                  @click="openSidebar = false"
                >
                  <Icon name="fa-solid:star" size="20" class="mr-1" />
                  Truyện mới
                </NuxtLink>
                <NuxtLink
                  to="/danh-sach/sap-ra-mat"
                  class="p-1 "
                  active-class="text-slate-500 bg-slate-300"
                  @click="openSidebar = false"
                >
                  <Icon name="fa-solid:hourglass-start" size="20" class="mr-1" />
                  Sắp ra mắt
                </NuxtLink>
                <NuxtLink
                  v-for="route in dynamicRoutes"
                  :key="route.path"
                  :to="route.path"
                  class="p-1 "
                  active-class="text-slate-500 bg-slate-300"
                  @click="openSidebar = false"
                >
                <Icon name="fa-solid:caret-right" size="24" 
                class=""
                active-class="bg-slate-500 rounded-full text-white " />
                  {{ route.title }}
                </NuxtLink>
              </ul>
              <div class="items-center gap-2 text-lg ml-6 text-base lg:flex">
                <NuxtLink
                :to="routes[4].path"
                class="px-4 py-2 font-bold hover:duration-150 hover:bg-slate-500 hover:text-white items-center rounded-full  "
                active-class="bg-slate-500 rounded-full text-white"
                >
                <Icon :name="routes[4].icon" size="24" 
                class=""
                active-class="bg-slate-500 rounded-full text-white " />
                </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <div class="items-center gap-2 text-lg text-base hidden lg:flex">
        <NuxtLink
        :to="routes[4].path"
        class="px-2 py-1 font-bold hover:duration-150 hover:bg-slate-500 hover:text-white items-center rounded-full"
        active-class="bg-slate-500 rounded-full text-white"
        >
        <Icon :name="routes[4].icon" size="30" 
        class=""
        active-class="bg-slate-500 rounded-full text-white " />
        </NuxtLink>
      </div>
    </nav>
  </header>
</template>

<style scoped>
@font-face {
  font-family: Chocopy;
  src: url(@/assets/fonts/chocopy.ttf);
}

.chocopy {
  font-family: Chocopy, sans-serif;
}
</style>
