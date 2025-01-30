# AplicacionWebDWS
Aplicación desarrollada durante el primer trimestre

En esta aplicación vamos a gestionar una cadena de cines y su base de datos.

- En primer lugar,tenemos los cines (espacios físicos) que forman parte del grupo, con sus salas y peliculas correspondientes, además del gerente que las gestiona.

- Un cine tiene varias salas, mientras que una sala solo puede estar en un cine. Así mismo, una sala puede tener varias películas, mientras que una película puede estar en varias salas. 

- Por su parte, un cliente puede tener asociado un carnet de socio, y este será único.
  
- Las películas se proyectaran en las salas, e irán asociadas a entradas que comprarán los clientes y que también quedarán registradas en la base de datos.

- Los empleados (encargados o no) solo pueden estar trabajando en un cine al mismo tiempo, pero pueden encargarse de una o más salas. Las salas podrán tener más de un empleado.

- Por último, los productos que se venden en la tienda de comestibles también quedarán registrados, pudiendo ser comprados por varios clientes, pero solo a través de un proveedor.

* Lo único que no hemos visto que he añadido ha sido el on-delete: do-nothing, puesto que no quería que se eliminara la tabla de las entradas si se elimina el cliente, puesto que se podrían duplicar asientos.


**---PRÁCTICA 2 VIEWS---**
En esta práctica vamos a incluir 10 URLs que deben cumplir diferentes criterios que iremos comentando.

1. Una URL que muestra todos los socios registrados con todos sus datos.
   Esta URL sirve a modo de introducción para sacar todos los datos de una tabla (socio) que se relaciona 1:1 con otra tabla (cliente). Como a todos los socios son clientes, esta query no solo nos mostrará las credenciales como socio, sino que también nos mostrará sus datos de cliente.
   

2. Una  URL que muestre todas las salas de un cine pasado como parámetro.
   Aquí trabajamos con las relaciones 1:M entre cine y sala, mostrando todas las salas de un cine en concreto.


3. Una URL que muestre todas las proyecciones de una sala en un día en concreto ordenadas de manera ascendente.
   Así incluimos el order-by en las querys.


4. Una URL que muestre todos los clientes que no son socios.
   En esta URL trabajamos la relación entre dos tablas donde no hay coincidencias (None).

5. Una URL que muestre la última proyección de un cine en concreto.
   En esta utilizamos el limit 1 y el orden en sentido descendente.

6. Una URL que muestre el salario medio de todos los empleados.
   Aquí trabajamos con el aggregate, el cual no hemos visto en clase.

7. Una URL que muestre las salas en la que se proyectarán películas cuya sinopsis empiece por un texto pasado como parámetro.
   Volvemos a trabajar con relaciones many-to-many.

8. Lista de películas de más de 3 horas que se proyecten en una sala en concreto
  Añadimos el AND a las queries.

9. Lista de salas de un cine pero de forma reversa.

10. Lista de encargados o empleados con un sueldo mayor a 1300 euros de un cine en concreto.

**Lo único que no hemos visto en clase es el timedelta, que lo he tenido que utilizar para condicionar las horas de proyección de las películas porque el atributo era de tipo Duration**


**---PRÁCTICA 3 TEMPLATES---**

- Para cumplir la condición de los template tags, encontramos un "for" con cada lista, varios "if-else" (por ejemplo en empleado.html), "include" para añadir un .html completo (así es como reutilizo código en las listas), "block" para añadir contenido específico de cada página a la plantilla principal, "extends" para que hereden de ella el resto y "load" para cargar archivos estáticos.

- He utilizado los operadores >, ==, != y or en empleado y "and" en cliente.

- Para los template filters he usado "capfirst" para nombres y apellidos, "cut" para quitar espacios en el NUSS, "upper" para que las letras del IBAN estén siempre en mayúsculas, "default" para poner una sinopsis por defecto, "timesince" para calcular desde hace cuanto lleva la película estrenada, "default_if_none" para que ponga un mensaje por defecto si no hay un tiempo de película establecido, "date" y "time" para ordenar las fechas, "title" para poner el título de la película en formato título y "lower" para poner en minúsculas el tamaño de la sala.

**Toda la información para añadir filtros y template tags la he extraido de los apuntes y la documentación oficial de Django**

**---PRÁCTICA 4 FORMULARIOS---***
- Respecto a las validaciones, se han tenido en cuenta los siguientes campos:
  Socio:
    Validación de campos obligatorios: DNI, Nombre, Apellidos.
    Validación de formato: DNI debe tener 9 caracteres.
Cliente:
  Validación de formato: El correo electrónico debe tener el formato correcto.
  Validación de longitud máxima de los campos: Nombre y Apellidos.
Película:
  Validación de campos obligatorios: Título, Director.
  Validación de longitud máxima: Título (100 caracteres).
Empleado:
  Validación de formato: Número de teléfono debe tener 9 dígitos.
  Validación de campo obligatorio: NUSS (Número de Seguridad Social).
Gerente:
  Validación de campos obligatorios: Nombre, Apellidos.
  Validación de formato: Teléfono debe tener 9 dígitos.
Cine:
  Validación de campos obligatorios: Dirección, Teléfono.
  Validación de formato: El email debe tener el formato correcto

- Se han utilizado diferentes widgets en los formularios, garantizando que los formularios sean visualmente atractivos y fáciles de usar. Los widgets utilizados son los siguientes:
Textarea: Para campos de texto largo (por ejemplo, descripción de una película).
Input de tipo number: Para ingresar datos numéricos (por ejemplo, salario de un empleado).
Select: Para elegir opciones predefinidas de una lista (por ejemplo, seleccionar un cine o sala).
Checkbox: Para seleccionar opciones booleanas (por ejemplo, si un empleado es encargado).
DateInput: Para elegir fechas (por ejemplo, fecha de alta del socio).
FileInput: Para subir imágenes o archivos (por ejemplo, imágenes asociadas a una película o cine).


**---PRÁCTICA 5 SESIONES Y AUTENTICACIÓN---**
- Incluir al menos dos tipos de usuarios claramente diferenciados (No cuenta el usuario administrador):
Se han definido tres tipos de usuarios: CLIENTE, EMPLEADO y GERENTE en el modelo Usuario.

- En cada vista controlarse los permisos y si el usuario está logueado o no:
Las vistas están decoradas con @login_required y @permission_required para controlar los permisos y la autenticación.

- En cada template de vista y formulario controlarse los permisos y si el usuario está logueado o no:
Los templates utilizan {% if request.user.is_authenticated %} y {% if perms.GestionCine.add_* %} para controlar los permisos y la autenticación.

- Incluir al menos 4 variables que se guarden en la sesión y que aparezcan siempre en la cabecera de la página. Y se eliminen cuando se desloguea el usuario:
Se han agregado variables de sesión en la vista index y se muestran en la cabecera de la página, eliminándose al desloguearse.

- Debemos hacer un registro de los distintos tipos de usuario, salvo el administrador, con sus validaciones correspondientes, y controlar que dependiendo del tipo de usuario tendrá unos valores u otros:
El formulario RegistroForm y la vista registrar_usuario manejan el registro de diferentes tipos de usuarios con validaciones específicas.

- Debemos hacer un login y logout del usuario:
La aplicación tiene vistas y templates para login y logout.

- Debe crearse una funcionalidad en algún formulario, que el contenido de algún select ManyToMany o ManyToOne varíe dependiendo del usuario que está logueado:
El formulario EntradaForm filtra las proyecciones disponibles según el cliente del usuario logueado.

- En los formularios de crear debe incluirse siempre el usuario que crea dicho registro por la sesión del usuario:
Las vistas de creación de entradas, clientes, empleados, etc., asignan el usuario logueado al registro antes de guardarlo.

- Debe crearse una funcionalidad en algún formulario de búsqueda, que el contenido se filtre por el usuario que está logueado:
La vista buscar_entrada filtra las entradas asociadas al cliente del usuario logueado.

- Implementar funcionalidad de reinicio de contraseña:
Se ha implementado la funcionalidad de reinicio de contraseña utilizando el backend de correo electrónico de consola y se ha agregado una opción en el menú para restablecer la contraseña.

**---PRÁCTICA 6 API REST I---**
- En esta practica tenemos que crear una api en nuestro servidor y obtener los datos desde una aplicación cliente. Para ello he creado una aplicación cliente nueva (puntos 1 y 2 de la tarea).

- En cuanto a las consultas, he utilizado 4 modelos de mi aplicación principal (cliente, cine, sala y película), de los cuales 3 tienen relaciones entre ellos que usaremos para mostrar las consultas mejoradas (puntos 3, 4 Y 7).

- He creado un token mediante OAUTH2 (punto 5).

- He generado una variable de entorno para cada tipo de usuario en el cliente. Para poder acceder a las claves, he tenido que crear una aplicación del oauth2/applications con CADA TIPO DE USUARIO. Con esas credenciales y con la clave de cada uno (expuestas más abajo), he generado un token para cada uno. Cada variable coge el valor de su token y se utiliza en las views. (punto 6)

- He utilizado Simple JWT para securizar mi API. Para ello, simplemente he seguido los pasos de la documentación oficial (https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html) y he utilizado el token generado en la request de la lista de clientes. Estos pasos se resumen en instalar SimpleJWT, modificar la configuración en el settings.py y en miweb/urls.py añadir el enlace para obtener los tokens. 
Hecho esto, solo queda generar el token en el cliente y pegarlo en nuestra view.(punto 8)

Usuarios:
  - Cliente: nombre de usuario -> mohcencito    contraseña -> mellamomohcen_11
      curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=mohcencito&password=mellamomohcen_11&client_id=Cliente_ID&client_secret=contraseña_clientes"

  - Empleado: nombre de usuario -> mohcencitoElEncargado    contraseña -> mellamomohcen_11
      curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=mohcencitoElEncargado&password=mellamomohcen_11&client_id=Empleado_ID&client_secret=contraseña_empleados"

  - Gerente: nombre de usuario -> mohcencitoElGerente    contraseña -> mellamomohcen_11 
      curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=mohcencitoElGerente&
      password=mellamomohcen_11&client_id=Gerente_ID&client_secret=contraseña_gerentes"
