import streamlit as st
import pandas as pd
import time
from langchain_community.llms import Ollama
from cachetools import LRUCache
from datetime import datetime

# Initialize the Llama3 model
cached_llm = Ollama(model="llama3:latest")

# Cache mekanizması
cache = LRUCache(maxsize=100)

# Dinamik JSON verisi filtreleme fonksiyonu
def filter_data_based_on_question(data, question):
    # Genel bir anahtar kelime ve değer analizi yapılarak filtreleme yapılır
    keywords = ["fiyat", "tarih", "yüksek", "düşük", "ortalama", "karşılaştır"]
    for keyword in keywords:
        if keyword in question:
            # Örneğin "fiyat" ile ilgili sorular
            if "fiyat" in question:
                if "yüksek" in question:
                    return data.nlargest(5, "Close_Price")  # En yüksek fiyatları döndür
                elif "düşük" in question:
                    return data.nsmallest(5, "Close_Price")  # En düşük fiyatları döndür
                else:
                    return data  # Tüm fiyatları döndür
            elif "tarih" in question:
                date_filter = question.split()[-1]  # Kullanıcıdan bir tarih alındığı varsayılır
                return data[data["Date"] == date_filter]
    return data  # Varsayılan olarak tüm veriyi gönder

# Analyze question with the model
def analyze_question_with_model(question, data):
    start_time = time.perf_counter()  # İşlem başlangıcı
    context = data.to_json(orient='records', force_ascii=False)  # JSON formatında veriyi hazırlama
    prompt = (
        f"Bağlam (JSON Verisi): {context}\n"
        f"Soru: {question}\n"
        f"Cevapları sadece Türkçe olarak ver ve soruda belirtilen tüm karşılaştırmaları yap. "
        f"Her bir hisse için tarih, kapanış fiyatı gibi detayları sıralı bir şekilde ver. "
        f"Eğer fiyat farkı ya da karşılaştırma isteniyorsa, ilgili tüm hesaplamaları yap ve açıkça belirt."
    )
    response = cached_llm(prompt, options={"language": "tr", "max_tokens": 500, "temperature": 0.7})
    end_time = time.perf_counter()  # İşlem bitişi
    elapsed_time = end_time - start_time  # Geçen süre

    if isinstance(response, str):
        return response, elapsed_time
    return response.get("answer", "Üzgünüm, model soruya uygun bir cevap veremedi."), elapsed_time

# Cache mekanizmasını kullanarak analiz yapma
def analyze_question_with_cache(question, data):
    if question in cache:
        return cache[question], 0  # Cache'den çek, zaman sıfır olarak gösterilir

    filtered_data = filter_data_based_on_question(data, question)  # Soruya göre filtrele
    context = filtered_data.to_json(orient='records', force_ascii=False)
    answer, elapsed_time = analyze_question_with_model(question, filtered_data)
    cache[question] = answer  # Cache'e kaydet
    return answer, elapsed_time

# Pandas ile ek analizler
def calculate_price_difference(data, stock1, stock2):
    data1 = data[data["Stock_Code"] == stock1]
    data2 = data[data["Stock_Code"] == stock2]
    merged = pd.merge(data1, data2, on="Date", suffixes=(f"_{stock1}", f"_{stock2}"))
    merged["Price_Difference"] = merged[f"Close_Price_{stock1}"] - merged[f"Close_Price_{stock2}"]
    return merged[["Date", f"Close_Price_{stock1}", f"Close_Price_{stock2}", "Price_Difference"]]

def compare_stocks_by_date(data, date, stocks):
    filtered_data = data[(data["Date"] == date) & (data["Stock_Code"].isin(stocks))]
    return filtered_data

# Streamlit interface
st.title("Dinamik ve Mukayeseli Hisse Senedi Analiz Chatbotu")

uploaded_file = st.file_uploader("Hisse senedi verilerinizi içeren JSON dosyasını yükleyin (örn. GetIMKBStocksClosePriceResult)")
if uploaded_file:
    raw_data = pd.read_json(uploaded_file)
    st.write("Yüklenen Ham JSON Verisi:", raw_data)  # Display raw JSON structure

    # Extract and process data if structure is correct
    if "GetIMKBStocksClosePriceResult" in raw_data.columns:
        stock_data = pd.DataFrame(raw_data["GetIMKBStocksClosePriceResult"].tolist())

        # Clean and format the data
        stock_data["Date"] = stock_data["Date"].apply(lambda x: datetime.utcfromtimestamp(int(x[6:16])).strftime('%Y-%m-%d'))
        st.write("İşlenmiş Hisse Senedi Verisi:", stock_data)

        # Input for questions
        question = st.text_input("Hisse senetleri hakkında bir soru sorun:")
        if question:
            answer, elapsed_time = analyze_question_with_cache(question, stock_data)
            st.write("Cevap:", answer)
            st.write(f"Yanıt süresi: {elapsed_time:.2f} saniye")

            # Eğer pandas ile ek analiz yaptıysan:
            if "fiyat farkı" in question:
                stocks_to_compare = ["AGESA", "AKBNK"]  # Örnek karşılaştırma hisseleri
                result = calculate_price_difference(stock_data, stocks_to_compare[0], stocks_to_compare[1])
                st.write(f"{stocks_to_compare[0]} ve {stocks_to_compare[1]} Fiyat Farkları:", result)
            elif "tarih" in question:
                selected_date = "2024-05-09"  # Örnek tarih, sorudan alınabilir
                stocks = ["AGESA", "AKBNK"]
                result = compare_stocks_by_date(stock_data, selected_date, stocks)
                st.write(f"{selected_date} Tarihindeki Hisse Karşılaştırması:", result)
    else:
        st.error("Geçersiz JSON yapısı. 'GetIMKBStocksClosePriceResult' anahtarı bulunamadı.")
