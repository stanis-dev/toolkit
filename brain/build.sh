#!/bin/sh
set -e
cd "$(dirname "$0")"

if [ "$1" != "--skip-tests" ]; then
  ./scripts/test.sh
fi

swiftc -swift-version 5 src/*.swift -o brain

mkdir -p Brain.app/Contents/MacOS Brain.app/Contents/Resources
cp resources/Info.plist Brain.app/Contents/
cp resources/AppIcon.icns Brain.app/Contents/Resources/
printf 'APPL????' > Brain.app/Contents/PkgInfo
cp brain Brain.app/Contents/MacOS/rec
codesign --force --options runtime \
  --entitlements resources/Brain.entitlements \
  --sign "Apple Development: stanis.samisco@gmail.com (JZ5B5LBZ3W)" Brain.app

rsync -a --delete Brain.app/ /Applications/Brain.app/

echo "Built brain binary and installed to /Applications/Brain.app"
