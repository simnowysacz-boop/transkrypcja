# 🎙️ Transkrypcja Facebook/YouTube (PL)

Aplikacja webowa do automatycznej transkrypcji materiałów wideo z Facebooka i YouTube w języku polskim, wykorzystująca model Whisper AI.

## 📦 Dostępne Wersje

### 🖥️ Wersja Lokalna (`app.py`)
- ✅ **Całkowicie darmowa**
- ✅ Najwyższa jakość transkrypcji
- ✅ Brak limitów użycia
- ⚠️ Wymaga instalacji Python, FFmpeg, torch
- ⚠️ Wymaga mocniejszego komputera

### ☁️ Wersja API (`app_api.py`)  
- ✅ **Działa w chmurze** (Streamlit Cloud)
- ✅ Szybka transkrypcja
- ✅ Nie wymaga instalacji dla użytkowników
- ✅ Dostęp przez link w przeglądarce
- 💰 Kosztuje: $0.006/minutę audio (~2.4 PLN/godzina)

## 🚀 Funkcje

- ✅ Pobieranie audio z linków Facebook/YouTube
- ✅ Automatyczna transkrypcja w języku polskim
- ✅ Wybór modelu Whisper (tiny → large)
- ✅ Wyświetlanie segmentów z czasami
- ✅ Eksport transkrypcji do pliku TXT
- ✅ Prosty system uwierzytelniania
- ✅ Intuicyjny interfejs Streamlit

## 📋 Wymagania

- Python 3.8+
- FFmpeg zainstalowany w systemie

### Instalacja FFmpeg (Windows)

1. Pobierz FFmpeg z: https://www.gyan.dev/ffmpeg/builds/
2. Rozpakuj archiwum
3. Dodaj folder `bin` do zmiennej środowiskowej PATH
4. Sprawdź instalację: `ffmpeg -version`

Lub użyj Chocolatey:
```powershell
choco install ffmpeg
```

## 🛠️ Instalacja

1. Sklonuj repozytorium lub pobierz pliki
2. Zainstaluj zależności:

```powershell
pip install -r requirements.txt
```

## ⚙️ Konfiguracja

Zmień hasło w pliku `app.py`:

```python
HASLO = "TAJNEMASLO2025"  # Zmień to hasło na własne
```

## 🎯 Uruchomienie

```powershell
streamlit run app.py
```

Aplikacja uruchomi się w przeglądarce pod adresem: `http://localhost:8501`

## 📖 Instrukcja użycia

1. **Zaloguj się** używając skonfigurowanego hasła
2. **Wybierz model Whisper** w menu bocznym (zalecany: `medium`)
3. **Wklej link** do filmu z Facebooka lub YouTube
4. **Kliknij "Rozpocznij transkrypcję"** i poczekaj
5. **Pobierz wyniki** jako plik TXT lub skopiuj tekst

## 🤖 Modele Whisper

| Model  | Rozmiar | Szybkość | Dokładność | Rekomendacja       |
|--------|---------|----------|------------|--------------------|
| tiny   | 39 MB   | ⚡⚡⚡⚡⚡    | ⭐⭐         | Testy              |
| base   | 74 MB   | ⚡⚡⚡⚡     | ⭐⭐⭐        | Szybkie przetwarzanie |
| small  | 244 MB  | ⚡⚡⚡      | ⭐⭐⭐⭐       | Dobry kompromis    |
| medium | 769 MB  | ⚡⚡       | ⭐⭐⭐⭐⭐      | ✅ **Zalecany (PL)** |
| large  | 1550 MB | ⚡        | ⭐⭐⭐⭐⭐      | Najwyższa jakość   |

## 🌐 Wdrożenie (Deployment)

### Streamlit Cloud (Darmowy)

1. Stwórz repozytorium GitHub z plikami projektu
2. Wejdź na https://share.streamlit.io/
3. Połącz repozytorium i wybierz `app.py`
4. Aplikacja będzie dostępna publicznie

### Lokalne uruchomienie produkcyjne

```powershell
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🔒 Bezpieczeństwo

⚠️ **WAŻNE:** Obecna implementacja używa prostego hasła hardkodowanego w kodzie. Jest to odpowiednie dla:
- Użytku osobistego
- Prototypów
- Małych zespołów

Dla aplikacji produkcyjnych rozważ:
- Zmienne środowiskowe dla hasła
- Proper authentication (OAuth, JWT)
- Szyfrowanie haseł
- Uwierzytelnianie wielopoziomowe

## 📝 Struktura projektu

```
Transkrypca_YT/
├── app.py              # Główna aplikacja Streamlit
├── requirements.txt    # Zależności Python
└── README.md          # Dokumentacja
```

## 🐛 Rozwiązywanie problemów

### "Błąd pobierania audio"
- Sprawdź czy link jest prawidłowy i publicznie dostępny
- Niektóre materiały mogą być chronione przez właściciela

### "Błąd transkrypcji"
- Upewnij się że FFmpeg jest zainstalowany
- Sprawdź czy masz wystarczająco RAM (model large wymaga ~10GB)
- Spróbuj mniejszego modelu

### Wolna transkrypcja
- Użyj mniejszego modelu (small zamiast medium)
- Większe modele wymagają GPU dla szybszego przetwarzania

## 💡 Wskazówki

- Model `medium` zapewnia najlepszy balans dla języka polskiego
- Pierwsza transkrypcja zajmie więcej czasu (pobieranie modelu)
- Krótsze filmy (<10 min) przetwarzają się szybciej
- GPU znacznie przyspiesza transkrypcję

## 📄 Licencja

MIT License - możesz swobodnie używać i modyfikować aplikację.

## 🤝 Wsparcie

W razie problemów sprawdź:
- Dokumentację Whisper: https://github.com/openai/whisper
- Dokumentację Streamlit: https://docs.streamlit.io/
- Dokumentację yt-dlp: https://github.com/yt-dlp/yt-dlp

---

Stworzono z ❤️ używając OpenAI Whisper i Streamlit
