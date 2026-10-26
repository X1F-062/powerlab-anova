# SPEC: tek yönlü ANOVA güç analizi (kabul kriterleri Gherkin)

Kapsam: F testi, tek yönlü ANOVA, sabit etkiler, omnibus. Modlar: a-priori, post-hoc.
Durum etiketleri: **[MATEMATİK]** standart formül; **[GÖZLENDİ REA-xx]** gerçek araçta kanıtlı;
**[HİPOTEZ]** henüz kanıtsız. Yazım oturumu (Oturum 2) yalnızca bu dosyayı görür.
Gizli doğrulama setinin bir kısmı bu dosyada YOKTUR; bunu kasıtlı olarak tutun.

## Model [MATEMATİK]
df1=k-1, df2=N-k, λ=f²·N, Fcrit = merkezi F'nin (1-α) kantili, güç = P(F'(df1,df2,λ) > Fcrit).
f = √(η²/(1-η²)); ortalamalardan f = σ_m/σ (eşit n: σ_m² = Σ(μ_i-μ̄)²/k).
A priori: koşulu sağlayan en küçük **toplam** N (güç N'de monoton artar).

## Senaryolar
```gherkin
Feature: A priori örneklem büyüklüğü
  Scenario: Orta etki, %80 güç  [HİPOTEZ → REA-01 ile doğrulanacak]
    Given f=0.25, alpha=0.05, power=0.80, groups=3
    Then n_total = 159 and n_total % 3 = 0
    And actual_power ≈ 0.8049 (4 hane)
    And df1 = 2 and df2 = 156 and ncp ≈ 9.9375

  Scenario: Orta etki, %95 güç  [HİPOTEZ → REA-01]
    Given f=0.25, alpha=0.05, power=0.95, groups=3
    Then n_total = 252 and actual_power ≈ 0.9515

  Scenario: Minimalite  [MATEMATİK + HİPOTEZ REA-01]
    Given herhangi geçerli girdi
    Then güç(n_total) >= hedef and güç(n_total - 3) < hedef

Feature: Post hoc güç
  Scenario: Doğrudan hesap  [MATEMATİK]
    Given f=0.25, alpha=0.05, n_total=159, groups=3
    Then actual_power ≈ 0.8049

Feature: Etki büyüklüğü girişi  [MATEMATİK]
  Scenario: eta2 dönüşümü
    Given eta2=0.0588235 Then f ≈ 0.25
  Scenario: Ortalamalar
    Given means=[-1,0,1], sd=1 Then f = sqrt(2/3)

Feature: Geçersiz girdi  [HİPOTEZ; sınırlar REA-04/05/06 ile belirlenecek]
  Scenario Outline: Hata sözleşmesi
    Given <girdi> Then çıktı {"error":...} ve çıkış kodu != 0
    Examples: f<=0 | alpha<=0 veya >=1 | power<=0 veya >=1 | groups<2 | n_total<=k | mode bilinmiyor
```

## Açık sorular (dürüstçe)
Bkz. LEDGER.md'de durumu "BEKLİYOR" olan tüm REA maddeleri: eşitlikte >=/>, N tavanı ve f=0.001 davranışı,
minimum N, alan aralıkları, ekran hassasiyeti, çok büyük N sapması.
