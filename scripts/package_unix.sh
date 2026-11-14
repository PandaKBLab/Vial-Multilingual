#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-or-later
set -euo pipefail

version=$(sed -n 's/^PANDAKB_VERSION = "\([^"]*\)"$/\1/p' src/main/python/pandakb_i18n.py)
test -n "$version"
mkdir -p dist build/runtime
printf 'PandaKB Vial %s\nSource: https://github.com/PandaKBLab/Vial-Multilingual/tree/%s\n' "$version" "$GITHUB_SHA" > build/runtime/BUILD-INFO.txt
deps=$(python -c 'from importlib.metadata import distributions; print("\n".join(sorted(d.metadata["Name"] + "==" + d.version for d in distributions())))')
printf '%s\n' "$deps" > build/runtime/DEPENDENCIES.txt
options=(--noconfirm --clean --name Vial --paths src/main/python
  --runtime-hook scripts/pandakb_frozen_resources.py
  --add-data src/main/resources/base:.
  --add-data src/main/icons/Icon.ico:.
  --add-data src/build/settings/base.json:.
  --add-data COPYING:. --add-data NOTICE:. --add-data README.md:.
  --add-data build/translation-coverage.md:.
  --add-data build/runtime/BUILD-INFO.txt:. --add-data build/runtime/DEPENDENCIES.txt:.)

if [[ "$(uname -s)" == Darwin ]]; then
  shape=build/Vial.iconset
  mkdir -p "$shape"
  for size in 16 32; do
    cp "src/main/icons/base/$size.png" "$shape/icon_${size}x${size}.png"
    cp "src/main/icons/base/$((size * 2)).png" "$shape/icon_${size}x${size}@2x.png"
  done
  for size in 128 256 512; do
    cp "src/main/icons/mac/$size.png" "$shape/icon_${size}x${size}.png"
    cp "src/main/icons/mac/$((size * 2)).png" "$shape/icon_${size}x${size}@2x.png"
  done
  iconutil -c icns "$shape" -o build/Vial.icns
  arch=$(uname -m)
  python -m PyInstaller "${options[@]}" --distpath target --windowed --target-arch "$arch" \
    --icon build/Vial.icns --osx-bundle-identifier com.pandakb.vial src/main/python/main.py
  app=target/Vial.app
  lipo -verify_arch "$arch" "$app/Contents/MacOS/Vial"
  codesign --verify --deep --strict "$app"
  mkdir -p build/dmg
  ditto "$app" "build/dmg/PandaKB Vial.app"
  ln -s /Applications build/dmg/Applications
  hdiutil create -volname 'PandaKB Vial' -srcfolder build/dmg -ov -format UDZO \
    "dist/PandaKB-Vial-v$version-macOS-$arch.dmg"
else
  python -m PyInstaller "${options[@]}" --distpath target src/main/python/main.py
  appdir=build/Vial.AppDir
  mkdir -p "$appdir/usr/bin"
  cp -a target/Vial/. "$appdir/usr/bin/"
  install -m 755 packaging/linux/AppRun "$appdir/AppRun"
  install -m 644 packaging/linux/pandakb-vial.desktop "$appdir/pandakb-vial.desktop"
  install -m 644 src/main/icons/linux/256.png "$appdir/pandakb-vial.png"
  curl --fail --location --silent --show-error --retry 3 \
    https://github.com/AppImage/appimagetool/releases/download/1.9.1/appimagetool-x86_64.AppImage \
    -o build/appimagetool.AppImage
  curl --fail --location --silent --show-error --retry 3 \
    https://github.com/AppImage/type2-runtime/releases/download/20251108/runtime-x86_64 \
    -o build/appimage-runtime
  sha256sum -c <<'EOF'
ed4ce84f0d9caff66f50bcca6ff6f35aae54ce8135408b3fa33abfc3cb384eb0  build/appimagetool.AppImage
2fca8b443c92510f1483a883f60061ad09b46b978b2631c807cd873a47ec260d  build/appimage-runtime
EOF
  chmod +x build/appimagetool.AppImage
  ARCH=x86_64 build/appimagetool.AppImage --appimage-extract-and-run \
    --runtime-file build/appimage-runtime "$appdir" "dist/PandaKB-Vial-v$version-Linux-x86_64.AppImage"
fi
