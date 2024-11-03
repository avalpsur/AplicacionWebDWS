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


---PRÁCTICA 2 VIEWS---
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
