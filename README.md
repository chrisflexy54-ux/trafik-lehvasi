# Trafik Levhası Tespiti... YOLO26 + SAHI

> **Trafik Levhası Tespiti** · Nesne Tespiti · Bilgisayarlı Görü · Gerçek Zamanlı
> NTEKO CHRIS EMERY NGUESSAN — No: 223908708

Yol kenarına yerleştirilmiş bir gözetleme kamerasının görüntü akışından trafik
levhalarının **gerçek zamanlı** ve otomatik tespitini yapan bir sistem.
**YOLO26** modeli (Ultralytics, Eylül 2025) ve uzaktaki küçük nesneleri tespit
etmek için **SAHI** kütüphanesi üzerine kuruludur.

---

## 1. Projenin Amacı

Yol kenarına konumlandırılmış bir kameranın görüntü akışında her türlü trafik
levhasını (hız sınırı, geçiş üstünlüğü, yasaklama, tehlike, yön, trafik ışıkları…)
gerçek trafik gözetleme koşullarını simüle ederek otomatik olarak tanıyabilen
bir model tasarlamak ve eğitmek.

## 2. Kullanılan Teknolojiler

| Bileşen | Görev |
|---------|-------|
| **YOLO26** (Ultralytics) | Gerçek zamanlı nesne tespiti, **NMS'siz** uçtan uca çıkarım, **MuSGD** optimizasyonu, küçük nesneler için ProgLoss + STAL |
| **SAHI** (Slicing Aided Hyper Inference) | Küçük/uzak levhaları tespit etmek için örtüşen parçalara (tile) bölme |
| **OpenCV** | Video yakalama, etiketlerin çizimi, görüntü kaydetme |
| **PyTorch** | Derin öğrenme arka ucu |
| **Roboflow Universe** | YOLO formatında önceden etiketlenmiş açık veri kümeleri (gündüz/gece/yağmur/kar) |

## 3. Benzer Projelere Göre Avantajları

- **YOLO26**, YOLO ailesinin en güncel sürümü: YOLO11'e kıyasla CPU üzerinde
  **%43'e** varan çıkarım hızı artışı → gömülü/gözetleme kameraları için uygun.
- **NMS'siz çıkarım**: maliyetli bir son işleme adımını ortadan kaldırır,
  gecikmeyi azaltır gerçek zaman için belirleyici.
- **SAHI**: klasik tespitin kaçırdığı levhaları yakalar (aşağıdaki karşılaştırmaya
  bakınız) → gerçek koşullarda çok daha sağlam.
- **Dayanıklılık**: çok koşullu veri kümeleri (gündüz, gece, yağmur, kar, bulanıklık,
  farklı açılar) ile sahada sürprizlerden kaçınma.

## 4. Kod Mimarisi

```
trafik-levhasi/
├── run_demo.py            # uçtan uca demo (eğitimsiz) → ekran görüntüleri
├── requirements.txt
├── configs/data.yaml      # sınıflar + veri kümesi yolları
├── src/
│   ├── config.py          # sabitler + yedek geçiş YOLO26 → YOLO11 → YOLOv8
│   ├── model_utils.py     # sağlam model yükleme
│   ├── prepare_data.py    # Roboflow Universe veri kümelerini indirme/birleştirme
│   ├── train.py           # YOLO26 eğitimi (MuSGD, erken durdurma, eğriler)
│   ├── evaluate.py        # metrikler: mAP50, mAP50-95, kesinlik, duyarlılık
│   ├── predict_image.py   # görüntü üzerinde klasik çıkarım
│   ├── predict_sahi.py    # görüntü üzerinde SAHI (slicing) çıkarımı
│   ├── realtime_camera.py # gerçek zamanlı webcam tespiti (yol kamerası senaryosu)
│   └── compare.py         # klasik vs SAHI karşılaştırma montajı
├── samples/               # örnek görüntüler (gerçek yol sahneleri)
└── outputs/               # etiketli sonuçlar + rapor için ekran görüntüleri
```

## 5. Kurulum

```bash
pip install -r requirements.txt
```

(Geliştirme makinesinde hâlihazırda mevcut: ultralytics 8.4, opencv 4.10, torch 2.8;
`sahi` requirements üzerinden kurulur.)

## 6. Projenin Çalıştırılması

```bash
# Anında demo (YOLO26'yı indirir, etiketli görüntüleri üretir):
python run_demo.py

# Rapor için klasik vs SAHI karşılaştırması:
python src/compare.py stop_rue1

# Webcam ile gerçek zamanlı tespit ('q' çıkış, 's' ekran görüntüsü):
python src/realtime_camera.py

# Tam eğitim hattı:
export ROBOFLOW_API_KEY="api_anahtariniz"
python src/prepare_data.py     # 1. veri kümesi
python src/train.py            # 2. YOLO26 eğitimi
python src/evaluate.py         # 3. metrikler
python src/predict_sahi.py samples/stop_rue1.jpg   # 4. SAHI çıkarımı
```

## 7. İlerleme Durumu (vize öncesi)

| Aşama | Durum |
|-------|-------|
| Pipeline mimarisi ve teknik seçimler (YOLO26 + SAHI) | ✅ Tamamlandı |
| Klasik + SAHI çıkarım scriptleri çalışır durumda | ✅ Tamamlandı |
| Gerçek zamanlı webcam tespiti | ✅ Tamamlandı (script hazır) |
| Görsel üreten uçtan uca demo | ✅ Tamamlandı |
| Klasik vs SAHI karşılaştırması doğrulandı | ✅ Tamamlandı |
| Eğitim + değerlendirme scriptleri | ✅ Kodlandı, çalıştırmaya hazır |
| Roboflow çok koşullu veri kümesinin oluşturulması/birleştirilmesi | 🔜 Başlatılacak (API anahtarı) |
| GPU'da nihai eğitim + nihai metrikler | 🔜 Sonraki adım |

**Mevcut doğrulama**: önceden eğitilmiş YOLO26 modeli, DUR levhalarını ve trafik
ışıklarını hâlihazırda doğal olarak tespit ediyor. SAHI ölçülebilir katkısını
gösterdi: `stop_rue1` üzerinde klasik yöntemde **3 nesne** tespit edilirken
SAHI ile **12 nesne** (uzaktaki birçok DUR levhası yakalandı); `feux_ville`
üzerinde **9 → 28**.

`outputs/comparaison_stop_rue1.jpg` ve `outputs/comparaison_feux_ville.jpg`
dosyalarına bakınız.
