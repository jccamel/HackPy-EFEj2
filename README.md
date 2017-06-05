# Hacking con Python
## Examen Final - Ejercicio 2

Crear una herramienta de pentesting con Python que permita ejecutar las siguientes tareas:
1. Dada una dirección IP o un nombre de dominio, encontrar información relacionada con el propietario de dicho dominio 
y los registros DNS correspondientes.
2. Ejecutar un proceso de geolocalización para encontrar las coordenadas (latitud y longitud) del objetivo en cuestión.
3. Ejecutar un escaneo con Nmap contra el objetivo y complementar la información obtenida utilizando los servicios de 
Shodan (shodan.io) y censys (censys.io).
4. En el caso de encontrar puertos que frecuentemente se relacionan con servidores web (80, 8080, 443, 10000) realizar 
una petición HTTP utilizando el método OPTIONS para determinar si efectivamente, el objetivo es un servidor web y 
extraer los métodos HTTP soportados.
5. Ejecutar un proceso de scraping contra el servidor web encontrado. Almacenar los documentos PDF e imágenes 
encontradas.
6. Paralelamente crear un proceso que se encargue de recoger los documentos e imágenes del directorio donde se 
almacenan los documentos y posteriormente extraer sus metadatos.
7. En el caso de encontrar puertos que frecuentemente se relacionan con servidores SSH (22) realizar una conexión 
y obtener el banner devuelto por el servidor para determinar si realmente se trata de un servidor SSH.
8. Ejecutar un proceso de fuerza bruta utilizando usuarios y contraseñas comunes. HINT: Utilizar el proyecto 
[FuzzDB](https://code.google.com/p/fuzzdb/)
9. Almacenar en un fichero de texto las credenciales de acceso en el caso de que el proceso anterior sea exitoso.

### Nota
+ La herramienta debe de poder ejecutarse sobre sistemas windows y linux.
* El estudiante deberá entregar el código fuente completo y además, un documento en el que se explique detalladamente 
el proceso de desarrollo y las funcionalidades de la herramienta.
