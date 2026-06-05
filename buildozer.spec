[app]
title = MiniGameParadise
package.name = minigameparadise
package.domain = org.orjun04
source.dir = .
source.include_exts = py, ttf
version = 0.1

# 🚀 [진짜 핵심] 미래의 파이썬 3.14가 실행되는 것을 막기 위해 python3==3.11.0 으로 버전을 강제 고정합니다.
requirements = python3==3.11.0, kivy==2.3.0, kivymd==1.2.0

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# 🚀 안정적인 빌드 도구 조합 고정
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.build_tools_version = 33.0.1
android.private_storage = True
android.accept_sdk_license = 1

[buildozer]
log_level = 2
warn_on_root = 1
