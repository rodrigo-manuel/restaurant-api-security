import requests

url = "http://localhost:8091/token"
usuario = "rodrigo"
password = "alfaro"

print("Validando rate limiting en el endpoint /token...")
print(f"Usuario: {usuario}")
print(f"Limite configurado: 5 solicitudes por minuto")
print("-" * 50)

for i in range(1, 11):
    respuesta = requests.post(
        url,
        data={"username": usuario, "password": password}
    )

    codigo = respuesta.status_code

    if codigo == 200:
        print(f"Solicitud {i}: HTTP {codigo} -> aceptada correctamente")
    elif codigo == 429:
        print(f"Solicitud {i}: HTTP {codigo} -> BLOQUEADA por rate limiting")
    else:
        print(f"Solicitud {i}: HTTP {codigo} -> respuesta inesperada")

print("-" * 50)
