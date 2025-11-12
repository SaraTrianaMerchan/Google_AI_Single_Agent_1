#!/bin/bash

echo "=== BUSCANDO LA API KEY PROBLEMÁTICA ==="
echo ""

echo "1. Checking environment variable:"
echo "GOOGLE_API_KEY actual value (first 20 chars):"
echo "$GOOGLE_API_KEY" | head -c 20 | od -c
echo ""

echo "2. Checking common config files:"
FILES=(
    "$HOME/.bashrc"
    "$HOME/.bash_profile"
    "$HOME/.zshrc"
    "$HOME/.profile"
    "$HOME/.env"
    ".env"
    "./.env"
    "$HOME/.config/gcloud/configurations/config_default"
    "$HOME/.google/credentials.json"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Checking: $file"
        if grep -q "GOOGLE_API_KEY" "$file" 2>/dev/null; then
            echo "  -> FOUND in $file"
            grep "GOOGLE_API_KEY" "$file" | head -c 50
            echo ""
        fi
    fi
done

echo ""
echo "3. Checking .env files in current directory:"
find . -maxdepth 2 -name ".env*" -type f 2>/dev/null | while read envfile; do
    echo "Found: $envfile"
    if grep -q "GOOGLE_API_KEY" "$envfile" 2>/dev/null; then
        echo "  -> Contains GOOGLE_API_KEY"
        grep "GOOGLE_API_KEY" "$envfile" | head -c 50
        echo ""
    fi
done

echo ""
echo "4. Checking if there's a .kaggle directory:"
if [ -d "$HOME/.kaggle" ]; then
    echo "Found .kaggle directory"
    ls -la "$HOME/.kaggle/"
fi

echo ""
echo "=== FIN DE LA BÚSQUEDA ==="
