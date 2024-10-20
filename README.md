# AplicacionWebDWS
Aplicación desarrollada durante el primer trimestre

En esta aplicación vamos a gestionar una cadena de cines y su base de datos.

En primer lugar,tenemos los cines (espacios físicos) que forman parte del grupo, con sus salas y peliculas correspondientes, además del gerente que las gestiona. Un cine tiene varias salas, mientras que una sala solo puede estar en un cine. Así mismo, una sala puede tener varias películas, mientras que una película puede estar en varias salas. 
Por su parte, un cliente puede tener asociado un carnet de socio, y este será único. 
Las películas se proyectaran en las salas, e irán asociadas a entradas que comprarán los clientes y que también quedarán registradas en la base de datos.
Los empleados (encargados o no) solo pueden estar trabajando en un cine al mismo tiempo, pero pueden encargarse de una o más salas. Las salas podrán tener más de un empleado. 
Por último, los productos que se venden en la tienda de comestibles también quedarán registrados, pudiendo ser comprados por varios clientes, pero solo a través de un proveedor.

* Lo único que no hemos visto que he añadido ha sido el on-delete: do-nothing, puesto que no quería que se eliminara la tabla de las entradas si se elimina el cliente, puesto que se podrían duplicar asientos.
