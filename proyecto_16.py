from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pathlib import Path



def llamada_genai(mensaje_inicial=None):
    load_dotenv(Path(__file__).resolve().parent / ".env")
    cliente = genai.Client()
    historial = []
    configuracion = types.GenerateContentConfig(
        system_instruction="Eres un analista de datos profesional"
    )

    while True:
        if mensaje_inicial is not None:
            mensaje = mensaje_inicial.strip()
            mensaje_inicial = None
        else:
            mensaje = input("tu: ").strip()
        if mensaje.lower() == "quit":
            print("adios")
            break
        if not mensaje:
            continue

        historial_temporal = historial + [
            {"role": "user", "parts": [{"text": mensaje}]}
        ]
        texto_completo = ""
        print("Gemini: ", end="", flush=True)

        try:
            respuesta = cliente.models.generate_content_stream(
                model="gemini-3.5-flash-lite",
                contents=historial_temporal,
                config=configuracion,
            )
            for chunk in respuesta:
                texto = chunk.text
                if texto:
                    print(texto, end="", flush=True)
                    texto_completo += texto
        except APIError as error:
            print()
            if error.code == 503:
                print("Servidor ocupado. Intenta enviar tu mensaje nuevamente.")
            else:
                print(f"Error de la API ({error.code}): {error.message}")
            # No guardar un intercambio fallido ni una respuesta parcial.
            continue

        print()
        if not texto_completo.strip():
            print("No se recibio una respuesta de texto. Intenta nuevamente.")
            continue

        historial = historial_temporal + [
            {"role": "model", "parts": [{"text": texto_completo}]}
        ]


if __name__ == "__main__":
    llamada_genai()
