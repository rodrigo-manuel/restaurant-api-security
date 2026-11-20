# Seguridad de APIs: mitigación de la falta de límite de solicitudes (OWASP API4:2023)

Trabajo en equipo de la asignatura Optativa (Ingeniería de Software, Universidad Cooperativa de Colombia, 2026). Cada integrante analizó, explotó de forma ética y mitigó una vulnerabilidad del OWASP API Security Top 10 (2023) en [Damn Vulnerable RESTaurant API](vulnerable-app/), una API intencionalmente vulnerable.

| Rama | Vulnerabilidad |
|---|---|
| `member-1-hashing` | Hashing débil de contraseñas |
| `member-2-jwt` | JWT inseguro |
| **`member-3-rate-limit`** | **Falta de límite de solicitudes (esta rama, mi parte)** |
| `member-4-authz` | Escalada de privilegios |

## Mi parte: API4:2023, Unrestricted Resource Consumption

**Autor:** Rodrigo Manuel Alfaro Giraldo

**Problema.** El endpoint de autenticación `POST /token` aceptaba solicitudes ilimitadas. Eso permitía ataques automatizados de fuerza bruta contra las contraseñas y el consumo excesivo de recursos del servidor.

**Explotación.** Con un script de PowerShell envié solicitudes automatizadas seguidas al endpoint: la API respondió todas, sin bloqueos ni respuestas HTTP 429.

**Mitigación.** Agregué limitación de solicitudes por dirección IP con [SlowAPI](https://github.com/laurentS/slowapi):

- [`app/rate_limiting.py`](vulnerable-app/app/rate_limiting.py): crea el `Limiter` con la IP del cliente como clave.
- [`app/init_app.py`](vulnerable-app/app/init_app.py): registra el limitador y el manejador de `RateLimitExceeded` en la aplicación FastAPI.
- [`app/apis/auth/services/get_token_service.py`](vulnerable-app/app/apis/auth/services/get_token_service.py): aplica `@limiter.limit("5/minute")` al endpoint `/token`.

**Validación.** Después de la mitigación, las primeras cinco solicitudes por minuto se atienden y las siguientes se rechazan con HTTP 429:

```txt
Rate limit exceeded: 5 per 1 minute
```

## Tecnologías

Python 3.10, FastAPI, PostgreSQL, Docker, SlowAPI, Swagger/OpenAPI, PowerShell.

## Ejecutar

```bash
cd vulnerable-app
docker compose up --build
```

La documentación interactiva de la API queda en `http://localhost:8091/docs` (puerto definido en `docker-compose.yml`).

## Reflexión

La falta de controles básicos, como un límite de solicitudes, compromete la disponibilidad del sistema y facilita el robo de cuentas. Estos controles deben diseñarse desde el inicio del desarrollo, no agregarse después de un incidente.

---

API vulnerable original: Damn Vulnerable RESTaurant API Game, con su propia licencia en [`vulnerable-app/LICENSE`](vulnerable-app/LICENSE).
