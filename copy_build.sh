#!/usr/bin/env bash

TARGET=build/
rm -Rf $TARGET && mkdir $TARGET
id=$(docker create elmo)
docker cp $id:/app/noises $TARGET
docker cp $id:/app/valid $TARGET
docker rm -v $id
