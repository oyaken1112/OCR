import streamlit as st
from PIL import Image
import pyocr
import platform
import os
import subprocess

# Tesseractのパスを確認するためのデバッグコード
def get_tesseract_path():
    try:
        result = subprocess.run(['which', 'tesseract'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Tesseract not found"
    except Exception as e:
        return f"Exception: {e}"

# Tesseractのパスを取得
tesseract_path = get_tesseract_path()
st.write(f"Tesseract path: {tesseract_path}")

# Tesseract のパス設定
if platform.system().lower() == "windows":
    pyocr.tesseract.TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    # Linux (Streamlit Cloudなどのクラウド環境)
    if tesseract_path == "Tesseract not found":
        st.error("Tesseract がインストールされていないか、パスが見つかりません。")
    else:
        pyocr.tesseract.TESSERACT_CMD = tesseract_path

# Tesseract のパス確認
if not os.path.exists(pyocr.tesseract.TESSERACT_CMD):
    st.error(f"Tesseract のパスが正しくありません: {pyocr.tesseract.TESSERACT_CMD}")
else:
    st.success(f"Tesseract のパスが正しく設定されています: {pyocr.tesseract.TESSERACT_CMD}")

# 画像読み込みのための言語と言語のコードを変換するリストを設定
set_language_list = {
    "日本語": "jpn",
    "英語": "eng",
}

st.title("文字認識アプリ")

set_language = st.selectbox("音声認識する言語を選んでください。", set_language_list.keys())
file_upload = st.file_uploader("ここに音声認識したファイルをアップロードしてください")

if file_upload is not None:
    st.image(file_upload)

    engines = pyocr.get_available_tools()
    st.write("OCRエンジンのリスト:", engines)
    if len(engines) == 0:
        st.error("OCRエンジンが見つかりません。Tesseractが正しくインストールされているか確認してください。")
    else:
        engine = engines[0]

        txt = engine.image_to_string(Image.open(file_upload), lang=set_language_list[set_language])
        st.write(txt)

        st.write("感情分析の結果")
        from asari.api import Sonar
        sonar = Sonar()
        res = sonar.ping(text=txt)
        st.write(res["classes"])
