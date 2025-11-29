# RELECLOUD ISW2 2025

> [!IMPORTANT]  
> *¡OJO SIGA LOS SIGUIENTES PASOS ANTES DE INICIAR LA APLICACION "RELECLOUD"!*
> 
> - *PASOS:*
>
> 1. VAYA A LA PESTAÑA DE LA EXTENSIÓN DE AZURE, PINCHE EN LA SECCION: SERVIDOR DE PostreSQL FLEXIBLE SERVER Y DESPLIEGUELA.
>
> 2. INICIE DESDE EL PORTAL DE AZURE EL SERVIDOR DE PostreSQL FLEXIBLE SERVER LLAMADO *" relecloud-web-db "* Y VAYA A LA SECCION DE BASE DE DATOS EN LA EXTENSIÓN DE AZURE DE VS CODE.
>
> 3. UNA VEZ DESPLEGADO EL MENÚ, HAGA CLICK DERECHO EN LA BASE DE DATOS LLAMADA *" relecloud-isw2-db "* Y VERÁ VARIAS BASE DE DATOS.
> 
> 4. CONECTESE A LA BASE DE DATOS LLAMADA *" djangoDB-prod "* HACIENDO CLICK DERECHO (MOSTRARÁ: "CONECT TO DATABASE"). ¡AHI PODRÁ ENCONTRAR LAS TABLAS DE LA BASE DE DATOS DE LA APLICACIÓN RELECLOUD SI SE REGISTRA COMO ADMIN!
>
> 5. VAYA A LA PESTAÑA LLAMADA APP SERVICE.
> 
> 6. RELICE EL DEPLOYMENT DE LA APP "RELECLOUD" HACIENDO CLICK DERECHO.
> 
> 7. VUELVA A HACER CLICK DERECHO SOBRE LA APP "RELECLOUD" Y PULSE START.
> 
> 8. ¡Y LISTO, YA PUEDE VER LA APLICACION RELECLOUD EN EL NAVEGADOR CON AZURE!


## Table of Contents

- [RELECLOUD ISW2 2025](#relecloud-isw2-2025)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)

## Introduction

Relecloud is a sample web application designed to demonstrate the capabilities of the Django framework + Python. It includes various features to help you get started with your own projects.

## Installation

To get started with the Relecloud project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/relecloud-isw2.git
    ```
2. Navigate to the project directory:
    ```sh
    cd relecloud-isw2
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Apply migrations:
    ```sh
    python manage.py migrate
    ```
5. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

Once the development server is running, you can access the application at `http://127.0.0.1:8000/`. Explore the features and customize the project as needed.
