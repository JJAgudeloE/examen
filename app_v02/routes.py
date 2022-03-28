from controllers import RegisterControllers, LoginControllers, crearproductoControllers, ProductosControllers

routes = {
"register": "/api/v01/registerexam", "register_controllers": RegisterControllers.as_view("register_api"),
"login": "/api/v01/login", "login_controllers": LoginControllers.as_view("login_api"),
"crearproducto": "/api/v01/crearproducto", "crearproducto_controllers": crearproductoControllers.as_view("crearproducto_api"),
"productos": "/api/v01/productos", "productos_controllers": ProductosControllers.as_view("productos_api")
}
