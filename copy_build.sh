#!/usr/bin/env bash

# fail fast
set -e

TARGET=build/
rm -Rf $TARGET && mkdir $TARGET

echo "Copying files from a docker image..."
docker run --rm -v $(pwd)/$TARGET:/host:rw sld cp -r /app/train /app/test /host

echo "Done. Execute 'make fix_permissions' in order to change the owner of samples."
