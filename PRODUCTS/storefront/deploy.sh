#!/bin/bash
cd "$(dirname "$0")"
cp index.html 200.html
npx surge . printmaxx-store.surge.sh
