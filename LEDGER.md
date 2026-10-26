# LEDGER: kanıt defteri
Etiketler: [DOK] kılavuz/makale · [REA] binary kanıtı (fonksiyon adresi veya dize ref.) · [AJAN] kanıtsız çıkarım.
**Puan yalnızca [REA] satırlarına verilir.** Aşağıda hiçbir satır henüz [REA] değildir; hepsini siz GUI + REA ile doldurun.
Her satıra: girdi, G*Power'ın gösterdiği çıktı, ekran görüntüsü yolu, REA'da fonksiyon adresi/dize, tarih.

| ID | Soru | Mevcut durum | Etiket | Kanıt (TODO) |
|----|------|--------------|--------|--------------|
| REA-01 | Toplam N k'nın katına yuvarlanıyor mu? | Hipotez: evet. Ham minimum 158 ve 251; hatırlanan G*Power 159 ve 252 (ikisi de 3'ün katı) | [AJAN] | GUI ss + yuvarlama kodunun adresi |
| REA-02 | Güç tam hedefe eşitse ≥ mı > mı? | Varsayım ≥ | [AJAN] | hedefe tam eşit güç üreten vektör bulun |
| REA-03 | "Actual power" kaç hane, yuvarlama mı kesme mi? | Varsayım 4 hane | [AJAN] | ss |
| REA-04 | Arama başlangıcı, adım, iterasyon tavanı; f=0.001 | Bilinmiyor (motorda 10^7 tavanı varsayım) | [AJAN] | f=0.001, 0.0001 denemeleri |
| REA-05 | Minimum geçerli toplam N ve k | Varsayım N≥k+1, k≥2 | [AJAN] | sınır girdileri |
| REA-06 | f, α, güç kabul aralıkları ve sınır dışı tepki | Varsayım (0,∞), (0,1), (0,1) | [AJAN] | sınır girdileri |
| REA-07 | Çok büyük N / λ'da sapma | Bilinmiyor | [AJAN] | N=10^5..10^7 |
| REA-08 | Kesirli N'ye karşı yukarı yuvarlama (pwr/statsmodels farkı) | scipy kesirli N verir; fark açıklanmalı | [AJAN] | 960 ölçek vektörü + GUI karşılaştırması |
| DOK-01 | df1=k-1, df2=N-k, λ=f²N, güç tanımı | Standart formül; G*Power makalelerinde de aynı | [DOK] | Faul vd. 2007 |
| DOK-02 | f ↔ η² dönüşümü | Standart | [DOK] | Cohen 1988 |

## Bu repoda bağımsız olarak doğrulananlar (G*Power'a dair DEĞİL, matematiğe dair)
- Motor, ncf'ten farklı bir yolla (Poisson-beta karışımı) 1e-9 içinde eşleşti; 100k Monte Carlo ile 5σ içinde eşleşti.
- f=.25, α=.05, k=3: ham asgari N = 158 (0.8022) ve 251 (0.9507); k'nın katı 159 (0.8049) ve 252 (0.9515).
