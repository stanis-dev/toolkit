#!/bin/sh
set -e
cd "$(dirname "$0")"

swiftc -swift-version 5 src/*.swift -o brain

mkdir -p Brain.app/Contents/MacOS Brain.app/Contents/Resources
cp resources/Info.plist Brain.app/Contents/
cp resources/AppIcon.icns Brain.app/Contents/Resources/
printf 'APPL????' > Brain.app/Contents/PkgInfo
cp brain Brain.app/Contents/MacOS/rec
KEYCHAIN="$(cd "$(dirname "$0")" && pwd)/brain-signing.keychain"
security unlock-keychain -p "" "$KEYCHAIN"
ORIG_KEYCHAINS=$(security list-keychains -d user | tr -d '"' | tr '\n' ' ')
security list-keychains -d user -s "$KEYCHAIN" $ORIG_KEYCHAINS
codesign --force --options runtime \
  --entitlements resources/Brain.entitlements \
  --keychain "$KEYCHAIN" \
  --sign 57EC4383E8EBC5F97C4F5676DA5BF9B5D00F7BC0 Brain.app
security list-keychains -d user -s $ORIG_KEYCHAINS

rsync -a --delete Brain.app/ /Applications/Brain.app/

echo "Built brain binary and installed to /Applications/Brain.app"
