#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Preserve the tested package bytes and publish one checksum list for all platforms.
set -euo pipefail
tag="${1:?version tag}"
packages="${2:?package artifact directory}"
dist="${3:?output directory}"
[[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]
mkdir -p "$dist"
(cd "$packages/PandaKB-Vial-Windows-x64" && sed 's/\r$//' SHA256SUMS.txt | sha256sum --check --strict)
files=()
for platform in Windows-x64 Linux-x86_64 macOS-arm64 macOS-x86_64; do
  case "$platform" in
    Windows-x64) suffixes=(setup.exe portable.zip);;
    Linux-x86_64) suffixes=(AppImage);;
    macOS-*) suffixes=(dmg);;
  esac
  for suffix in "${suffixes[@]}"; do
    separator=-
    if [[ "$suffix" == AppImage || "$suffix" == dmg ]]; then separator=.; fi
    name="PandaKB-Vial-$tag-$platform$separator$suffix"
    test -s "$packages/PandaKB-Vial-$platform/$name"
    cp "$packages/PandaKB-Vial-$platform/$name" "$dist/"
    files+=("$name")
  done
done
(cd "$dist" && sha256sum "${files[@]}" > SHA256SUMS.txt && sha256sum --check --strict SHA256SUMS.txt)
