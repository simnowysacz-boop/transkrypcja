import streamlit as st
import openai
import yt_dlp
import os
import tempfile
from pathlib import Path

# Konfiguracja strony
st.set_page_config(
    page_title="Transkrypcja PL - Facebook/YouTube (API)",
    page_icon="🎙️",
    layout="centered"
)

# Stałe
HASLO = "BozeNarodzenie25"  # Zmień to hasło na własne

# Pobierz klucz API z secrets (Streamlit Cloud) lub ze zmiennej środowiskowej
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Inicjalizacja OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Inicjalizacja session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def logowanie():
    """Wyświetla formularz logowania"""
    st.title("🔐 Logowanie")
    st.write("Wprowadź hasło, aby uzyskać dostęp do aplikacji transkrypcji.")
    
    haslo_input = st.text_input("Hasło:", type="password", key="password_input")
    
    if st.button("Zaloguj się", key="login_button"):
        if haslo_input == HASLO:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Nieprawidłowe hasło!")

def pobierz_audio(url: str, output_path: str) -> str:
    """
    Pobiera audio z podanego URL (Facebook/YouTube) używając yt-dlp
    
    Args:
        url: Link do materiału wideo
        output_path: Ścieżka do zapisu pliku audio
    
    Returns:
        Ścieżka do pobranego pliku audio
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            duration = info.get('duration', 0)
        return output_path + '.mp3', duration
    except Exception as e:
        raise Exception(f"Błąd pobierania audio: {str(e)}")

def transkrybuj_audio_api(audio_path: str) -> dict:
    """
    Wykonuje transkrypcję pliku audio używając OpenAI Whisper API
    
    Args:
        audio_path: Ścieżka do pliku audio
    
    Returns:
        Słownik z wynikami transkrypcji
    """
    try:
        with open(audio_path, 'rb') as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pl",
                response_format="verbose_json"
            )
        
        # Konwersja do formatu zgodnego z lokalnym Whisper
        result = {
            'text': transcript.text,
            'language': 'pl',
            'segments': [],
            'duration': getattr(transcript, 'duration', 0)
        }
        
        # Jeśli API zwraca segmenty
        if hasattr(transcript, 'segments'):
            result['segments'] = transcript.segments
        
        return result
    except Exception as e:
        raise Exception(f"Błąd transkrypcji API: {str(e)}")

def aplikacja_glowna():
    """Główna aplikacja transkrypcji"""
    st.title("🎙️ Transkrypcja Facebook/YouTube (PL)")
    st.write("Aplikacja do automatycznej transkrypcji materiałów wideo w języku polskim.")
    st.info("🌐 **Wersja API** - Działa w chmurze, szybka transkrypcja przez OpenAI")
    
    # Sprawdź czy klucz API jest dostępny
    if not OPENAI_API_KEY:
        st.error("⚠️ Brak klucza API OpenAI! Aplikacja nie będzie działać.")
        st.info("Administrator musi dodać klucz API w ustawieniach Streamlit Cloud (Secrets).")
        return
    
    # Sidebar z opcjami
    with st.sidebar:
        st.header("⚙️ Informacje")
        st.success("✅ OpenAI Whisper API")
        st.info("""
        **Wersja API:**
        - Szybka transkrypcja
        - Działa w chmurze
        - Wysoka dokładność PL
        - Koszt: $0.006/min
        """)
        
        st.markdown("---")
        st.write("**💰 Szacowane koszty:**")
        st.write("- 10 min: $0.06 (~0.24 PLN)")
        st.write("- 30 min: $0.18 (~0.72 PLN)")
        st.write("- 60 min: $0.36 (~1.44 PLN)")
        
        if st.button("🚪 Wyloguj się"):
            st.session_state.authenticated = False
            st.rerun()
    
    # Główna sekcja
    st.header("📎 Podaj link do materiału")
    url = st.text_input(
        "Link do filmu (Facebook lub YouTube):",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Wklej pełny link do filmu z Facebooka lub YouTube"
    )
    
    if st.button("🎬 Rozpocznij transkrypcję", type="primary"):
        if not url:
            st.warning("⚠️ Proszę podać link do filmu.")
            return
        
        # Tworzenie tymczasowego katalogu
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Pobieranie audio
                with st.spinner("⬇️ Pobieranie audio..."):
                    output_path = os.path.join(temp_dir, "audio")
                    audio_file, duration = pobierz_audio(url, output_path)
                    st.success("✅ Audio pobrane pomyślnie!")
                
                # Sprawdź rozmiar pliku (API ma limit 25MB)
                file_size_mb = os.path.getsize(audio_file) / (1024 * 1024)
                if file_size_mb > 25:
                    st.error(f"❌ Plik jest za duży ({file_size_mb:.1f}MB). OpenAI API akceptuje max 25MB.")
                    st.info("💡 Spróbuj krótszego filmu lub użyj wersji lokalnej (app.py)")
                    return
                
                # Szacowany koszt
                cost_usd = (duration / 60) * 0.006
                cost_pln = cost_usd * 4.0
                st.info(f"💰 Szacowany koszt: ${cost_usd:.4f} (~{cost_pln:.2f} PLN)")
                
                # Transkrypcja
                with st.spinner("🎙️ Transkrypcja w toku... To może potrwać chwilę."):
                    result = transkrybuj_audio_api(audio_file)
                    st.success("✅ Transkrypcja zakończona!")
                
                # Wyświetlanie wyników
                st.header("📝 Wyniki transkrypcji")
                
                # Pełny tekst
                st.subheader("Pełny tekst:")
                st.text_area(
                    "Transkrypcja:",
                    result['text'],
                    height=300,
                    label_visibility="collapsed"
                )
                
                # Przycisk pobierania
                st.download_button(
                    label="💾 Pobierz transkrypcję (TXT)",
                    data=result['text'],
                    file_name="transkrypcja.txt",
                    mime="text/plain"
                )
                
                # Segmenty z czasami (jeśli dostępne)
                if result.get('segments'):
                    with st.expander("🕐 Pokaż segmenty z znacznikami czasu"):
                        for segment in result['segments']:
                            start = segment.get('start', 0)
                            end = segment.get('end', 0)
                            text = segment.get('text', '')
                            st.write(f"**[{start:.2f}s - {end:.2f}s]** {text}")
                
                # Informacje statystyczne
                with st.expander("📊 Statystyki"):
                    num_chars = len(result['text'])
                    num_words = len(result['text'].split())
                    
                    # Przybliżona liczba tokenów (1 token ≈ 4 znaki dla PL)
                    estimated_tokens = num_chars // 4
                    
                    # Rzeczywisty koszt
                    actual_cost_usd = (duration / 60) * 0.006
                    actual_cost_pln = actual_cost_usd * 4.0
                    
                    st.write(f"- **Język wykryty:** {result.get('language', 'pl')}")
                    st.write(f"- **Liczba znaków:** {num_chars:,}")
                    st.write(f"- **Liczba słów:** {num_words:,}")
                    st.write(f"- **Szacowana liczba tokenów:** {estimated_tokens:,}")
                    st.write(f"- **Długość audio:** {duration:.1f}s ({duration/60:.1f} min)")
                    st.write(f"- **Koszt transkrypcji:** ${actual_cost_usd:.4f} (~{actual_cost_pln:.2f} PLN)")
                
            except Exception as e:
                st.error(f"❌ Wystąpił błąd: {str(e)}")
                st.info("💡 Sprawdź czy link jest prawidłowy i czy materiał jest publicznie dostępny.")

def main():
    """Główna funkcja aplikacji"""
    if not st.session_state.authenticated:
        logowanie()
    else:
        aplikacja_glowna()
    
    # Stopka
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "© 2025 – Created by Marek Oleniacz&AI"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
