#!/bin/sh
set -e
BRAIN_DIR="$(dirname "$0")"

if [ "$1" != "--skip-tests" ]; then
  /bin/sh "$BRAIN_DIR/scripts/test.sh"
fi

swiftc -swift-version 5 "$BRAIN_DIR"/src/*.swift -o "$BRAIN_DIR/brain"

mkdir -p "$BRAIN_DIR/Brain.app/Contents/MacOS" "$BRAIN_DIR/Brain.app/Contents/Resources"
cp "$BRAIN_DIR/resources/Info.plist" "$BRAIN_DIR/Brain.app/Contents/"
cp "$BRAIN_DIR/resources/AppIcon.icns" "$BRAIN_DIR/Brain.app/Contents/Resources/"
printf 'APPL????' > "$BRAIN_DIR/Brain.app/Contents/PkgInfo"
cp "$BRAIN_DIR/brain" "$BRAIN_DIR/Brain.app/Contents/MacOS/rec"
codesign --force --options runtime \
  --entitlements "$BRAIN_DIR/resources/Brain.entitlements" \
  --sign "Apple Development: stanis.samisco@gmail.com (JZ5B5LBZ3W)" "$BRAIN_DIR/Brain.app"

rsync -a --delete "$BRAIN_DIR/Brain.app/" /Applications/Brain.app/

echo "Built brain binary and installed to /Applications/Brain.app"
