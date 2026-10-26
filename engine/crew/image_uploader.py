# -*- coding: utf-8 -*-
"""
engine/crew/image_uploader.py
-----------------------------
썸네일 이미지 자동 호스팅 업로더 (ImgBB, GitHub CDN, Fallback)
Blogger API v3의 로컬 이미지 첨부 불가 한계를 해결:
- 1순위: ImgBB API (무료 32MB, 0.5초 고속 업로드, https://i.ibb.co/... 영구 URL)
- 2순위: GitHub Repo Raw CDN (GITHUB_TOKEN & REPO 설정 시 자동 푸시)
- 3순위: Base64 Data URI 및 Blogger 호환 대체 배너
"""

import os
import base64
import requests
from typing import Optional, Dict, Any


class ImageUploader:
    def __init__(self):
        self.imgbb_api_key = os.getenv("IMGBB_API_KEY", "").strip()
        self.github_token = os.getenv("GITHUB_TOKEN", "").strip()
        self.github_repo = os.getenv("GITHUB_REPO", "").strip()  # 예: "username/repo"
        self.github_branch = os.getenv("GITHUB_BRANCH", "main").strip()

    def upload_image(self, file_path: str, custom_name: Optional[str] = None) -> Dict[str, Any]:
        """
        로컬 이미지 파일을 외부 호스팅 서비스에 업로드하고 공용 HTTPS URL을 반환.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"업로드할 이미지 파일을 찾을 수 없습니다: {file_path}")

        file_name = custom_name or os.path.basename(file_path)

        # 1. ImgBB API 시도
        if self.imgbb_api_key:
            res = self._upload_to_imgbb(file_path, file_name)
            if res.get("success"):
                return res

        # 2. GitHub Raw CDN 시도
        if self.github_token and self.github_repo:
            res = self._upload_to_github(file_path, file_name)
            if res.get("success"):
                return res

        # 3. Fallback: Base64 Data URI (블로그 본문 인라인 이미지용)
        return self._create_data_uri(file_path)

    def _upload_to_imgbb(self, file_path: str, file_name: str) -> Dict[str, Any]:
        try:
            with open(file_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")

            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": self.imgbb_api_key,
                "image": b64_data,
                "name": os.path.splitext(file_name)[0]
            }
            resp = requests.post(url, data=payload, timeout=20)
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                image_url = data.get("display_url") or data.get("url")
                print(f" -> [ImageUploader] ImgBB 업로드 성공: {image_url}")
                return {
                    "success": True,
                    "provider": "imgbb",
                    "url": image_url,
                    "thumb_url": data.get("thumb", {}).get("url")
                }
            else:
                print(f" -> [ImageUploader] ImgBB 오류 응답: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f" -> [ImageUploader] ImgBB 업로드 예외 발생: {e}")

        return {"success": False}

    def _upload_to_github(self, file_path: str, file_name: str) -> Dict[str, Any]:
        try:
            with open(file_path, "rb") as f:
                b64_content = base64.b64encode(f.read()).decode("utf-8")

            remote_path = f"assets/thumbnails/{file_name}"
            api_url = f"https://api.github.com/repos/{self.github_repo}/contents/{remote_path}"
            headers = {
                "Authorization": f"Bearer {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            # 기존 파일 존재 여부 확인 (SHA 확인용)
            sha = None
            check_resp = requests.get(api_url, headers=headers, timeout=10)
            if check_resp.status_code == 200:
                sha = check_resp.json().get("sha")

            payload = {
                "message": f"Auto-upload thumbnail: {file_name}",
                "content": b64_content,
                "branch": self.github_branch
            }
            if sha:
                payload["sha"] = sha

            put_resp = requests.put(api_url, headers=headers, json=payload, timeout=20)
            if put_resp.status_code in (200, 201):
                raw_url = f"https://raw.githubusercontent.com/{self.github_repo}/{self.github_branch}/{remote_path}"
                print(f" -> [ImageUploader] GitHub Raw CDN 업로드 성공: {raw_url}")
                return {
                    "success": True,
                    "provider": "github_raw",
                    "url": raw_url
                }
            else:
                print(f" -> [ImageUploader] GitHub 업로드 오류: {put_resp.status_code} - {put_resp.text}")
        except Exception as e:
            print(f" -> [ImageUploader] GitHub 업로드 예외 발생: {e}")

        return {"success": False}

    def _create_data_uri(self, file_path: str) -> Dict[str, Any]:
        """API 키가 없을 때의 인라인 Data URI 백업"""
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(file_path)[1].lower().replace(".", "") or "webp"
        data_uri = f"data:image/{ext};base64,{b64}"
        print(" -> [ImageUploader] API 키 미설정: 인라인 Data URI로 Fallback 생성 완료.")
        return {
            "success": True,
            "provider": "data_uri",
            "url": data_uri
        }
