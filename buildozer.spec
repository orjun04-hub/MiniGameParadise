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

# 🚀 [핵심 교정] 구글 서버에서 404 에러 없이 r25b 패키지를 다이렉트로 꽂아오는 정확한 명칭입니다.
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
**android.accept_sdk_license = 1**
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
