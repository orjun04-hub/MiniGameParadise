name: Build APK

on:
  push:
  workflow_dispatch:

jobs:
  build:
    # 🚀 빌도저 및 안드로이드 SDK 빌드 도구와 가장 호환성이 좋은 우분투 최신 버전으로 변경합니다.
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Free Disk Space
      run: |
        sudo rm -rf /usr/share/dotnet
        sudo rm -rf /usr/local/lib/android
        sudo rm -rf /opt/ghc
        sudo rm -rf "/usr/local/share/boost"

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    # 🚀 자바 환경을 안드로이드 구형/신형 빌드 도구 모두와 호환되는 JDK 17로 세팅합니다.
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    # 🚀 aidl 실행에 필요한 모든 32비트/64비트 크로스 컴파일 라이브러리를 하나도 빠짐없이 주입합니다.
    - name: Install System Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev libgdbm-dev libreadline-dev libffi-dev uuid-dev ccache lld g++-multilib lib32z1 lib32ncurses6 lib32stdc++6 libstdc++6

    - name: Install Buildozer and Cython
      run: |
        pip install --upgrade pip setuptools wheel
        pip install "cython<3.0.0" buildozer python-for-android

    # 🚀 라이선스 자동 동의 및 빌도저 내부 SDK 패키징 엔진 강제 연동
    - name: Build APK with Buildozer
      env:
        BUILDOZER_ACCEPT_SDK_LICENSE: "1"
        APP_ANDROID_ACCEPT_SDK_LICENSE: "1"
        ANDROID_LAUNCHER_ACCEPT_SDK_LICENSE: "1"
      run: |
        buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: package
        path: bin/*.apk
