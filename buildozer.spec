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

# Gradle 버전 충돌 방지를 위한 API 및 빌드 버전 강제 고정
android.api = 33
android.minapi = 21
android.ndk_api = 24
android.private_storage = True
android.accept_sdk_license = 1

# [핵심 수정] 에러 메시지가 요구한 Gradle 8.0 이상 버전을 강제로 주입합니다.
android.gradle_dependencies = 
android.gradle_version = 8.0
android.android_gradle_plugin_version = 8.1.0

[buildozer]
log_level = 2
warn_on_root = 1
