# 🚀 Instrukcja Wdrożenia na Streamlit Cloud

## 📋 Wymagania wstępne

1. Konto GitHub (darmowe)
2. Konto OpenAI z aktywnym API key
3. Konto Streamlit Cloud (darmowe)

---

## 1️⃣ Przygotowanie Repozytorium GitHub

### Stwórz nowe repozytorium:
1. Wejdź na https://github.com/new
2. Nazwa: `transkrypcja-yt` (lub dowolna)
3. Ustaw jako **Public** (wymagane dla darmowego Streamlit Cloud)
4. ✅ Zaznacz "Add a README file"
5. Kliknij **Create repository**

### Wyślij kod na GitHub:

```powershell
# W folderze projektu wykonaj:
cd C:\Users\win11\Documents\Projekty\Transkrypca_YT

# Inicjalizuj Git
git init

# Dodaj wszystkie pliki
git add .

# Pierwszy commit
git commit -m "Initial commit - Aplikacja transkrypcji"

# Połącz z GitHub (ZAMIEŃ na swój URL!)
git remote add origin https://github.com/TWOJA_NAZWA/transkrypcja-yt.git

# Wyślij kod
git branch -M main
git push -u origin main
```

**⚠️ WAŻNE:** Plik `.gitignore` chroni przed wysłaniem:
- Klucza API (`secrets.toml`)
- Plików tymczasowych
- Pobranych plików audio

---

## 2️⃣ Uzyskanie Klucza API OpenAI

1. Wejdź na https://platform.openai.com/
2. Zaloguj się lub zarejestruj
3. Przejdź do **API keys**: https://platform.openai.com/api-keys
4. Kliknij **+ Create new secret key**
5. Nazwa: `Transkrypcja App`
6. **Skopiuj klucz** (format: `sk-proj-...`)
7. ⚠️ **Zapisz klucz bezpiecznie** - nie będziesz mógł go ponownie zobaczyć!

### Dodaj metodę płatności:
1. Przejdź do: https://platform.openai.com/settings/organization/billing/overview
2. Kliknij **Add payment method**
3. Dodaj kartę kredytową
4. Opcjonalnie: Ustaw limit wydatków (np. $10/miesiąc)

---

## 3️⃣ Wdrożenie na Streamlit Cloud

### Połącz z GitHub:
1. Wejdź na https://share.streamlit.io/
2. Kliknij **Sign in** → Zaloguj przez GitHub
3. Kliknij **New app**

### Konfiguracja aplikacji:
- **Repository:** Wybierz `TWOJA_NAZWA/transkrypcja-yt`
- **Branch:** `main`
- **Main file path:** `app_api.py` ⬅️ **WAŻNE: Użyj wersji API!**
- **App URL:** Wybierz nazwę (np. `moja-transkrypcja`)

### Dodaj Secret (Klucz API):
1. Kliknij **Advanced settings**
2. W sekcji **Secrets** wklej:

```toml
OPENAI_API_KEY = "sk-proj-TWOJ_PRAWDZIWY_KLUCZ_TUTAJ"
```

3. ⚠️ Zamień `sk-proj-TWOJ_PRAWDZIWY_KLUCZ_TUTAJ` na **rzeczywisty klucz** z OpenAI
4. Kliknij **Deploy!**

---

## 4️⃣ Czekaj na Deploy

- ⏳ Pierwsze wdrożenie zajmie 2-5 minut
- 📊 Możesz obserwować logi w czasie rzeczywistym
- ✅ Gdy zobaczyjesz "Your app is live!" - gotowe!

---

## 5️⃣ Udostępnij Aplikację

Twoja aplikacja będzie dostępna pod adresem:
```
https://TWOJA-APLIKACJA.streamlit.app
```

Możesz udostępnić ten link komukolwiek! 🎉

### Przykładowy link do dodania w README.md:
```markdown
## 🌐 Demo Online
Aplikacja dostępna online: https://moja-transkrypcja.streamlit.app

**Hasło:** BozeNarodzenie25
```

---

## 🔧 Aktualizacja Aplikacji

Gdy wprowadzisz zmiany w kodzie:

```powershell
git add .
git commit -m "Opis zmian"
git push
```

Streamlit Cloud automatycznie wykryje zmiany i zaktualizuje aplikację! 🚀

---

## 💰 Monitorowanie Kosztów

### W OpenAI Dashboard:
1. Przejdź do https://platform.openai.com/usage
2. Sprawdzaj miesięczne zużycie API
3. Ustaw alerty przy określonych kwotach

### Szacowane koszty użycia:
| Użycie miesięczne | Koszt USD | Koszt PLN |
|-------------------|-----------|-----------|
| 10 godz transkrypcji | $3.60 | ~14 PLN |
| 50 godz transkrypcji | $18 | ~72 PLN |
| 100 godz transkrypcji | $36 | ~144 PLN |

---

## 🔒 Bezpieczeństwo

### ✅ DOBRZE:
- Klucz API w Streamlit Secrets (ukryty)
- Plik `.gitignore` chroni lokalne secrets
- Hasło do aplikacji

### ❌ NIGDY:
- Nie commituj `secrets.toml` do GitHub
- Nie udostępniaj klucza API publicznie
- Nie wklejaj klucza w kodzie źródłowym

---

## 🆘 Rozwiązywanie Problemów

### Błąd: "OpenAI API key not found"
- Sprawdź czy dodałeś klucz w **Streamlit Secrets**
- Format musi być: `OPENAI_API_KEY = "sk-proj-..."`
- Zrestartuj aplikację w Streamlit Cloud

### Błąd: "Quota exceeded"
- Sprawdź limit w OpenAI Dashboard
- Dodaj metodę płatności
- Zwiększ limit wydatków

### Aplikacja nie startuje:
- Sprawdź logi w Streamlit Cloud
- Upewnij się że używasz `app_api.py` (nie `app.py`)
- Sprawdź czy `requirements_api.txt` jest poprawny

---

## 📞 Wsparcie

- **Streamlit Docs:** https://docs.streamlit.io/
- **OpenAI Docs:** https://platform.openai.com/docs/
- **yt-dlp Issues:** https://github.com/yt-dlp/yt-dlp/issues

---

## 🎯 Podsumowanie

Po wykonaniu tych kroków:
- ✅ Aplikacja działa online 24/7
- ✅ Dostępna pod publicznym URL
- ✅ Automatyczne aktualizacje z GitHub
- ✅ Bezpieczne przechowywanie klucza API
- ✅ Darmowy hosting na Streamlit Cloud

**Czas wdrożenia:** ~15-20 minut

Powodzenia! 🚀
