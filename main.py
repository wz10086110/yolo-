from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
import shutil
import uuid

from services.overall_service import analyze_overall
from services.crack_service import analyze_crack
from services.segment_service import analyze_segment
from services.assessment_service import assess_damage
from services.report_service import create_report

app = FastAPI()

# ======================
# 跨域
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# 路径配置
# ======================
BASE_URL = "http://127.0.0.1:8000"
UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
REPORT_DIR = "reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
app.mount("/results", StaticFiles(directory="results"), name="results")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/reports", StaticFiles(directory="reports"), name="reports")


# ======================
# URL工具
# ======================
def to_url(path: str):

    if not path:
        return None

    path = path.replace("\\", "/")

    if path.startswith("http"):
        return path

    if path.startswith("/results"):
        return BASE_URL + path

    if path.startswith("/uploads"):
        return BASE_URL + path

    if path.startswith("reports"):
        return BASE_URL + "/" + path

    return BASE_URL + "/" + path


# =========================================================
# 文件夹上传
# =========================================================
@app.post("/upload-folder")
async def upload_folder(files: list[UploadFile] = File(...)):

    folder_id = str(uuid.uuid4())
    folder_path = os.path.join(UPLOAD_DIR, folder_id)
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        safe_name = file.filename.replace("/", "_").replace("\\", "_")
        file_path = os.path.join(folder_path, safe_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "folder_id": folder_id,
        "file_count": len(files)
    }


# =========================================================
# 文件夹分析
# =========================================================
@app.post("/start-analysis")
async def start_analysis(folder_id: str = Form(...)):

    folder_path = os.path.join(UPLOAD_DIR, folder_id)

    if not os.path.exists(folder_path):
        return {"success": False, "error": "folder not found"}

    image_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    all_results = []

    for file_path in image_files:

        try:
            # ======================
            # 每张图单独 try（关键）
            # ======================
            overall_result = analyze_overall(file_path)
            crack_result = analyze_crack(file_path)
            segment_result = analyze_segment(file_path)

            result = assess_damage(
                crack_count=crack_result.get("crack_count", 0),
                spalling_count=segment_result.get("spalling_count", 0),
                rebar_count=segment_result.get("rebar_count", 0),
                crack_length=crack_result.get("crack_length", 0),
                spalling_area=segment_result.get("spalling_area", 0),
                rebar_area=segment_result.get("rebar_area", 0)
            )

            all_results.append({
                "file": os.path.basename(file_path),

                "crack_count": crack_result.get("crack_count", 0),
                "spalling_count": segment_result.get("spalling_count", 0),
                "rebar_count": segment_result.get("rebar_count", 0),

                "damage_level": result.get("damage_name", "未知"),
                "score": result.get("score", 0),
                "suggestion": result.get("advice", "暂无建议"),

                "images": {
                    "original": to_url(file_path),
                    "final": to_url(overall_result.get("result_image"))
                }
            })

        except Exception as e:
            # ⭐关键：失败也要继续
            all_results.append({
                "file": os.path.basename(file_path),
                "error": str(e)
            })

            continue

    # ======================
    # PDF（也必须保护）
    # ======================
    try:
        pdf_path = create_report(all_results)
        pdf_path = to_url(pdf_path)
    except Exception as e:
        pdf_path = None

    return {
        "success": True,
        "results": all_results,
        "pdf_path": pdf_path
    }
# =========================================================
# 单图分析
# =========================================================
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(
            UPLOAD_DIR,
            file_id + "_" + file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        overall_result = analyze_overall(file_path)
        crack_result = analyze_crack(file_path)
        segment_result = analyze_segment(file_path)

        result = assess_damage(
            crack_count=crack_result.get("crack_count", 0),
            spalling_count=segment_result.get("spalling_count", 0),
            rebar_count=segment_result.get("rebar_count", 0),
            crack_length=crack_result.get("crack_length", 0),
            spalling_area=segment_result.get("spalling_area", 0),
            rebar_area=segment_result.get("rebar_area", 0)
        )

        response = {
            "success": True,
            "file": file.filename,

            "crack_count": crack_result.get("crack_count", 0),
            "spalling_count": segment_result.get("spalling_count", 0),
            "rebar_count": segment_result.get("rebar_count", 0),

            "damage_level": result.get("damage_name", "未知"),
            "score": result.get("score", 0),
            "suggestion": result.get("advice", "暂无建议"),

            "images": {
                "original": to_url(file_path),
                "final": to_url(overall_result.get("result_image"))
            }
        }

        # ======================
        # PDF生成（强化版）
        # ======================
        try:
            pdf_path = create_report(response)

            print("PDF原始路径:", pdf_path)

            if pdf_path and os.path.exists(pdf_path):
                response["pdf_path"] = to_url(pdf_path)
                print("PDF已加入返回:", response["pdf_path"])
            else:
                print("PDF路径无效或文件不存在")

        except Exception as e:
            print("PDF生成失败：", str(e))

        return response

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ======================
# health check
# ======================
@app.get("/")
def root():
    return {"message": "API running"}
