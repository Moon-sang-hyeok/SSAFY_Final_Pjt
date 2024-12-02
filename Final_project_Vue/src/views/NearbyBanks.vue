<template>
  <div class="nearby-banks">
    <h1>주변 은행 검색</h1>

    <!-- 검색창 -->
    <div class="search-box">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="위치를 입력하세요"
        @input="searchLocation"
      />
      <button @click="searchLocation">검색</button>
    </div>
    
    <!-- 검색어 결과 리스트 -->
    <div v-if="searchResults.length > 0" class="search-results">
      <ul>
        <li
          v-for="(result, index) in searchResults"
          :key="index"
          @click="selectLocation(result)"
        >
          {{ result.place_name }}
        </li>
      </ul>
    </div>

    <!-- 지도 및 오른쪽 선택 정보 -->
    <div class="content-wrapper">
      <!-- Kakao 지도 표시 영역 -->
      <div id="map" class="map"></div>

      <!-- 선택된 장소와 은행 정보 -->
      <div class="selected-info">
        <h2>선택된 장소</h2>
        <p v-if="selectedPlace">장소명: {{ selectedPlace.place_name }}</p>
        <p v-if="selectedPlace">주소: {{ selectedPlace.address_name }}</p>
        
        <h2>주변 은행</h2>
        <ul>
          <li v-for="(bank, index) in selectedBanks" :key="index">
            <strong>{{ bank.place_name }}</strong><br />
            {{ bank.address_name }}
          </li>
        </ul>
        
        <!-- 선택된 은행 정보 -->
        <div v-if="selectedBank">
          <h3>선택된 은행</h3>
          <p>은행명: {{ selectedBank.place_name }}</p>
          <p>주소: {{ selectedBank.address_name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "NearbyBanks",
  setup() {
    const map = ref(null); // 지도 객체
    const searchQuery = ref(""); // 검색 입력
    const selectedPlace = ref(null); // 선택된 장소 정보
    const selectedBanks = ref([]); // 선택된 은행 리스트
    const selectedBank = ref(null); // 선택된 은행 정보
    const markers = ref([]); // 현재 표시된 마커 배열
    const infowindow = ref(null); // InfoWindow 객체
    const searchResults = ref([]); // 실시간 검색 결과

    onMounted(() => {
      const apiKey = import.meta.env.VITE_KAKAO_MAP_API_KEY;

      // Kakao Maps API 스크립트 로드
      const script = document.createElement("script");
      script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${apiKey}&libraries=services`;
      script.onload = () => {
        window.kakao.maps.load(() => {
          const container = document.getElementById("map");
          const options = {
            center: new window.kakao.maps.LatLng(37.5665, 126.9780), // 서울 중심
            level: 3, // 확대 레벨
          };
          map.value = new window.kakao.maps.Map(container, options);
          infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 }); // InfoWindow 생성
        });
      };
      document.head.appendChild(script);
    });

    // 검색 실행
    const searchLocation = () => {
      if (!window.kakao || !searchQuery.value) return;

      const places = new window.kakao.maps.services.Places(map.value);

      // 키워드로 장소 검색
      places.keywordSearch(searchQuery.value, (data, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          // 검색 결과 리스트에 업데이트
          searchResults.value = data;
        } else {
          searchResults.value = [];
        }
      });
    };

    // 위치 선택 시 처리
    const selectLocation = (place) => {
      // 장소 클릭 시, 해당 위치로 지도 이동
      const coords = new window.kakao.maps.LatLng(place.y, place.x);
      map.value.setCenter(coords);

      // 선택된 장소 정보 설정
      selectedPlace.value = {
        place_name: place.place_name,
        address_name: place.address_name,
      };

      // 선택된 장소를 중심으로 은행 검색
      searchBanks(coords);

      // 검색어 리스트 숨기기
      searchResults.value = [];
    };

    // 은행 카테고리 검색
    const searchBanks = (coords) => {
      if (!map.value) return;

      // 기존 마커 제거
      clearMarkers();

      const places = new window.kakao.maps.services.Places(map.value);

      // 은행 카테고리(BK9)로 검색
      places.categorySearch(
        "BK9",
        (data, status) => {
          if (status === window.kakao.maps.services.Status.OK) {
            // 검색된 은행 리스트를 업데이트
            selectedBanks.value = data;

            // 검색 결과로 마커 표시
            data.forEach((place) => {
              displayMarker(place);
            });
          } else {
            console.error("은행 검색에 실패했습니다.");
          }
        },
        { location: coords, radius: 1000, useMapBounds: true } // 1km 반경
      );
    };

    // 마커 표시
    const displayMarker = (place) => {
      const marker = new window.kakao.maps.Marker({
        map: map.value,
        position: new window.kakao.maps.LatLng(place.y, place.x),
      });

      // 마커 클릭 이벤트
      window.kakao.maps.event.addListener(marker, "click", () => {
        infowindow.value.setContent(` 
          <div style="padding:5px;font-size:12px;">
            <strong>${place.place_name}</strong><br/>
            ${place.address_name}
          </div>
        `);
        infowindow.value.open(map.value, marker);

        // 선택된 은행 정보 업데이트
        selectedBank.value = {
          place_name: place.place_name,
          address_name: place.address_name,
        };
      });

      markers.value.push(marker); // 마커 저장
    };

    // 기존 마커 삭제
    const clearMarkers = () => {
      markers.value.forEach((marker) => marker.setMap(null));
      markers.value = [];
      if (infowindow.value) infowindow.value.close();
    };

    return {
      searchQuery,
      selectedPlace,
      selectedBanks,
      selectedBank,
      searchLocation,
      searchResults,
      selectLocation,
    };
  },
};
</script>

<style scoped>
/* 기본 스타일 */
body {
  font-family: 'Arial', sans-serif;
  background-color: #f8f9fa;
  margin: 0;
  padding: 0;
}

.nearby-banks {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  font-size: 32px;
  color: #343a40;
  margin-bottom: 40px;
}

.search-box {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.search-box input {
  padding: 12px 20px;
  font-size: 16px;
  border-radius: 25px;
  border: 2px solid #007bff;
  width: 60%;
  margin-right: 10px;
}

.search-box button {
  padding: 12px 20px;
  font-size: 16px;
  border-radius: 25px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.search-box button:hover {
  background-color: #0056b3;
}

.content-wrapper {
  display: flex;
  flex-direction: row; 
  margin-top: 20px;
}

.map {
  width: 70%;
  height: 500px;
  margin-right: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.selected-info {
  width: 28%;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  max-height: 500px;
  overflow-y: auto;
}

h2 {
  font-size: 22px;
  color: #007bff;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  color: #495057;
  margin: 5px 0;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  padding: 12px;
  background-color: #f1f1f1;
  border-radius: 5px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

li:hover {
  background-color: #e9ecef;
}

.search-results {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.search-results ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.search-results li {
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  margin-bottom: 5px;
  cursor: pointer;
}

.search-results li:hover {
  background-color: #f1f1f1;
}
</style>
