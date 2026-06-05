[app]
title = MiniGameParadise
package.name = minigameparadise
package.domain = org.orjun04
source.dir = .
source.include_exts = py, ttf
version = 0.1
requirements = python3, kivy==2.3.0, kivymd==1.2.0
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# 🚀 [진짜 최종 합의] 에러를 일으키는 python_type 줄을 지우고 버전만 깔끔하게 명시합니다.
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.build_tools_version = 33.0.1
android.python_version = 3.11
android.private_storage = True
android.accept_sdk_license = 1
# ... 기존 설정들 ...
# 이 줄을 [app] 섹션에 추가하세요:
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

[buildozer]
log_level = 2
warn_on_root = 1
