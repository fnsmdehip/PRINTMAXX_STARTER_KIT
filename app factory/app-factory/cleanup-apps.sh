#!/bin/bash

# Cleanup script to fix app structures

cleanup_app() {
    local app_dir=$1
    echo "Cleaning up $app_dir..."

    cd "$app_dir"

    # If there's a nested scripture-streak folder, move its contents up
    if [ -d "scripture-streak" ]; then
        echo "Found nested scripture-streak folder in $app_dir, fixing..."

        # Move contents from nested folder to current directory
        find scripture-streak -mindepth 1 -maxdepth 1 | while read item; do
            basename_item=$(basename "$item")
            if [ -e "$basename_item" ]; then
                echo "Skipping $basename_item (already exists)"
            else
                mv "$item" .
            fi
        done

        # Remove the now-empty nested folder
        rmdir scripture-streak 2>/dev/null || echo "Could not remove scripture-streak folder"
    fi

    cd ..
}

# Clean up religious apps
cd religious-apps
for app_dir in */; do
    if [ -d "$app_dir" ]; then
        cleanup_app "$app_dir"
    fi
done
cd ..

# Clean up non-religious apps
cd non-religious-apps
for app_dir in */; do
    if [ -d "$app_dir" ]; then
        cleanup_app "$app_dir"
    fi
done
cd ..

echo "Cleanup completed!"