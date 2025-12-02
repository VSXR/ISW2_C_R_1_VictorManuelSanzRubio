# Relecloud ISW2

**Relecloud ISW2** es una aplicación web desarrollada con Django como parte de las prácticas de la asignatura **Ingeniería del Software II**.

## Índice

- [Relecloud ISW2](#relecloud-isw2)
  - [Índice](#índice)
  - [Requisitos del Proyecto](#requisitos-del-proyecto)
    - [Instalación de Dependencias](#instalación-de-dependencias)
  - [Ejecución del Servidor](#ejecución-del-servidor)
  - [Pruebas](#pruebas)
    - [Ejecución de Pruebas Unitarias](#ejecución-de-pruebas-unitarias)
  - [Despliegue](#despliegue)

## Requisitos del Proyecto

Antes de empezar, asegúrate de tener instalados:

- **Python** (versión 3.12)
- **pip** (gestor de paquetes de Python)
- **virtualenv** (para crear entornos virtuales)

### Instalación de Dependencias

1. Crea un entorno virtual en el directorio del proyecto:

   ```powershell
   python -m venv .venv
   ```

2. Activa el entorno virtual:

   - En **Linux/macOS**:
     ```sh
     source .venv/bin/activate
     ```
   - En **Windows**:
     ```powershell
     .venv\Scripts\activate
     ```

3. Instala las dependencias definidas en `requirements.txt`:
   ```powershell
   pip install -r requirements.txt
   ```

## Ejecución del Servidor

Para iniciar el servidor de desarrollo local:

```sh
python manage.py runserver
```

Una vez ejecutado, podrás acceder a la aplicación en [http://localhost:8000](http://localhost:8000).


## Pruebas

### Ejecución de Pruebas Unitarias

Antes de ejecutar las pruebas:

1. Asegúrate de que la base de datos de pruebas esté correctamente configurada.

2. Instala `pytest` si no lo tienes instalado:
    ```sh
    pip install pytest
    ```
3. Ejecuta las pruebas utilizando `pytest`:
    ```sh
    pytest
    ```

## Despliegue

El proyecto está configurado para ser desplegado en **Azure**. La configuración del pipeline de despliegue se encuentra en el archivo `azure-pipelines.yml`.

Para más detalles, consulta la documentación oficial de Azure Pipelines.