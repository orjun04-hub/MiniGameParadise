name: Build APK

on:
  push:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

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
        python-version: '3.11'

    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Install System Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev libgdbm-dev libreadline-dev libffi-dev uuid-dev ccache lld g++-multilib lib32z1 lib32ncurses6 lib32stdc++6 libstdc++6

    - name: Install Buildozer and Cython
      run: |
        pip install --upgrade pip setuptools wheel
        pip install "cython<3.0.0" buildozer python-for-android

    # 🚀 [오류 해결] 뼈대 폴더를 깨뜨리는 android clean 명령을 빼고, 곧바로 무결성 빌드에 진입합니다.
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
