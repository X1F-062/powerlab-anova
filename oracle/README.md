# oracle/
- `gpower_vectors.csv` (SİZ ÜRETİN): G*Power GUI'den ≥30 vektör.
  Başlık: `id,f,alpha,power,groups,n_total,actual_power,critical,df1,df2,ncp,screenshot`
  Sınır vektörleri şart: f çok küçük/büyük, α uçları, güç çok yüksek/düşük, k=2 ve k>3, geçersiz girdi (ayrı dosya).
  Ekran görüntüleri `oracle/screens/` altında.
- `scale_vectors.csv`: `python tests/gen_scale_vectors.py` (scipy ile 960 vektör; G*Power DEĞİL).
