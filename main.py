name: Build APK

on:
  push:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Install System Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev libgdbm-dev libreadline-dev libffi-dev uuid-dev ccache lld g++-multilib lib32z1 lib32ncurses6 lib32stdc++6 libstdc++6 tar

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install Buildozer
      run: |
        pip install --upgrade pip
        pip install buildozer

    - name: Build APK
      run: |
        # 메모리 부족 방지를 위해 컴파일 병렬 스레드 수를 1로 고정
        export MAKEFLAGS="-j1"
        export BUILDOZER_ACCEPT_SDK_LICENSE=1
        export CC=/usr/bin/gcc
        export CXX=/usr/bin/g++
        
        # 캐시 삭제 후 빌드
        rm -rf .buildozer
        buildozer -v android debug

    - name: Upload Artifacts
      uses: actions/upload-artifact@v4
      with:
        name: package
        path: bin/*.apk
