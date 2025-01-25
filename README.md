# Dinamik ve Mukayeseli Hisse Senedi Analiz Chatbotu

Bu proje, kullanıcıların JSON formatında yükledikleri hisse senedi verileri üzerinde dinamik analiz yapmalarını sağlayan bir chatbot uygulamasıdır. Uygulama, **Streamlit** arayüzü üzerinden çalışır ve kullanıcıdan gelen sorulara göre JSON verilerini filtreler, analiz eder ve uygun cevaplar üretir. Ayrıca **LLM (Llama3)** ile doğal dil işleme yetenekleri entegre edilmiştir.

---

## Özellikler

1. **Dinamik JSON İşleme**:
   - Kullanıcılar farklı JSON dosyaları yükleyebilir.
   - Yüklenen verilerde anahtar kelimelere dayalı dinamik filtreleme yapılır.

2. **Doğal Dil Soruları**:
   - Kullanıcıların soruları Türkçe olarak işlenir.
   - Sorulara göre analiz yapılır ve cevaplar detaylı bir şekilde Türkçe üretilir.

3. **Pandas Tabanlı Veri Analizi**:
   - Tarih bazlı filtreleme.
   - Fiyat karşılaştırmaları.
   - Fiyat farkı hesaplamaları gibi birçok işlev sunar.

4. **Model Entegrasyonu**:
   - Llama3 kullanılarak dinamik ve anlamlı cevaplar üretilir.
   - Modelin performansı, cache mekanizması ile optimize edilmiştir.

5. **Cache Mekanizması**:
   - Daha önce sorulmuş sorular için cevaplar saklanır ve hızlı erişim sağlanır.

---

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki araçlar ve kütüphanelere ihtiyacınız var:

- **Python 3.8+**
- **Streamlit**
- **Pandas**
- **LangChain Community Llama3**
- **Cachetools**

Gerekli paketleri yüklemek için:
```bash
pip install streamlit pandas langchain-community cachetools
```

---

## Projenin Çalıştırılması

1. **Proje Klasörünü İndirin**:
   ```bash
   git clone <repository-url>
   cd project-folder
   ```

2. **Uygulamayı Çalıştırın**:
   ```bash
   streamlit run app.py
   ```

3. **JSON Dosyasını Yükleyin**:
   - Arayüzde verilen alana JSON formatında hisse senedi verinizi yükleyin.

4. **Sorularınızı Sorun**:
   - "AGESA'nın tüm kapanış fiyatlarını listele."
   - "AGESA ve AKBNK hisselerinin fiyat farklarını hesapla."
   - "2024-05-09 tarihindeki kapanış fiyatlarını karşılaştır."

5. **Sonuçları İnceleyin**:
   - Uygulama, yüklediğiniz veriler ve sorularınıza göre analiz sonuçlarını görüntüler.

---

## JSON Veri Yapısı

Uygulama, örnek bir JSON veri formatını aşağıdaki gibi kabul eder:

```json
{
  "GetIMKBStocksClosePriceResult": [
    {
      "Stock_Code": "AGESA",
      "Close_Price": 87.25,
      "Date": "/Date(1713984000000+0300)/"
    },
    {
      "Stock_Code": "AKBNK",
      "Close_Price": 34.75,
      "Date": "/Date(1713984000000+0300)/"
    }
  ]
}
```

---

## Örnek Sorular

- "AGESA'nın kapanış fiyatlarını sırala."
- "AGESA ve AKBNK fiyat farklarını hesapla."
- "2024-05-09 tarihinde en yüksek kapanış yapan hisse nedir?"
- "Son 3 ayda hangi hisse daha yüksek kapanış yaptı?"

---

## Geliştirici Notları

1. **Dinamik Filtreleme**:
   - Kullanıcının sorularında yer alan anahtar kelimeler otomatik olarak algılanır ve JSON verisi filtrelenir.

2. **Model Performansı**:
   - Modelin yanıt süresi, `time.perf_counter()` ile ölçülür ve kullanıcıya gösterilir.

3. **Veri İşleme**:
   - Pandas kütüphanesi, verilerin düzenlenmesi, analiz edilmesi ve görselleştirilmesi için etkin şekilde kullanılmıştır.

---

## Katkıda Bulunma

Projeye katkıda bulunmak isterseniz, lütfen bir `pull request` gönderin veya bir `issue` açarak sorunuzu iletin. Geri bildirimleriniz memnuniyetle karşılanır!

---

## Lisans

Bu proje açık kaynaklıdır ve [MIT Lisansı](LICENSE) altında sunulmaktadır.

