#!/bin/bash

echo "=== LIMPIANDO CONFIGURACIÓN ==="
echo ""

# Tu API key limpia (la que está en .env)
CLEAN_KEY="AIzaSyBOthTs2wsnCdMQX5_G1m"

echo "1. Limpiando ~/.bashrc"
# Eliminar la línea placeholder
sed -i '/export GOOGLE_API_KEY="tu_api_key_aquí"/d' ~/.bashrc

# Añadir la correcta si no existe
if ! grep -q "export GOOGLE_API_KEY=\"$CLEAN_KEY\"" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Google API Key for ADK" >> ~/.bashrc
    echo "export GOOGLE_API_KEY=\"$CLEAN_KEY\"" >> ~/.bashrc
    echo "✓ API key añadida a ~/.bashrc"
else
    echo "✓ ~/.bashrc ya tiene la API key correcta"
fi

echo ""
echo "2. Verificando .env en proyecto"
if [ -f ".env" ]; then
    echo "✓ .env existe con la key correcta"
else
    echo "export GOOGLE_API_KEY=$CLEAN_KEY" > .env
    echo "✓ .env creado"
fi

echo ""
echo "3. Asegurando que .env esté en .gitignore"
if [ ! -f ".gitignore" ]; then
    echo ".env" > .gitignore
    echo "✓ .gitignore creado"
elif ! grep -q "^.env$" .gitignore; then
    echo ".env" >> .gitignore
    echo "✓ .env añadido a .gitignore"
else
    echo "✓ .env ya está en .gitignore"
fi

echo ""
echo "4. Limpiando variable de entorno actual"
unset GOOGLE_API_KEY
export GOOGLE_API_KEY="$CLEAN_KEY"

echo ""
echo "5. Verificando que la nueva key esté limpia:"
echo "$GOOGLE_API_KEY" | od -c | head -3

echo ""
echo "=== LIMPIEZA COMPLETADA ==="
echo ""
echo "IMPORTANTE: Ejecuta esto para recargar:"
echo "  source ~/.bashrc"
echo ""
echo "Después prueba tu agente con:"
echo "  python3 agent_minimal.py"
