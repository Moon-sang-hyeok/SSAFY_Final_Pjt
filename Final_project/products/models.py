from django.db import models

# Create your models here.

class SavingProducts(models.Model):
    # baseList 값
    fin_prdt_cd = models.CharField(max_length=20)  # 금융상품 코드
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    fin_co_no = models.CharField(max_length=20)    # 금융회사 코드
    join_way = models.CharField(max_length=20)     # 가입방법
    spcl_cnd = models.TextField()                  # 우대조건
    join_member = models.TextField()              # 가입대상
    kor_co_nm = models.CharField(max_length=20)   # 금융회사명
    max_limit = models.IntegerField(null=True)

    # optionList 값
    intr_rate = models.FloatField(max_length=20)  # 저축금리
    intr_rate2 = models.FloatField(max_length=20)  # 최고 우대금리
    intr_rate_type_nm = models.CharField(max_length=20) # 저축 금리 유형명
    rsrv_type_nm = models.CharField(max_length=20)   # 적립 유형명
    save_trm = models.IntegerField()        # 저축기간
    class Meta:
        unique_together = ('fin_prdt_cd', 'fin_co_no','fin_prdt_nm','save_trm')  # 고유 제약 조건 추가

    def __str__(self):
        return f"{self.fin_prdt_nm} ({self.fin_prdt_cd})"



class DepositProducts(models.Model):
    # baseList 값
    fin_prdt_cd = models.CharField(max_length=20)  # 금융상품 코드
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    fin_co_no = models.CharField(max_length=20)    # 금융회사 코드
    join_way = models.CharField(max_length=20)     # 가입방법
    spcl_cnd = models.TextField()                  # 우대조건
    join_member = models.TextField()              # 가입대상
    kor_co_nm = models.CharField(max_length=20)   # 금융회사명
    max_limit = models.IntegerField(null=True)
    # optionList 값
    intr_rate = models.FloatField(max_length=20)  # 저축금리
    intr_rate2 = models.FloatField(max_length=20)  # 최고 우대금리
    intr_rate_type_nm = models.CharField(max_length=20) # 저축 금리 유형명
    save_trm = models.IntegerField()        # 저축기간
    class Meta:
        unique_together = ('fin_prdt_cd', 'fin_co_no','fin_prdt_nm','save_trm')  # 고유 제약 조건 추가

    def __str__(self):
        return f"{self.fin_prdt_nm} ({self.fin_prdt_cd})"
    


