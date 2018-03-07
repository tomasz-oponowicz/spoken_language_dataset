#!/usr/bin/env bash

# fail fast
set -e

TARGET=build/
rm -Rf $TARGET && mkdir $TARGET
id=$(docker create elmo)
docker cp $id:/app/noises $TARGET
docker cp $id:/app/train $TARGET
docker cp $id:/app/valid $TARGET
docker cp $id:/app/test $TARGET
docker rm -v $id
