# SPDX-License-Identifier: GPL-2.0-or-later
$ErrorActionPreference = 'Stop'
$bundle = (Resolve-Path 'target/Vial').Path
$versionLine = Select-String -Path 'src/main/python/pandakb_i18n.py' -Pattern '^PANDAKB_VERSION = "([0-9.]+)"$'
$version = $versionLine.Matches[0].Groups[1].Value
$package = Join-Path (Resolve-Path dist).Path "PandaKB-Vial-v$version-Windows-x64-setup.exe"
$removeList = Join-Path (Resolve-Path build).Path 'uninstall-files.nsh'
$lines = foreach ($file in Get-ChildItem -LiteralPath $bundle -File -Recurse) {
    'Delete "$INSTDIR\{0}"' -f [IO.Path]::GetRelativePath($bundle, $file.FullName)
}
$lines += foreach ($dir in (Get-ChildItem -LiteralPath $bundle -Directory -Recurse | Sort-Object { $_.FullName.Length } -Descending)) {
    'RMDir "$INSTDIR\{0}"' -f [IO.Path]::GetRelativePath($bundle, $dir.FullName)
}
$lines | Set-Content -LiteralPath $removeList -Encoding utf8
$nsis = Join-Path ${env:ProgramFiles(x86)} 'NSIS\makensis.exe'
& $nsis "/DVERSION=$version" "/DPACKAGE=$package" "/DBUNDLE=$bundle" "/DREMOVE_LIST=$removeList" 'packaging/windows/installer.nsi'
if ($LASTEXITCODE -ne 0) { throw "NSIS build failed ($LASTEXITCODE)" }

$installer = Start-Process -FilePath $package -ArgumentList '/S' -WindowStyle Hidden -Wait -PassThru
if ($installer.ExitCode -ne 0) { throw "Silent installation failed ($($installer.ExitCode))" }
$installed = Join-Path $env:LOCALAPPDATA 'PandaKB\Vial'
$zipExeHash = (Get-FileHash -LiteralPath (Join-Path $bundle 'Vial.exe')).Hash
if ((Get-FileHash -LiteralPath (Join-Path $installed 'Vial.exe')).Hash -ne $zipExeHash) {
    throw 'Installed EXE differs from the portable package.'
}
$env:QT_QPA_PLATFORM = 'windows'
$output = Join-Path (Resolve-Path build).Path 'installed-smoke'
$smoke = Start-Process -FilePath (Join-Path $installed 'Vial.exe') -ArgumentList "--pandakb-smoke-test en `"$output`"" -WindowStyle Hidden -PassThru
if (-not $smoke.WaitForExit(90000)) { Stop-Process -Id $smoke.Id; throw 'Installed app timed out.' }
if ($smoke.ExitCode -ne 0 -or -not (Test-Path (Join-Path $output 'smoke-en.json'))) { throw 'Installed app smoke test failed.' }
$sentinel = Join-Path $installed 'user-layout-test.vil'
Set-Content -LiteralPath $sentinel -Value 'User file must survive uninstall.'
$uninstall = Start-Process -FilePath (Join-Path $installed 'Uninstall.exe') -ArgumentList "/S _?=$installed" -WindowStyle Hidden -Wait -PassThru
if ($uninstall.ExitCode -ne 0 -or (Test-Path (Join-Path $installed 'Vial.exe')) -or -not (Test-Path $sentinel)) {
    throw 'Uninstall failed or did not preserve the user file.'
}
