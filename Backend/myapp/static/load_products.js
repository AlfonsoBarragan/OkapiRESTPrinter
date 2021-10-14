// Código Javascript
function CreationsViewModel() {
    var self = this;
    self.creationsURI = 'http://0.0.0.0:8080/creations_printed';
    self.creations = ko.observableArray();

    self.miAjax = function (uri, method, data) {
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(data),
            error: function (jqXHR) {
                console.log("Se ha producido un error en una petición Ajax: " + jqXHR.status);
            }
        };

        return $.ajax(request);
    }

    // Para el get que obtiene la colección de usuarios completa NO pasamos datos 
    self.miAjax(self.creationsURI, 'GET').done(function (data) {
        for (var i = 0; i < data.creations.length; i++) {
            self.creations.push({
                idCreation:     ko.observable(data.creations[i].idCreation),
                name:           ko.observable(data.creations[i].name),
                author:         ko.observable(data.creations[i].author),
                price:          ko.observable(data.creations[i].price),
                description:    ko.observable(data.creations[i].description),
                url: ko.observable(self.creationsURI + "/" + data.creations[i].idCreation)
            });
        }
    });
}

var creationsViewModel = new CreationsViewModel();

// Nuevo Modelo de Vista para anyadir usuarios
function AnyadirUsuarioViewModel() {
    var self = this;
    self.nombreUsuario = ko.observable();
    self.email = ko.observable();
    self.estado= ko.observable(true);

    self.anyadirUsuario = function() {
        $('#anyadir').modal('hide');

        usuariosViewModel.guardarNuevo({
            nombreUsuario: self.nombreUsuario(),
            email: self.email(),
            activo: self.estado()
        });
        self.nombreUsuario("");
        self.email("");
    }
}

// Nuevo Modelo de Vista para editar usuarios
function EditarUsuarioViewModel() {
    var self = this;
    self.id = ko.observable();
    self.nombreUsuario = ko.observable();
    self.email = ko.observable();
    self.estado= ko.observable(true);

    self.mostrarUsuario = function(usuario) {
        // Lo copia antes de modificarlo
        self.usuario = usuario;
        self.id(usuario.id())
        self.nombreUsuario(usuario.nombreUsuario());
        self.email(usuario.email());
        self.estado(usuario.activo());
    }

    self.guardarModificacion = function(){
        $('#editar'). modal('hide');
        usuariosViewModel.guardarModificacion(self.usuario, {
            id: self.id(),
            nombreUsuario: self.nombreUsuario(),
            email: self.email(),
            activo: self.estado()
        })
    }
}

var editarUsuarioViewModel = new EditarUsuarioViewModel();
ko.applyBindings(creationsViewModel, $('#cuerpo')[0]);
ko.applyBindings(editarUsuarioViewModel, $('#product_details')[0]);
