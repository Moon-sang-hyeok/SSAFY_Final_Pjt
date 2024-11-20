<template>
    <div class="nearby-banks">
      <h1>주변 은행 검색</h1>
  
      <!-- Kakao 지도 표시 영역 -->
      <div id="map" style="width: 100%; height: 500px;"></div>
  
      <!-- 선택된 위치 출력 -->
      <div v-if="selectedLocation">
        <h2>선택된 위치</h2>
        <p>위도: {{ selectedLocation.lat }}</p>
        <p>경도: {{ selectedLocation.lng }}</p>
      </div>
  
      <!-- 근처 은행 목록 -->
      <div v-if="banks.length > 0">
        <h2>근처 은행</h2>
        <ul>
          <li v-for="(bank, index) in banks" :key="index">
            <p>{{ bank.name }}</p>
            <p>{{ bank.address }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted, ref } from 'vue';
  import axios from 'axios';
  
  export default {
    name: 'NearbyBanks',
    setup() {
      const map = ref(null);
      const selectedLocation = ref(null);
      const banks = ref([]);
  
      // Kakao Maps API 지도 객체 생성
      onMounted(() => {
        window.kakao.maps.load(() => {
          const container = document.getElementById('map');
          const options = {
            center: new window.kakao.maps.LatLng(37.5665, 126.9780), // 서울 중심
            level: 3, // 지도 확대 수준
          };
          map.value = new window.kakao.maps.Map(container, options);
  
          // 지도 클릭 시 위치 정보 저장
          window.kakao.maps.event.addListener(map.value, 'click', function (mouseEvent) {
            const latLng = mouseEvent.latLng;
            selectedLocation.value = {
              lat: latLng.getLat(),
              lng: latLng.getLng(),
            };
            fetchNearbyBanks(latLng.getLat(), latLng.getLng()); // 선택된 위치에서 근처 은행 찾기
          });
        });
      });
  
      // 근처 은행 검색 API 호출
      const fetchNearbyBanks = async (lat, lng) => {
        try {
          const response = await axios.get('http://localhost:8000/banks/nearby-banks', {
            params: {
              lat: lat,
              lng: lng,
            },
            headers: {
        Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
      },
          });

          console.log(response.data); // 응답 데이터 확인
          

          // 응답 받은 은행 데이터 처리
          banks.value = response.data;
        } catch (error) {
          console.error('은행 정보를 가져오는 데 실패했습니다.', error);
        }
      };
  
      return {
        selectedLocation,
        banks,
      };
    },
  };
  </script>
  
  <style scoped>
.nearby-banks {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

#map {
  width: 100%;
  height: 500px;
  margin-bottom: 20px;
}

h1, h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f8f8f8;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

li p {
  margin: 5px 0;
}
</style>