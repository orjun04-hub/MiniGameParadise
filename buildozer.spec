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

# 🚀 [핵심 수정] 빌도저가 정확히 매핑할 수 있는 공식 NDK 버전 풀네임을 적어줍니다.
android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = 1

[buildozer]
log_level = 2
warn_on_root = 1
