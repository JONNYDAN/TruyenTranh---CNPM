<script lang="ts" setup>
import { ComicComments, ComicDetail, Comment } from '@/types';
import { meta } from '@/utils/data';

type ChapterDetail = {
  id: number;
  chapter_name: string;
  chapter_api_data: string;
};
type Tab = 'chapters' | 'comments';

const route = useRoute();
const comicId = route.params.comicId as string;
const CHAPTER_PER_PAGE = 50;

const chaptersSection = ref<ChapterDetail[]>([]);
const currentTab = ref<Tab>('chapters');
const comments = ref<Comment[]>([]);
const description = ref<any>(null);

const commentPage = ref<number>(1);
const currentChapterPage = ref<number>(0);
const isEnd = ref<boolean>(false);

const isFetching = ref<boolean>(false);
const isTooLongDescription = ref<boolean>(false);
const showFullDescription = ref<boolean>(false);

const showChapterSelection = ref<boolean>(false);
const currentDownloadChapterPage = ref<number>(0);
const chaptersDownloadSection = ref<ChapterDetail[]>([]);
const showDownloadModal = ref<boolean>(false);
const downloadChapters = ref<number[]>([]);


  const [
    comicDetail
  ] = await Promise.all([
      useFetchData(`/truyen-tranh/${comicId}`),
    ]);

    const comic = comicDetail.data.item;

    console.log('Comic:', comic );


// Ensure comic.chapters is an array
const chapters = Array.isArray(comic.chapters) ? comic.chapters : [];
const serverData = Array.isArray(chapters[0].server_data) ? chapters[0].server_data : [];
const total_chapter = serverData.length; 

console.log(chapters[0].server_data);
console.log(total_chapter);

const totalChapterPage = !isNaN(Number(total_chapter))
  ? Math.ceil(Number(total_chapter) / CHAPTER_PER_PAGE)
  : 0;

console.log(totalChapterPage);


const getChapter = (start: number, end: number) => {
  const limit = CHAPTER_PER_PAGE * 6;
  const chapters = serverData
    .filter(( chapter : any, idx: number) => {
      if(idx >= start && idx <= end){
        return true
      }
      return false
    });
  return chapters;
};


chaptersSection.value = getChapter(0, CHAPTER_PER_PAGE);
chaptersDownloadSection.value = getChapter(0, CHAPTER_PER_PAGE);

const onChangeChapterGroup = (idx: number) => {
  currentChapterPage.value = idx;
  chaptersSection.value = getChapter(
    idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1,
    (idx + 1) * CHAPTER_PER_PAGE
  );
};

const onChangeChapterDownloadGroup = (idx: number) => {
  currentDownloadChapterPage.value = idx;
  chaptersDownloadSection.value = getChapter(
    idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1,
    (idx + 1) * CHAPTER_PER_PAGE
  );
};

const getComments = async () => {
  try {
    isFetching.value = true;
    commentPage.value += 1;
    const data = await useFetchData(
      `/truyen-tranh/${comicId}/comments?page=${commentPage.value}`
    );
    comments.value = [...comments.value, ...data.comments];
    if (commentPage.value >= data.total_pages) isEnd.value = true;
  } catch (err) {
    console.log(err);
  } finally {
    isFetching.value = false;
  }
};

const onAddDownloadChapter = (chapterId: number) => {
  if (downloadChapters.value.includes(chapterId)) {
    const chapterIdx = downloadChapters.value.indexOf(chapterId);
    downloadChapters.value.splice(chapterIdx, 1);
  } else {
    downloadChapters.value = [...downloadChapters.value, chapterId];
  }
};

const handleDownloadChapters = async () => {
  try {
    for (const chapterId of downloadChapters.value) {
      const href = `/download?comicId=${comicId}&chapterId=${chapterId}`;
      const a = document.createElement('a');
      a.href = href;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(href);
    }
    showDownloadModal.value = false;
    downloadChapters.value = [];
  } catch (err) {
    console.log(err);
  }
};

onMounted(() => {
  if (description.value) {
    const { clientHeight, scrollHeight } = description.value;
    isTooLongDescription.value = clientHeight < scrollHeight;
  }
});

watch(showDownloadModal, (status) => {
  document.body.style.overflow = status ? 'hidden' : 'auto';
});

useSeoMeta(
  meta({
    title: comic.name + ' | STORIES',
    description: comic.content,
    image: comic.thumb_url,
  })
);
useServerSeoMeta(
  meta({
    title: comic.name + ' | STORIES',
    description: comic.content,
    image: comic.thumb_url,
  })
);

const baseUrl = 'https://otruyenapi.com/uploads/comics/';
const imageFile = ref(comic.thumb_url);

const imageSrc = computed(() => `${baseUrl}${imageFile.value}`);
</script>


<template>
  <div class="relative pt-12 px-4 min-h-screen">
    <div
      class="absolute top-0 inset-x-0 h-80 bg-gradient-to-b from-slate-100 -z-10"
    />
    <div
      class="max-w-5xl mx-auto border-4 border-transparent p-0 rounded-xl sm:grid sm:grid-cols-4 gap-6 md:p-4 md:border-white"
    >
      <div
        class="aspect-[2/3] w-56 mx-auto sm:w-full rounded-lg border-2 overflow-hidden border-slate-500 relative sm:col-span-1"
      >
        <img
          class="w-full h-full object-cover"
          :src="imageSrc"
          :alt="comic.name"
          draggable="false"
        />
        <div
          class="flex gap-1 absolute font-bold top-0 inset-x-0 z-10 text-xs text-white"
        >
          <span
            v-if="comic.status === 'Finished'"
            class="bg-sky-500 py-0.5 px-2 rounded-b-sm first:rounded-bl-none"
          >
            End
          </span>
        </div>
      </div>
      <div class="sm:col-span-3">
        <h4 class="text-3xl font-extrabold mt-5 sm:mt-0">{{ comic.name }}</h4>
        <div class="font-bold text-sm flex flex-wrap items-center gap-2 my-1">
          <NuxtLink
            v-for="genre in comic.category"
            :to="`/genres?type=${genre.id}`"
            class="px-2 py-0.5 rounded bg-transparent border-2 border-slate-300 duration-100 hover:bg-slate-300"
          >
            {{ genre.name }}
          </NuxtLink>
        </div>
        <div class="font-semibold flex items-center gap-2 my-1">
          Tác giả:
          <template v-if="Array.isArray(comic.author)">
            <div v-for="(author, idx) in comic.author" :key="author">
              <NuxtLink
                :to="`/search?q=${author.replace(/\s+/g, '+')}`"
                class="text-fuchsia-500"
              >
                {{ author }}
              </NuxtLink>
              <span class="select-none" v-if="idx < comic.author.length - 1">
                -
              </span>
            </div>
          </template>
          
          <template v-else>
            <NuxtLink
                :to="`/search?q=${(comic.author || '').replace(/\s+/g, '+')}`"
                class="text-fuchsia-500"
              >
                {{ comic.author }}
            </NuxtLink>

          </template>
        </div>
        <div class="mt-2" v-if="comic.content">
          <p
            :class="showFullDescription ? 'line-clamp-none' : 'line-clamp-5'"
            ref="description"
          >
            <span v-html="comic.content"></span>
          </p>
          <button
            v-if="isTooLongDescription"
            class="font-semibold hover:underline"
            @click="showFullDescription = !showFullDescription"
          >
            {{ showFullDescription ? 'Show less' : 'Show more' }}
          </button>
        </div>
        <div
          class="flex flex-col sm:flex-row items-center gap-3 mt-5 font-bold"
        >
          <button
          @click="
              () => {
                if (!comic.chapters || !comic.chapters.length) return;
                navigateTo(`/truyen-tranh/${comic.slug}/1`);
              }
            "
            :class="`btn-more ${
              comic.chapters && comic.chapters.length
                ? 'border-slate-500 bg-slate-500'
                : 'border-gray-500 bg-gray-500'
            }`"
            :disabled="!comic.chapters || !comic.chapters.length"

          >
            <div class="svg-wrapper-1">
              <div class="svg-wrapper">
                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-book"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 19a9 9 0 0 1 9 0a9 9 0 0 1 9 0" /><path d="M3 6a9 9 0 0 1 9 0a9 9 0 0 1 9 0" /><path d="M3 6l0 13" /><path d="M12 6l0 13" /><path d="M21 6l0 13" /></svg>
              </div>
            </div>
            <span>Đọc</span>
          </button>

          <button
            @click="showDownloadModal = true"
            :class="`btn-more ${
              comic.chapters && comic.chapters.length
                ? 'border-slate-500 bg-slate-500'
                : 'border-gray-500 bg-gray-500'
            }`"
            :disabled="!comic.chapters || !comic.chapters.length"
          >
            <div class="svg-wrapper-1">
              <div class="svg-wrapper">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="icon icon-tabler icon-tabler-download"
                >
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
                  <path d="M7 11l5 5l5 -5" />
                  <path d="M12 4l0 12" />
                </svg>
              </div>
            </div>
            <span>Download</span>
          </button>
        </div>
      </div>
    </div>
    <div class="max-w-5xl mx-auto mt-5">
      <div
        class="flex items-center gap-6 font-bold text-lg sm:text-xl border-b-2 py-1"
      >
        <button
          :class="`flex items-center gap-1 ${
            currentTab === 'chapters' ? 'text-slate-500' : ''
          }`"
          @click="currentTab = 'chapters'"
        >
          <Icon name="bytesize:book" size="20" />
          Chapters
        </button>
      </div>
      <div v-show="currentTab === 'chapters'">
        <h4
          class="mt-6 text-center text-2xl font-bold text-gray-700 select-none"
          v-if="!comic.chapters || !comic.chapters.length"
        >
          No Chapter
        </h4>
        <div
          v-else
          class="flex items-center gap-3 my-5 text-gray-800 font-semibold text-sm flex-wrap"
        >
          <button
            v-for="(_, idx) in new Array(totalChapterPage)"
            :class="`px-2 py-0.5 rounded-full ${
              idx === currentChapterPage
                ? 'bg-slate-100 text-slate-500'
                : 'bg-gray-100'
            }`"
            @click="onChangeChapterGroup(idx)"
          >
            <template v-if="idx + 1 < totalChapterPage">
              {{
                `${idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1} - ${
                  (idx + 1) * CHAPTER_PER_PAGE
                }`
              }}
            </template>
            <template v-else>
              {{
                `${
                  totalChapterPage === 1 ? 0 : idx * CHAPTER_PER_PAGE + 1
                } - ${total_chapter}`
              }}
            </template>
          </button>
        </div>
        <ul class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <NuxtLink
            v-for="chapter in chaptersSection"
            class="border rounded px-3 py-2 truncate hover:bg-slate-50 duration-100"
            :to="`/truyen-tranh/${comicId}/${chapter.chapter_name}`"
          >
            <abbr :title="chapter.chapter_name" class="no-underline">
              Chap {{ chapter.chapter_name }}
            </abbr>
          </NuxtLink>
        </ul>
      </div>
      
    </div>
  </div>
  <!-- Download -->
  <div
    :class="`fixed z-50 inset-0 bg-[rgba(0,0,0,0.8)] flex flex-col items-center justify-center duration-200 ${
      showDownloadModal
        ? 'opacity-1 pointer-events-auto'
        : 'opacity-0 pointer-events-none'
    }`"
  >
    <img
      src="@/assets/img/download_girls.webp"
      alt="Download"
      draggable="false"
    />
    <div class="bg-white rounded-lg py-4 px-6 w-[90vw] max-w-3xl">
      <div class="flex flex-col sm:flex-row items-center gap-2.5 sm:gap-5">
        <h3 class="text-2xl font-semibold">Select chapters</h3>
        <div
          class="border rounded px-3 py-1 relative cursor-pointer"
          @click="showChapterSelection = !showChapterSelection"
        >
          Chapters
          <Icon name="icon-park-outline:down" size="24" class="ml-2" />
          <ul
            class="absolute top-10 w-40 right-1/2 translate-x-1/2 border rounded bg-white max-h-60 overflow-auto"
            v-show="showChapterSelection"
          >
            <li
              v-for="(_, idx) in new Array(totalChapterPage)"
              :class="`px-2 py-1 border-b last:border-b-0 ${
                idx === currentDownloadChapterPage
                  ? 'text-slate-500 font-medium'
                  : ''
              }`"
              @click="onChangeChapterDownloadGroup(idx)"
            >
              <template v-if="idx + 1 < totalChapterPage">
                {{
                  `${idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1} - ${
                    (idx + 1) * CHAPTER_PER_PAGE
                  }`
                }}
              </template>
              <template v-else>
                {{
                  `${
                    totalChapterPage === 1 ? 0 : idx * CHAPTER_PER_PAGE + 1
                  } - ${total_chapter}`
                }}
              </template>
            </li>
          </ul>
        </div>
      </div>
      <ul
        class="grid sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3 max-h-[45vh] overflow-auto my-3 py-1 pr-1 select-none"
      >
        <li
          v-for="chapter in chaptersDownloadSection"
          :key="chapter.id"
          :class="`border rounded px-2 py-1 cursor-pointer duration-100 truncate ${
            downloadChapters.includes(chapter.id)
              ? 'border-slate-500 bg-slate-500 text-white'
              : ''
          }`"
          @click="onAddDownloadChapter(chapter.id)"
        >
          {{ chapter.chapter_name }}
        </li>
      </ul>
      <div class="flex items-center justify-end gap-5 font-medium">
        <button class="text-rose-500" @click="showDownloadModal = false">
          Cancel
        </button>
        <button
          :class="`text-white px-2.5 py-1.5 rounded flex items-center gap-1.5 ${
            downloadChapters.length
              ? 'border-slate-500 bg-slate-500'
              : 'border-gray-500 bg-gray-500'
          }`"
          @click="handleDownloadChapters"
          :disabled="!downloadChapters.length"
        >
          Download
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media only screen and (min-width: 320px) and (max-width: 576px) {
  .responsive-devices {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media only screen and (min-width: 576px) and (max-width: 768px) {
  .responsive-devices {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.5rem;
  }
  .title {
    font-size: 1.5rem;
    line-height: 2rem;
  }
}
</style>
