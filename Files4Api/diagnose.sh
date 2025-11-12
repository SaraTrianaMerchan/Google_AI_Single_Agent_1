#!/bin/bash

echo "=== DIAGNOSTIC SCRIPT FOR GOOGLE ADK ==="
echo ""

echo "1. Checking locale settings:"
locale
echo ""

echo "2. Checking LANG variable:"
echo "LANG=$LANG"
echo ""

echo "3. Checking LC_ALL variable:"
echo "LC_ALL=$LC_ALL"
echo ""

echo "4. Checking Python encoding:"
python3 -c "import sys; print(f'Default encoding: {sys.getdefaultencoding()}'); print(f'Filesystem encoding: {sys.getfilesystemencoding()}')"
echo ""

echo "5. Checking if Google API key is set:"
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "WARNING: GOOGLE_API_KEY not set!"
else
    # Mostrar solo los primeros y últimos 4 caracteres
    KEY_START=$(echo $GOOGLE_API_KEY | cut -c1-4)
    KEY_END=$(echo $GOOGLE_API_KEY | tail -c 5)
    echo "GOOGLE_API_KEY is set: ${KEY_START}...${KEY_END}"
    
    # Verificar si tiene caracteres raros
    if echo "$GOOGLE_API_KEY" | grep -qP '[^\x00-\x7F]'; then
        echo "ERROR: Your API key contains non-ASCII characters!"
    else
        echo "API key looks clean (ASCII only)"
    fi
fi
echo ""

echo "6. Checking Python packages:"
pip list | grep -E "google-adk|httpx|tenacity"
echo ""

echo "=== END DIAGNOSTIC ==="
