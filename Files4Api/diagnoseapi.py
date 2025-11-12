#!/usr/bin/env python3
"""
Diagnóstico detallado del problema con Google Gemini API
"""

import os
import sys
import json

def main():
    print("=== DIAGNÓSTICO DE API KEY ===\n")
    
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY no está configurada")
        sys.exit(1)
    
    print(f"✓ API Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"  Longitud: {len(api_key)} caracteres")
    print()
    
    # Intentar una llamada directa a la API REST de Gemini
    print("=== PROBANDO CONEXIÓN DIRECTA A GEMINI API ===\n")
    
    try:
        import requests
    except ImportError:
        print("⚠️  requests no instalado. Instalando...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
        import requests
    
    # URL de la API de Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! Say 'API works' in Spanish."
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Enviando petición a: {url[:60]}...")
    print()
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("✓ ¡ÉXITO! La API key funciona correctamente")
            data = response.json()
            if 'candidates' in data:
                text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"\nRespuesta de Gemini: {text}")
            print("\n=== TU API KEY ES VÁLIDA ===")
            print("El problema está en la configuración del Google ADK")
            return True
            
        elif response.status_code == 400:
            error_data = response.json()
            print("❌ ERROR 400 - Bad Request")
            print(f"\nRespuesta completa:")
            print(json.dumps(error_data, indent=2))
            
            if 'error' in error_data:
                error = error_data['error']
                message = error.get('message', '')
                status = error.get('status', '')
                
                print(f"\nEstado: {status}")
                print(f"Mensaje: {message}")
                
                if 'API_KEY_INVALID' in status or 'API key not valid' in message:
                    print("\n🔍 DIAGNÓSTICO:")
                    print("  1. La API key existe pero no es válida para Gemini")
                    print("  2. Posibles causas:")
                    print("     - API key de un servicio diferente (no Gemini)")
                    print("     - API key restringida a IPs/dominios específicos")
                    print("     - Generative Language API no habilitada")
                    print("\n💡 SOLUCIÓN:")
                    print("  1. Ve a: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
                    print("  2. Asegúrate de seleccionar el proyecto correcto (arriba izquierda)")
                    print("  3. Click en ENABLE si no está habilitada")
                    print("  4. Espera 1-2 minutos y vuelve a probar")
            return False
            
        elif response.status_code == 403:
            print("❌ ERROR 403 - Forbidden")
            print("La API key no tiene permisos para usar Gemini API")
            print("\n💡 SOLUCIÓN:")
            print("  1. Verifica que estés en el proyecto correcto")
            print("  2. Ve a: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
            print("  3. Habilita la API")
            return False
            
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - La petición tardó demasiado")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1)
