import os
import streamlit as st
import requests
import random
import time
from typing import Dict, List, Optional

# --- Page & Session State Setup ---
st.set_page_config(page_title="Indian History Explorer", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

if "needs_reload" not in st.session_state:
    st.session_state.needs_reload = False

# --- Multilingual UI Text ---
LANGUAGES = {
    "English": {
        "title": "🏛️ Indian History Explorer",
        "subtitle": "Discover the Rich Heritage of India",
        "search_placeholder": "Search for Indian historical events, personalities, or periods...",
        "search_button": "Explore History",
        "quiz_title": "🧠 Test Your Knowledge",
        "quiz_button": "Take Quiz",
        "quiz_topic_placeholder": "Enter topic for quiz (e.g., Mughal Empire, Freedom Struggle)",
        "no_results": "No results found. Please try a different search term.",
        "loading": "Loading historical information...",
        "quiz_loading": "Generating quiz questions...",
        "submit_quiz": "Submit Quiz",
        "score_text": "Your Score:",
        "correct_answer": "Correct Answer:",
        "explanation": "Explanation:",
        "congratulations": "Congratulations!",
        "well_done": "Well Done!",
        "good_effort": "Good Effort!",
        "keep_learning": "Keep Learning!",
        "language_selector": "Select Language",
        "wiki_link": "Read More on Wikipedia",
        "image_gallery": "Related Images",
        "historical_context": "Historical Context"
    },
    "हिंदी": {
        "title": "🏛️ भारतीय इतिहास खोजकर्ता",
        "subtitle": "भारत की समृद्ध विरासत की खोज करें",
        "search_placeholder": "भारतीय ऐतिहासिक घटनाओं, व्यक्तित्वों या कालों की खोज करें...",
        "search_button": "इतिहास खोजें",
        "quiz_title": "🧠 अपने ज्ञान का परीक्षण करें",
        "quiz_button": "प्रश्नोत्तरी लें",
        "quiz_topic_placeholder": "प्रश्नोत्तरी के लिए विषय दर्ज करें (जैसे मुगल साम्राज्य, स्वतंत्रता संग्राम)",
        "no_results": "कोई परिणाम नहीं मिला। कृपया एक अलग खोज शब्द आज़माएं।",
        "loading": "ऐतिहासिक जानकारी लोड हो रही है...",
        "quiz_loading": "प्रश्नोत्तरी प्रश्न तैयार किए जा रहे हैं...",
        "submit_quiz": "प्रश्नोत्तरी जमा करें",
        "score_text": "आपका स्कोर:",
        "correct_answer": "सही उत्तर:",
        "explanation": "स्पष्टीकरण:",
        "congratulations": "बधाई हो!",
        "well_done": "बहुत अच्छा!",
        "good_effort": "अच्छा प्रयास!",
        "keep_learning": "सीखते रहें!",
        "language_selector": "भाषा चुनें",
        "wiki_link": "विकिपीडिया पर और पढ़ें",
        "image_gallery": "संबंधित चित्र",
        "historical_context": "ऐतिहासिक संदर्भ"
    },
    "తెలుగు": {
        "title": "🏛️ భారత చరిత్ర అన్వేషణ",
        "subtitle": "భారతదేశ అతిపెద్ద చరిత్రను తెలుసుకోండి",
        "search_placeholder": "భారత చరిత్ర సంఘటనలు, వ్యక్తులు లేదా కాలాలను శోధించండి...",
        "search_button": "చరిత్ర కొరకు వెతపండి",
        "quiz_title": "🧠 మీ జ్ఞానాన్ని పరీక్షించండి",
        "quiz_button": "క్విజ్ ప్రారంభించండి",
        "quiz_topic_placeholder": "క్విజ్ కోసం అంశాన్ని నమోదు చేయండి...",
        "no_results": "ఫలితాలు లేవు. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "loading": "చరిత్రా సమాచారం లోడ్ అవుతోంది...",
        "quiz_loading": "క్విజ్ ప్రశ్నలు తయారవుతున్నాయి...",
        "submit_quiz": "క్విజ్ సమర్పించండి",
        "score_text": "మీ స్కోరు:",
        "correct_answer": "సరైన సమాధానం:",
        "explanation": "వివరణ:",
        "congratulations": "అదిరిపోయింది!",
        "well_done": "మంచిది!",
        "good_effort": "సాధారణంగా బాగా!",
        "keep_learning": "ఇంకా తెలుసుకోండి!",
        "language_selector": "భాషను ఎంచుకోండి",
        "wiki_link": "వికీపీడియాలో చదవండి",
        "image_gallery": "సంబంధిత చిత్రాలు",
        "historical_context": "చారిత్రక నేపథ్యం"
    },
    "தமிழ்": {
        "title": "🏛️ இந்திய வரலாறு ஆராய்ச்சி",
        "subtitle": "இந்தியாவின் பாடசாலையை கண்டறியுங்கள்",
        "search_placeholder": "இந்திய வரலாற் சம்பவங்கள், நபர்கள் அல்லது காலங்களை தேடவும்...",
        "search_button": "வரலாறு தேடு",
        "quiz_title": "🧠 உங்கள் அறிவை முயற்சி செய்யுங்கள்",
        "quiz_button": "வினாடி வினா தொடங்கு",
        "quiz_topic_placeholder": "வினாடி வினாவிற்கு ஒரு தலைப்பை உள்ளிடவும்...",
        "no_results": "பயன்படுத்த முடிந்த ஒன்றும் இல்லை.",
        "loading": "வரலாறு தகவல் ஏற்று கொண்டிருக்கிறது...",
        "quiz_loading": "வினாடி வினாக்கள் உருவாக்கப்படுகிறது...",
        "submit_quiz": "வினாடி வினா சமர்ப்பிக்கவும்",
        "score_text": "உங்கள் மதிப்பெண்:",
        "correct_answer": "சரியான பதில்:",
        "explanation": "விளக்கம்:",
        "congratulations": "வாழ்த்துகள்!",
        "well_done": "மிகப் போகா!",
        "good_effort": "நல் முயற்சி!",
        "keep_learning": "மீண்டும் கற்றுக்கொள்ளுங்கள்!",
        "language_selector": "மொழியைத் தேர்வு செய்க",
        "wiki_link": "விக்கிப்பீடியாவில் வாசிக்கவும்",
        "image_gallery": "படப் தொகுப்பு",
        "historical_context": "வரலாற்று சூழல்"
    },
    "മലയാളം": {
        "title": "🏛️ ഇന്ത്യൻ ചരിത്രം അന്വേഷിക്കുക",
        "subtitle": "ഭാരതത്തിന്റെ സമ്പന്നമായ ചാരിത്ര്യം അന്വേഷിക്കുക",
        "search_placeholder": "ഭാരതീയ ചരിത്ര സംഭവങ്ങൾ, വ്യക്തികൾ അല്ലെങ്കിൽ സമയങ്ങൾ അന്വേഷിക്കുക...",
        "search_button": "ചരിത്രം അന്വേഷിക്കുക",
        "quiz_title": "🧠 നിങ്ങളുടെ അറിവ് പരിശോദിക്കുക",
        "quiz_button": "ക്വിസ് ആരംഭിക്കുക",
        "quiz_topic_placeholder": "ക്വിസിന് വിഷയം നൽകുക...",
        "no_results": "ഫലങ്ങൾ ലഭ്യമല്ല.",
        "loading": "ചരിത്ര വിവരം ലോഡ് ചെയ്യുന്നു...",
        "quiz_loading": "ക്വിസ് ചോദ്യങ്ങൾ തയ്യാറാണ്...",
        "submit_quiz": "ക്വിസ് സമർപ്പിക്കുക",
        "score_text": "നിങ്ങളുടെ സ്കോർ:",
        "correct_answer": "ശരി ഉത്തരം:",
        "explanation": "വിവരണം:",
        "congratulations": "അഭിനന്ദനങ്ങൾ!",
        "well_done": "നല്ലത്!",
        "good_effort": "ശ്രമം!",
        "keep_learning": "കൂടുതൽ പഠിക്കുക!",
        "language_selector": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "wiki_link": "വിക്കിപ്പീഡിയയിൽ വായിക്കുക",
        "image_gallery": "ചിത്രങ്ങൾ",
        "historical_context": "ചരിത്രപരമായ പശ്ചാത്തലം"
    }
}

# --- Wikipedia language domains ---
WIKI_DOMAINS = {
    "English": "en",
    "हिंदी": "hi",
    "తెలుగు": "te",
    "தமிழ்": "ta",
    "മലയാളം": "ml"
}

# --- Wikipedia Explorer Class ---
class IndianHistoryExplorer:
    def __init__(self, lang_code: str):
        self.search_url = f"https://{lang_code}.wikipedia.org/w/api.php"
        self.summary_url = f"https://{lang_code}.wikipedia.org/api/rest_v1/page/summary/"
        self.commons_url = "https://commons.wikimedia.org/w/api.php"

    def search_wikipedia(self, query: str) -> List[Dict]:
        params = {"action": "query", "format": "json", "list": "search", "srsearch": query, "srlimit": 5}
        try:
            r = requests.get(self.search_url, params=params, timeout=10)
            r.raise_for_status()
            return r.json().get("query", {}).get("search", [])
        except Exception as e:
            st.error(f"Search error: {e}")
            return []

    def get_summary(self, title: str) -> Optional[Dict]:
        clean = title.replace(" ", "_")
        try:
            r = requests.get(self.summary_url + clean, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            st.error(f"Summary error: {e}")
            return None

    def get_images(self, title: str, limit: int = 4) -> List[Dict]:
        params = {
            "action": "query", "format": "json", "generator": "search",
            "gsrsearch": title, "gsrnamespace": 6, "gsrlimit": limit,
            "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": 300
        }
        try:
            r = requests.get(self.commons_url, params=params, timeout=10)
            r.raise_for_status()
            pages = r.json().get("query", {}).get("pages", {})
            imgs = []
            for p in pages.values():
                info = p.get("imageinfo", [{}])[0]
                if info.get("thumburl"):
                    imgs.append({"url": info["thumburl"], "title": p.get("title", "").replace("File:", "")})
            return imgs
        except Exception as e:
            st.error(f"Image error: {e}")
            return []

# --- Quiz Generator via Wikipedia ---
def generate_quiz_from_wikipedia(topic: str, lang_code: str, count: int = 5) -> List[Dict]:
    explorer = IndianHistoryExplorer(lang_code)
    pages = explorer.search_wikipedia(topic)
    facts = []
    for p in pages[:3]:
        summary = explorer.get_summary(p["title"])
        extract = summary.get("extract", "") if summary else ""
        sentences = [s.strip() for s in extract.split('.') if len(s.strip()) > 20]
        for s in sentences:
            facts.append((p["title"], s))
    random.shuffle(facts)
    # Build quiz
    quiz = []
    for i in range(min(count, len(facts))):
        title, fact = facts[i]
        question = f"In reference to '{title}', which statement is correct?"
        correct = fact.strip()
        words = correct.split()
        distractors = []
        for _ in range(3):
            idx = random.randint(0, max(0, len(words)-8))
            distractor = ' '.join(words[idx:idx+8]) + '...'
            distractors.append(distractor)
        options = distractors + [correct]
        random.shuffle(options)
        quiz.append({
            "question": question,
            "options": options,
            "correct": options.index(correct),
            "explanation": correct
        })
    return quiz

# --- Main App ---
def main():
    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # Sidebar — language selector
    st.sidebar.title("⚙️ " + LANGUAGES[st.session_state.language]["language_selector"])
    lang = st.sidebar.selectbox(
        "", options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language)
    )
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.session_state.needs_reload = True

    if st.session_state.needs_reload:
        st.session_state.needs_reload = False
        st.rerun()

    txt = LANGUAGES[st.session_state.language]
    lang_code = WIKI_DOMAINS[st.session_state.language]
    explorer = IndianHistoryExplorer(lang_code)

    st.title(txt["title"])
    st.markdown(f"**{txt['subtitle']}**")

    tab1, tab2 = st.tabs([txt["search_button"], txt["quiz_button"]])

    with tab1:
        st.header(txt["search_button"])
        query = st.text_input("search_input", placeholder=txt["search_placeholder"], label_visibility="collapsed")
        if st.button(txt["search_button"]):
            if not query.strip():
                st.warning(txt["no_results"])
            else:
                with st.spinner(txt["loading"]):
                    results = explorer.search_wikipedia(query)
                    time.sleep(0.3)
                if results:
                    st.success(f"{len(results)} result(s)")
                    for idx, item in enumerate(results):
                        title = item["title"]
                        with st.expander(f"📜 {title}", expanded=(idx == 0)):
                            summary = explorer.get_summary(title)
                            if summary:
                                c1, c2 = st.columns([3,1])
                                with c1:
                                    st.subheader(txt["historical_context"])
                                    st.write(summary.get("extract", ""))
                                    link = summary.get("content_urls", {}).get("desktop", {}).get("page", "")
                                    if link:
                                        st.markdown(f"[{txt['wiki_link']}]({link})")
                                with c2:
                                    thumb = summary.get("thumbnail", {}).get("source", "")
                                    if thumb:
                                        st.image(thumb, width=200)
                                st.subheader(txt["image_gallery"])
                                imgs = explorer.get_images(title)
                                if imgs:
                                    cols = st.columns(len(imgs))
                                    for i_img, img in enumerate(imgs):
                                        cols[i_img].image(img["url"], caption=img["title"], use_container_width=True)
                                else:
                                    st.info(txt["no_results"])
                else:
                    st.warning(txt["no_results"])

    with tab2:
        st.header(txt["quiz_title"])
        topic = st.text_input("quiz_topic", placeholder=txt["quiz_topic_placeholder"], label_visibility="collapsed")
        if st.button(txt["quiz_button"]):
            if topic.strip():
                st.session_state.quiz_active = True
                st.session_state.quiz_data = generate_quiz_from_wikipedia(topic, lang_code, count=5)
                st.session_state.user_answers = {}
            else:
                st.warning(txt["quiz_topic_placeholder"])

        if st.session_state.quiz_active and st.session_state.quiz_data:
            st.markdown("---")
            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"**Q{i+1}. {q['question']}**")
                ans = st.radio(f"ans_{i}", q["options"], key=f"ans_{i}")
                st.session_state.user_answers[i] = ans
            if st.button(txt["submit_quiz"]):
                total = len(st.session_state.quiz_data)
                correct = sum(
                    st.session_state.user_answers.get(i) == q["options"][q["correct"]]
                    for i, q in enumerate(st.session_state.quiz_data)
                )
                pct = correct / total * 100
                st.metric(txt["score_text"], f"{correct}/{total} ({pct:.1f}%)")
                message = (
                    txt["congratulations"] if pct >= 80 else
                    txt["well_done"] if pct >= 60 else
                    txt["good_effort"] if pct >= 40 else
                    txt["keep_learning"]
                )
                st.success(message)
                st.markdown("### Detailed Answers")
                for i, q in enumerate(st.session_state.quiz_data):
                    ua = st.session_state.user_answers.get(i)
                    ca = q["options"][q["correct"]]
                    with st.expander(f"Q{i+1}: {q['question']}"):
                        if ua == ca:
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Incorrect")
                            st.write(f"{txt['correct_answer']} {ca}")
                        st.write(f"**{txt['explanation']}** {q['explanation']}")
                if st.button("🔁 " + txt["quiz_button"]):
                    st.session_state.quiz_active = False

if __name__ == "__main__":
    main()
