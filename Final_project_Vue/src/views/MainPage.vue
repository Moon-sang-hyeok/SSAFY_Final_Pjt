<template>
  <div id="main-page">
    <!-- 뉴스 슬라이더 -->
    <div class="slider">
      <div
        class="slide"
        v-for="(news, index) in newsList"
        :key="index"
        :class="{ active: currentSlide === index }"
      >
        <a :href="news.url" target="_blank">
          <div class="image-container">
            <img
              :src="news.image"
              :alt="news.title"
              @error="onImageError"
            />
          </div>
        </a>
      </div>
      <div class="controls">
        <button @click="prevSlide">❮</button>
        <button @click="nextSlide">❯</button>
      </div>
      <div class="indicators">
        <span
          v-for="(news, index) in newsList"
          :key="index"
          :class="{ active: currentSlide === index }"
          @click="goToSlide(index)"
        ></span>
      </div>
    </div>

    <!-- 운세 보기 -->
    <h1>오늘의 운세</h1>
    <button @click="getFortune">운세 보기</button>
    <div v-if="fortune">
      <p>{{ fortune }}</p>
    </div>
    <div v-else>
      <p>운세를 가져오는 중...</p>
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from "vue";
import image1 from "@/assets/캡처1.jpeg"; // 이미지 경로를 import로 정의
import image2 from "@/assets/캡처2.jpeg";
import image3 from "@/assets/캡처3.jpeg";
import placeholderImage from "@/assets/logo.svg"
export default {
  name: "MainPage",
  setup() {
    const fortune = ref(null);
    const newsList = ref([
  {
    title: "한경 기사 1",
    image: image1, // import한 이미지 사용
    url: "https://www.hankyung.com/article/2024081162591",
  },
  {
    title: "한경 기사 2",
    image: image2,
    url: "https://www.fntimes.com/html/view.php?ud=2024101118020054237391cf86_18",
  },
  {
    title: "한경 기사 3",
    image: image3,
    url: "https://www.fntimes.com/html/view.php?ud=202410211205202453f09e13944d_18",
  },
]);
    const currentSlide = ref(0);

    const getFortune = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:8000/open_ai/api/open_ai/');
        fortune.value = response.data.fortune;
      } catch (error) {
        console.error("운세를 가져오는 데 오류가 발생했습니다:", error);
        fortune.value = "운세를 가져오는 데 실패했습니다.";
      }
    };

    const nextSlide = () => {
      currentSlide.value =
        (currentSlide.value + 1) % newsList.value.length;
    };

    const prevSlide = () => {
      currentSlide.value =
        (currentSlide.value - 1 + newsList.value.length) %
        newsList.value.length;
    };

    const onImageError = (event) => {
  event.target.src = require("@/assets/default-placeholder.png"); // 대체 이미지 경로
};

    onMounted(() => {
      setInterval(nextSlide, 3000); // 3초마다 슬라이드 전환
    });
    

    return {
      fortune,
      getFortune,
      newsList,
      currentSlide,
      nextSlide,
      prevSlide,
      onImageError,
    };
  },
};
</script>

<style scoped>
#main-page {
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* 슬라이더 스타일 */
.slider {
  position: relative; /* 내부 슬라이드 위치를 기준으로 설정 */
  width: 1000px;
  max-width: 1000px;
  margin: 0 auto 20px;
  overflow: hidden;
  border-radius: 10px;
  height: 500px; /* 고정 높이 설정 */
}

.slide {
  display: none; /* 기본적으로 숨김 */
  width: 100%;
  height: 100%;
}

.slide.active {
  display: block; /* 활성화된 슬라이드만 표시 */
}

.image-container {
  width: 100%;
  height: 100%;
  background-color: #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.controls {
  position: absolute;
  top: 50%;
  width: 100%;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
}

.controls button {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.controls button:hover {
  background: rgba(0, 0, 0, 0.8);
}

/* 운세 보기 스타일 */
h1 {
  color: #333;
}

p {
  font-size: 18px;
  color: #555;
}

button {
  padding: 10px 20px;
  background-color: #c1c7e1;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #555;
}
</style>
