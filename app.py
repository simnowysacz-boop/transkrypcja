import streamlit as st
import whisper
import yt_dlp
import os
import tempfile
from pathlib import Path
import shutil

# Konfiguracja strony
st.set_page_config(
    page_title="Transkrypcja PL - Facebook/YouTube",
    page_icon="🎙️",
    layout="centered"
)

# Stałe
HASLO = "BozeNarodzenie25"  # Zmień to hasło na własne

# Znajdź FFmpeg automatycznie
def znajdz_ffmpeg():
    """Znajduje ścieżkę do FFmpeg w systemie"""
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return os.path.dirname(ffmpeg_path)
    
    # Sprawdź typowe lokalizacje w Windows
    possible_paths = [
        r"C:\Users\win11\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
    ]
    
    for path in possible_paths:
        if os.path.exists(os.path.join(path, 'ffmpeg.exe')):
            return path
    
    return None

FFMPEG_PATH = znajdz_ffmpeg()

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
    
    # Dodaj ścieżkę do FFmpeg jeśli znaleziona
    if FFMPEG_PATH:
        ydl_opts['ffmpeg_location'] = FFMPEG_PATH
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path + '.mp3'
    except Exception as e:
        raise Exception(f"Błąd pobierania audio: {str(e)}")

def transkrybuj_audio(audio_path: str, model_size: str = "medium") -> dict:
    """
    Wykonuje transkrypcję pliku audio używając Whisper
    
    Args:
        audio_path: Ścieżka do pliku audio
        model_size: Rozmiar modelu Whisper (tiny, base, small, medium, large)
    
    Returns:
        Słownik z wynikami transkrypcji
    """
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path, language="pl", fp16=False)
        return result
    except Exception as e:
        raise Exception(f"Błąd transkrypcji: {str(e)}")

def aplikacja_glowna():
    """Główna aplikacja transkrypcji"""
    st.title("🎙️ Transkrypcja Facebook/YouTube (PL)")
    st.write("Aplikacja do automatycznej transkrypcji materiałów wideo w języku polskim.")
    
    # Ostrzeżenie jeśli FFmpeg nie znaleziony
    if not FFMPEG_PATH:
        st.error("⚠️ FFmpeg nie został znaleziony! Aplikacja może nie działać poprawnie.")
        st.info("Zainstaluj FFmpeg i zrestartuj aplikację.")
    
    # Sidebar z opcjami
    with st.sidebar:
        st.header("⚙️ Ustawienia")
        model_size = st.selectbox(
            "Model Whisper:",
            ["tiny", "base", "small", "medium", "large"],
            index=3,
            help="Większe modele są dokładniejsze, ale wolniejsze"
        )
        st.info("""
        **Rozmiary modeli:**
        - tiny: Najszybszy, najmniej dokładny
        - base: Szybki, dobry do testów
        - small: Kompromis szybkość/dokładność
        - medium: Zalecany dla PL ✅
        - large: Najdokładniejszy, najwolniejszy
        """)
        
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
                    audio_file = pobierz_audio(url, output_path)
                    st.success("✅ Audio pobrane pomyślnie!")
                
                # Transkrypcja
                with st.spinner(f"🎙️ Transkrypcja w toku (model: {model_size})... To może potrwać kilka minut."):
                    result = transkrybuj_audio(audio_file, model_size)
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
                
                # Segmenty z czasami (opcjonalnie)
                with st.expander("🕐 Pokaż segmenty z znacznikami czasu"):
                    for segment in result['segments']:
                        start = segment['start']
                        end = segment['end']
                        text = segment['text']
                        st.write(f"**[{start:.2f}s - {end:.2f}s]** {text}")
                
                # Informacje statystyczne
                with st.expander("📊 Statystyki"):
                    num_chars = len(result['text'])
                    num_words = len(result['text'].split())
                    
                    # Przybliżona liczba tokenów (1 token ≈ 4 znaki dla PL)
                    estimated_tokens = num_chars // 4
                    
                    # Przybliżony koszt (model Whisper jest darmowy lokalnie)
                    # Ale można pokazać teoretyczny koszt API OpenAI: $0.006/min audio
                    duration = result['segments'][-1]['end'] if result['segments'] else 0
                    estimated_cost_usd = (duration / 60) * 0.006
                    estimated_cost_pln = estimated_cost_usd * 4.0  # przybliżony kurs
                    
                    st.write(f"- **Język wykryty:** {result.get('language', 'pl')}")
                    st.write(f"- **Liczba segmentów:** {len(result['segments'])}")
                    st.write(f"- **Liczba znaków:** {num_chars:,}")
                    st.write(f"- **Liczba słów:** {num_words:,}")
                    st.write(f"- **Szacowana liczba tokenów:** {estimated_tokens:,}")
                    st.write(f"- **Długość audio:** {duration:.1f}s ({duration/60:.1f} min)")
                    st.write(f"- **Szacowany koszt (API):** ${estimated_cost_usd:.4f} (~{estimated_cost_pln:.2f} PLN)")
                    st.info("💡 Używasz lokalnego modelu Whisper - **całkowicie za darmo!** Powyższy koszt to tylko orientacyjna wartość gdyby użyć API OpenAI.")
                
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
