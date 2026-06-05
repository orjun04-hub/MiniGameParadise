[app]
title = MiniGameParadise
package.name = minigameparadise
package.domain = org.orjun04
source.dir = .
source.include_exts = py, ttf
version = 0.1

# 🚀 requirements는 원래대로 깨끗하게 되돌립니다.
requirements = python3, kivy==2.3.0, kivymd==1.2.0

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# 🚀 [최종 마침표] 빌도저가 올바르게 인식하는 정석 파이썬 버전 고정 문법입니다.
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.build_tools_version = 33.0.1
android.python_type = cpython
android.python_version = 3.11
android.private_storage = True
android.accept_sdk_license = 1

[buildozer]
log_level = 2
warn_on_root = 1
