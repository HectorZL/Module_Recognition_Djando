# Sistema de Reconocimiento Facial para Instituciones

Sistema avanzado de reconocimiento facial diseñado para instituciones educativas, corporativas y gubernamentales que requieran control de acceso y registro de asistencia mediante reconocimiento biométrico facial.

## 🚀 Características Principales


- **Registro de asistencia automático(Logs)**
- **Detección de intentos de suplantación**
- **Interfaz web administrativa**
- **Reportes y análisis de acceso**
- **Soporte para múltiples cámaras**
- **Integración con sistemas de seguridad**

## 📋 Requisitos del Sistema

- Python 3.8 o superior
- PostgreSQL/MongoDB
- Nginx (para producción)
- GPU NVIDIA (recomendado para mejor rendimiento)

## 🛠️ Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/tu-institucion/sistema-reconocimiento-facial.git
cd sistema-reconocimiento-facial
```

2. Crear un entorno virtual

```bash
python -m venv venv
```

3. Activar el entorno virtual

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

4. Instalar dependencias

```bash
pip install -r requirements.txt
```

5. Configurar variables de entorno

```bash
cp .env.example .env
# Editar el archivo .env con tus configuraciones
```

6. Aplicar migraciones

```bash
python manage.py migrate
```

7. Crear usuario administrador

```bash
python manage.py createsuperuser
```

8. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

## 🏗️ Estructura del Proyecto

```
sistema-reconocimiento/
├── core/                   # Configuración principal
├── recognition/           # Lógica de reconocimiento facial
├── dashboard/             # Panel de administración
├── api/                   # Endpoints de la API
├── static/                # Archivos estáticos
├── media/                 # Imágenes y modelos
├── templates/             # Plantillas HTML
├── manage.py
└── requirements.txt
```

## 🔐 Variables de Entorno

Configura las siguientes variables en producción:

- `SECRET_KEY`
- `DEBUG` (establecer a False en producción)
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `FACE_ENCODING_MODEL`
- `MAX_FACE_DISTANCE`
- `CAMERA_SOURCES`

## 🖥️ Módulos Principales

- **Sistema de Reconocimiento**: Procesamiento de imágenes y detección facial
- **Gestión de Usuarios**: Registro y administración de perfiles
- **Control de Acceso**: Restricciones por horarios y zonas
- **Reportes**: Generación de informes de asistencia
- **API REST**: Integración con otros sistemas

## 🔒 Seguridad

- Cifrado de datos biométricos
- Autenticación de dos factores
- Registro de eventos de seguridad
- Cumplimiento con RGPD/LGPD
- Encriptación de datos sensibles

## 📊 Base de Datos

El sistema soporta múltiples motores de base de datos:

- PostgreSQL (recomendado para producción)
- SQLite (solo para desarrollo)
- MongoDB (para almacenamiento de vectores faciales)

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor lee nuestra [guía de contribución](CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

Para soporte técnico, por favor contacte a:

- Email: soporte@institucion.com
- Teléfono: +1 234 567 8900
- Horario de atención: Lunes a Viernes, 9:00 - 18:00

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Licença

This project is under the MIT license. View the archive `LICENSE` for more details.

## 👥 Author

Cafu Dev - [Emicy963](https://github.com/Emicy963)
