import streamlit as st
from google import genai
from gtts import gTTS
import io
import json

# UI 텍스트 사전
LANG_UI = {
    "한국어": {
        "api_sidebar": "⚙️ 설정",
        "native_lang": "나의 모국어 (UI)",
        "target_lang": "학습할 언어",
        "title": "🌐 다국어 작문 연습기",
        "subtitle": "AI 기반 외국어 작문 및 레벨업 분석기",
        "input_label": "학습 언어로 문장을 입력하세요:",
        "analyze_btn": "✨ 분석 및 첨언하기",
        "placeholder_prefix": "예: ",
        "feedback_title": "📝 분석 및 피드백",
        "level_label": "학습 난이도",
        "vocab_label": "📚 주요 단어 공부",
        "levelup_label": "🚀 한 단계 위로! (Level-up)",
        "synonym_label": "🔗 유의어",
        "antonym_label": "💡 반의어",
        "point_label": "수준으로 쓰기",
        "corrected_label": "✅ 교정된 문장",
        "meaning_label": "👉 **뜻:**",
        "point_title": "💡 포인트",
        "audio_btn": "🔈 발음 듣기",
        "analaizing": "AI 선생님이 문장을 분석중입니다...",
        "mission_label": "번역해보기",
        "mission_btn": "🎯 예문 생성",
        "mission_placeholder": "무슨 말을 써야할 지 모르겠다면 번역연습을 해보아요.",
     },
    "English": {
        "api_sidebar": "⚙️ Settings",
        "native_lang": "My Native Language (UI)",
        "target_lang": "Target Language",
        "title": "🌐 Polyglot Tutor",
        "subtitle": "AI-Powered Writing & Level-up Analysis",
        "input_label": "Enter text in the language you are learning:",
        "analyze_btn": "✨ Analyze & Feedback",
        "placeholder_prefix": "Ex: ",
        "feedback_title": "📝 Analysis & Feedback",
        "level_label": "Difficulty",
        "vocab_label": "📚 Key Vocabulary",
        "levelup_label": "🚀 Level-up Sentences",
        "synonym_label": "🔗 Synonym",
        "antonym_label": "💡 Antonym",
        "point_label": "level to write",
        "corrected_label": "✅ Corrected Frase",
        "meaning_label": "👉 **Meaning:**",
        "point_title": "💡 Point",
        "audio_btn": "🔈 Listen",
        "analaizing": "The AI ​​teacher is analyzing the sentence.",
        "mission_label": "To try to translate",
        "mission_btn": "🎯 Generate example",
        "mission_placeholder": "If you don't know what to write, let's try to translate.",
    },
    "日本語": {
        "api_sidebar": "⚙️ 設定",
        "native_lang": "自分の母国語 (UI)",
        "target_lang": "学習する言語",
        "title": "🌐 多言語作文チューター",
        "subtitle": "AIによる作文添削とレベルアップ分析",
        "input_label": "学習中の言語で文章を入力してください。:",
        "analyze_btn": "✨ 添削および分析する",
        "placeholder_prefix": "例: ",
        "feedback_title": "📝 分析とフィードバック",
        "level_label": "難度",
        "vocab_label": "📚 重要単語学習",
        "levelup_label": "🚀 ステップアップ！",
        "synonym_label": "🔗 類義語, 似たような単語",
        "antonym_label": "💡 反意語, 反対の意味の単語",
        "point_label": "レベルで書いてみよう。",
        "corrected_label": "✅ 修正された文章",
        "meaning_label": "👉 **意味:**",
        "point_title": "💡 ポイント",
        "audio_btn": "🔈 発音を聞く",
        "analaizing": "AI先生が文章を解析しています。。。",
        "mission_label": "翻訳してみよう",
        "mission_btn": "🎯 例文作成",
        "mission_placeholder": "何を書けばよく分からないときは翻訳の練習をしてみましょう。",
    },
    "Italiano": {
        "api_sidebar": "⚙️ Impostazioni",
        "native_lang": "La mia lingua madre (UI)",
        "target_lang": "Lingua da imparare",
        "title": "🌐 Tutor di Scrittura Poliglotta",
        "subtitle": "Analisi della scrittura e potenziamento del livello tramite AI",
        "input_label": "Inserisci una frase nella lingua che stai imparando:",
        "analyze_btn": "✨ Analizza e Commenta",
        "placeholder_prefix": "Es: ",
        "feedback_title": "📝 Analisi e Feedback",
        "level_label": "Difficoltà",
        "vocab_label": "📚 Studio dei vocaboli chiave",
        "levelup_label": "🚀 Sali di livello! (Level-up)",
        "synonym_label": "🔗 Sinonimi",
        "antonym_label": "💡 Contrari",
        "point_label": "Scrivere al livello",
        "corrected_label": "✅ Frase Corretta",
        "meaning_label": "👉 **Significato:**",
        "point_title": "💡 Punti chiave",
        "audio_btn": "🔈 Ascolta la pronuncia",
        "analaizing": "L'insegnante AI sta analizzando la frase...",
        "mission_label": "Per provare a tradurre",
        "mission_btn": "🎯 Genera esempio",
        "mission_placeholder": "Se non sai cosa scrivere, proviamo a tradurre.",
    },
}

# gTTS 언어 코드 매핑 (내부 로직용)
LANG_CODES = {
    "Italian": "it",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru",
    "Vietnamese": "vi",
    "Thai": "th",
    "Dutch": "nl",
    "Turkish": "tr"
}

# 국기 매핑 사전 (보너스 아이디어)
FLAGS = {
    "Italian": "🇮🇹", "English": "🇺🇸", "Spanish": "es", "French": "🇫🇷", 
    "German": "🇩🇪", "Japanese": "🇯🇵", "Chinese": "🇨🇳", "Korean": "🇰🇷"
}

# 학습 언어별 입력을 돕기 위한 예제 문장 (일부러 조금씩 틀린 표현들)
TARGET_EXAMPLES = {
    "Italian": "Io andare a mercato ieri.",
    "English": "I goes to school tomorrow.",
    "Spanish": "Yo querer comer una manzana.",
    "French": "Je manger le pomme.",
    "German": "Ich essen Brot heute.",
    "Japanese": "私は昨日、りんごを食べます。",
    "Chinese": "我昨天去商店买东西。", # 예시는 올바른 문장이어도 좋습니다.
    "Korean": "나 내일 학교 갔어요."
}

# 레벨별 상세 가이드 정의 (CEFR 기준)
LEVEL_GUIDE = {
    "A1": "very basic, focusing on daily greetings and simple self-introduction.",
    "A2": "routine tasks, basic personal/family info, and simple shopping scenarios.",
    "B1": "personal interests, work-related topics, and describing experiences or dreams.",
    "B2": "complex ideas on both concrete and abstract topics, including technical discussions in their field.",
    "C1": "demanding, longer texts with implicit meaning, using sophisticated vocabulary and professional nuances.",
    "C2": "virtually everything heard or read, including subtle nuances of meaning in complex academic or literary contexts."
}

# --- 1. 페이지 설정 및 상태 유지(Session State) ---
st.set_page_config(page_title="Bella Scrittura", layout="wide")

# AI 분석 결과를 저장할 바구니를 만듭니다. (이게 있어야 버튼 눌러도 안 날아감)
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# 사이드바: 설정
with st.sidebar:
    # 1. 예약석 생성 (타이틀용)
    st.divider()
    sidebar_title_placeholder = st.empty()
    select_place = st.empty() # 모국어 선택창용
    if "native_lang" not in st.session_state:
        st.session_state.native_lang = "English"  # 초기 기본값
    ui = LANG_UI[st.session_state.native_lang]

    # 2. 모국어 선택 (한국어, English, 日本語)
    # 아직 ui가 정의되지 않았으므로 처음엔 영어/한국어로 가이드를 줍니다.
    native_choice = st.selectbox(
        ui["native_lang"], 
        list(LANG_UI.keys()), 
        index=list(LANG_UI.keys()).index(st.session_state.native_lang),
        key="lang_selector"
    )

    if native_choice != st.session_state.native_lang:
        st.session_state.native_lang = native_choice
        st.rerun()  # 이 명령어가 '한 번 더 클릭'하는 수고를 없애줍니다.

    # 3. 타이틀 배치
    sidebar_title_placeholder.title(ui["api_sidebar"])

    # 4. 학습 언어 및 API 설정
    target_choice = st.selectbox(ui["target_lang"], list(LANG_CODES.keys()))
    target_code = LANG_CODES[target_choice]
    
    api_key = st.text_input("Gemini API Key", type="password")

    # 모델 목록을 저장할 세션 상태 초기화
    if "model_list" not in st.session_state:
        st.session_state.model_list = []

    if api_key:
        if not st.session_state.model_list:
            try:
                # 모델을 가져오는 동안만 잠깐 로딩 표시
                with st.spinner("🔄 Loading models..."):
                    client = genai.Client(api_key=api_key)
                    fetched_models = []
                    
                    # SDK 버전에 따라 속성명이 다를 수 있으므로 안전하게 접근
                    for m in client.models.list():
                        # 'generate_content' 혹은 'generateContent' 확인
                        # hasattr를 사용하여 속성이 존재하는지 먼저 체크 (404/AttributeError 방지)
                        methods = getattr(m, 'supported_generation_methods', [])
                        if 'generateContent' in methods or 'generate_content' in methods:
                            name = m.name.replace('models/', '')
                            fetched_models.append(name)
                    
                    if fetched_models:
                        st.session_state.model_list = sorted(fetched_models)
                    else:
                        # 목록이 비어있으면 기본값 강제 할당
                        st.session_state.model_list = ["gemini-2.5-flash", "gemini-pro-latest", "gemini-2.5-flash-lite"]
            except Exception as e:
                # 에러 발생 시 사용자에게 에러를 보여주지 않고 조용히 기본 모델로 세팅
                # 이것이 진정한 UX 관리입니다.
                st.session_state.model_list = ["gemini-2.5-flash", "gemini-pro-latest", "gemini-2.5-flash-lite"]
        
        # 모델 선택창 출력
        selected_model = st.selectbox(
            "Select AI Model", 
            st.session_state.model_list,
            index=0
        )
    else:
        st.info("Please enter your API Key")
        selected_model = "gemini-2.5-flash"
    
    # 5. 나머지 설정들
    current_flag = FLAGS.get(target_choice, "🌐")
    target_flag = FLAGS.get(native_choice, "🌐")

    st.divider()
    st.caption(f"Status: {native_choice} ➡️ {target_choice}")

# 메인 UI
st.title(f"{current_flag} {ui['title']}")
st.caption(ui["subtitle"])

col_input, col_mission = st.columns([1.2, 1])

# 버튼 배치를 위한 컬럼
with col_input:

    # 입력창
    example_text = TARGET_EXAMPLES.get(target_choice, "...")
    user_input = st.text_area(
        ui["input_label"], 
        placeholder=f"{ui['placeholder_prefix']}{example_text}",
        height=150
    ) # 입력창 크기를 조금 더 키워주면 시원시원합니다.

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_btn = st.button(ui["analyze_btn"], use_container_width=True)

    # --- 2. 분석 로직 (버튼 클릭 시 실행) ---
    if analyze_btn:
        if not api_key:
            st.error("API 키를 입력해주세요.")
        elif not user_input:
            st.warning("분석할 문장을 입력해주세요.")
        else:
            current_mission = st.session_state.get("current_mission")
            client = genai.Client(api_key=api_key)

            if current_mission:
                # [미션 모드] 원문과의 비교를 최우선으로 함
                mode_instruction = f"""
                [MISSION MODE]
                - The user's goal is to translate the following sentence into {target_choice}.
                - Original Sentence (Source): "{current_mission}"
                - Please evaluate how accurately the user captured the meaning and nuance of the source sentence.
                """
            else:
                mode_instruction = f"""
                    [FREE WRITING MODE]
                    - The user is writing freely in {target_choice}.
                    - Please analyze the sentence for naturalness, grammar, and flow.
                    """

            prompt = f"""
            이 지침을 참고해줘: {mode_instruction},
            사용자의 {target_choice} 문장: "{user_input}"
            너는 전문 {target_choice} 강사야. 사용자의 모국어인 {native_choice}로 친절하게 대답해줘. 아래 항목을 포함한 JSON 형식으로 대답해줘.:
            {{
                "corrected": "교정된 완벽한 문장",
                "translation": "교정된 문장의 {native_choice} 번역",
                "explanation": "문법 오류 및 수정 이유 ({native_choice})",
                "current_level": "현재 문장의 난이도 (A1-C2)",
                "level_up": [
                {{
                    "level": "현재보다 한 단계 높은 레벨 (예: A2)",
                    "sentence": "해당 레벨의 확장 문장",
                    "meaning": "{native_choice} 뜻",
                    "advanced_points": "이 문장에서 새로 쓰인 고급 문법이나 어휘 설명"
                }},
                {{
                    "level": "현재보다 두 단계 높은 레벨 (예: B1)",
                    "sentence": "해당 레벨의 확장 문장",
                    "meaning": "{native_choice} 뜻",
                    "advanced_points": "이 문장에서 새로 쓰인 고급 문법이나 어휘 설명"
                }}
                ],
                "vocabulary": [
                {{
                    "word": "핵심 단어", 
                    "meaning": "{native_choice} 뜻",
                    "synonym": "유의어(뜻)", 
                    "antonym": "반의어(뜻)"
                }}
                ]
            }}
            채팅 텍스트 없이 오직 JSON 데이터만 출력해. 
            특히 'level_up' 섹션은 학습자가 다음 단계로 넘어갈 수 있도록 더 풍부한 표현과 격식 있는 어휘를 사용해줘.
            """
        
            with st.spinner(ui["analaizing"]):
                try:
                    response = client.models.generate_content(model=selected_model, contents=prompt)
                    # JSON 데이터 정제 및 저장
                    clean_json = response.text.strip().replace('```json', '').replace('```', '')
                    st.session_state.analysis_result = json.loads(clean_json)
                except Exception as e:
                    st.error(f"분석 중 오류가 발생했습니다: {e}")

with col_mission:

    # --- 메인 영역: 미션 생성기 ---
    st.subheader(ui.get("mission_label", "🎯 오늘의 미션"))

    # 예문이 출력될 공간
    mission_area = st.info(st.session_state.get("current_mission", ui.get("mission_placeholder", "번역할 문장이 여기 나타납니다.")))

    # 난이도 선택 (CEFR 기준)
    level_choice = st.select_slider(
        "Level",
        options=["A1", "A2", "B1", "B2", "C1", "C2"],
        value="A1"
    )

    col_gen_btn, col_del_btn = st.columns([1, 1])

    with col_gen_btn:
        gen_btn = st.button(ui.get("mission_btn", "🎯 예문 생성"))

    # 예문 생성 로직
    if gen_btn:
        with st.spinner("AI가 미션을 만드는 중..."):
            # simple sentence라는 표현을 삭제하고 LEVEL_GUIDE를 삽입
            client = genai.Client(api_key=api_key)
            mission_prompt = f"""
            Act as a professional language examiner. 
            Create a sentence in {native_choice} for a learner to translate into {target_choice}.
            The sentence MUST strictly reflect the {level_choice} level of the CEFR standard.
        
            Level Characteristics: {LEVEL_GUIDE[level_choice]}
        
            Requirements:
            1. Return ONLY the sentence in {native_choice}.
            2. No explanations, no translations, no quotes.
            3. Ensure the sentence complexity (grammar, vocabulary, and length) matches the {level_choice} level perfectly.
            """
        
            try:
                m_res = client.models.generate_content(model=selected_model, contents=mission_prompt)
                st.session_state.current_mission = m_res.text.strip().replace('"', '')
                st.rerun()
            except Exception as e:
                st.error(f"미션 생성 실패: {e}")

    if st.session_state.get("current_mission"):
        with col_del_btn:
            if st.button("🗑️ 미션 지우기 (자유 작문 모드로 변경)"):
                st.session_state.current_mission = None
                st.rerun()

st.divider()

# --- 3. 결과 화면 표시 (분석 결과가 있을 때만 항상 표시) ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    
    # 1. 교정 및 평가
    c1, c2 = st.columns([2, 1])
    with c1:
        st.success(ui['corrected_label'])
        st.subheader(res['corrected'])
        st.write(f"{ui['meaning_label']} {res['translation']}") # 최종 번역 추가
        
        if st.button(ui['audio_btn']):
            with st.spinner("Generating audio..."):
                # 이미 사이드바에서 정의된 target_code를 바로 사용
                tts = gTTS(text=res['corrected'], lang=target_code) 
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3', autoplay=True)

    with c2:
        st.metric(f"{ui['level_label']}", res['current_level'])
    st.divider()
    # 2. 상세 설명
    st.info(ui["feedback_title"])
    st.write(res['explanation'])

    # 3. 단어 및 확장
    st.divider()
    v1, v2 = st.columns(2)
    with v1:
        st.subheader(ui["vocab_label"])
        for item in res['vocabulary']:
            st.write(f"**{item['word']}** ({item['meaning']})")
            st.caption(f"{ui['synonym_label']}: {item['synonym']} | {ui['antonym_label']}: {item['antonym']}")
            st.write("") # 간격 띄우기
    
    with v2:
        st.subheader(ui["levelup_label"])
        for i, up in enumerate(res['level_up']):
            with st.expander(f"⭐ {up['level']} {ui['point_label']}", expanded=True):
                st.write(f"{current_flag}| {up['sentence']}")
                st.caption(f"{target_flag}| {up['meaning']}")
                st.info(f"{ui['point_title']}: {up['advanced_points']}")
                
                # 확장 문장용 발음 버튼 (고유 키를 위해 i 사용)
                if st.button(f"{ui['audio_btn']}", key=f"voice_{i}"):
                    tts = gTTS(text=up['sentence'], lang=target_code)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp, format='audio/mp3', autoplay=True)