# AplicacionWebDWS


**---PRÁCTICA API REST IV---**



Usuarios:
  - Cliente: nombre de usuario -> mohcencito    contraseña -> mellamomohcen_11
      curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=mohcencito&password=mellamomohcen_11&client_id=Cliente_ID&client_secret=contraseña_clientes"

  - Empleado: nombre de usuario -> mohcencitoElEncargado    contraseña -> mellamomohcen_11
      curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=mohcencitoElEncargado&password=mellamomohcen_11&client_id=Empleado_ID&client_secret=contraseña_empleados"

  - Gerente: nombre de usuario -> mohcencitoElGerente    contraseña -> mellamomohcen_11 
      curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=mohcencitoElGerente&
      password=mellamomohcen_11&client_id=Gerente_ID&client_secret=contraseña_gerentes"

  - Admin :  curl -X POST "http://127.0.0.1:8000/oauth2/token/" -d "grant_type=password&username=admin&password=1234&client_id=admin&client_secret=admin"