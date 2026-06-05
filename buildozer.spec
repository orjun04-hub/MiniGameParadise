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

# 🚀 알파벳 'y'나 참/거짓 판단을 흐리는 문자를 완벽히 제거한 표준 세팅
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = 1

[buildozer]
log_level = 2
warn_on_root = 1
