<template>
  <div class="currency-converter">
    

    <div class="content-container">
      <!-- 왼쪽: 환율 계산기 -->
      <div class="converter-container">
        <div class="converter-form">
          <br>
          <h1 class="title">환율 계산기</h1>
          <div class="form-group">
            <label for="currency">통화 선택:</label>
            <select v-model="selectedCurrency" id="currency" @change="convertCurrency">
              <option v-for="(rate, key) in exchangeRates" :key="key" :value="key">{{ key }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="amount">금액 입력 (원화 또는 선택한 통화):</label>
            <input type="number" v-model="amount" id="amount" placeholder="금액을 입력하세요" @input="convertCurrency" />
          </div>

          <div class="form-group">
            <label for="converted-currency">변환할 통화:</label>
            <select v-model="convertedCurrency" id="converted-currency" @change="convertCurrency">
              <option v-for="(rate, key) in exchangeRates" :key="key" :value="key">{{ key }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="converted-amount">변환된 금액:</label>
            <input type="text" :value="convertedAmount" id="converted-amount" disabled />
          </div>
        </div>
      </div>

      <!-- 오른쪽: 현재 환율 상태 -->
      <div v-if="Object.keys(exchangeRates).length > 0" class="exchange-rate-container">
        <h1 class="title">현재 환율 상태</h1>
        <table>
          <thead>
            <tr>
              <th>통화</th>
              <th>환율 (원화 기준)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(rate, currency) in exchangeRates" :key="currency">
              <td>{{ currency }}</td>
              <td>{{ rate }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'CurrencyConverter',
  setup() {
    const exchangeRates = ref({});
    const selectedCurrency = ref('USD');
    const convertedCurrency = ref('KRW');
    const amount = ref(0);
    const convertedAmount = ref(0);

    const fetchExchangeRates = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/exchange/api/exchange-rates/');
        exchangeRates.value = response.data;
        convertCurrency();
      } catch (error) {
        console.error('환율 정보를 가져오는 데 실패했습니다.', error);
      }
    };

    const convertCurrency = () => {
      const selectedRate = parseFloat(exchangeRates.value[selectedCurrency.value].replace(',', ''));
      const convertedRate = parseFloat(exchangeRates.value[convertedCurrency.value].replace(',', ''));

      if (amount.value && !isNaN(amount.value) && !isNaN(selectedRate) && !isNaN(convertedRate)) {
        if (selectedCurrency.value === 'KRW') {
          convertedAmount.value = (amount.value / selectedRate * convertedRate).toFixed(2);
        } else {
          convertedAmount.value = (amount.value * selectedRate / convertedRate).toFixed(2);
        }
      } else {
        convertedAmount.value = 0;
      }
    };

    onMounted(() => {
      fetchExchangeRates();
    });

    return {
      exchangeRates,
      selectedCurrency,
      convertedCurrency,
      amount,
      convertedAmount,
      convertCurrency,
    };
  },
};
</script>

<style scoped>
.currency-converter {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px;
  background-color: #f4f4f9;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  text-align: left;
  margin-bottom: 20px;
}

.content-container {
  display: flex;
  justify-content: space-between;
  gap: 40px;
  
}

.converter-container {
  flex: 0.6;
  display: flex;
  flex-direction: column;
  max-width: 1000px;
}

.exchange-rate-container {
  flex: 0.4;
  padding-top: 20px;
  border-left: 2px solid #ddd;
  padding-left: 20px;
  max-width: 1000px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #444;
  margin-bottom: 8px;
}


select {
  width: 70%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  color: #555;
  background-color: #fff;
  transition: border 0.3s;

}

input {
  width: 65%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  color: #555;
  background-color: #fff;
  transition: border 0.3s;

}

input:focus,
select:focus {
  border-color: #4CAF50;
  outline: none;
}

input::placeholder {
  color: #bbb;
}

input:disabled {
  background-color: #f9f9f9;
  border: 2px solid #ddd;
}

.exchange-rate-container table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.exchange-rate-container th,
.exchange-rate-container td {
  padding: 12px;
  text-align: center;
  border: 1px solid #ddd;
  font-size: 16px;
}

.exchange-rate-container th {
  background-color: #f4f4f9;
  font-weight: 600;
}

.exchange-rate-container td {
  background-color: #fff;
}

.exchange-rate-container tr:hover {
  background-color: #f1f1f1;
}
</style>
