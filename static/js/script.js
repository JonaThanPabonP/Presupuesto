const tipoSelect = document.getElementById('tipo');
const categoriaSelect = document.getElementById('categoria');

// Función para actualizar las opciones del select de categorías
function cargarCategoria() {
    // Obtener el valor seleccionado en el select de tipo
    var tipo = tipoSelect.value;
    var url = "/categorias_tipo/" + tipo;

    // Hacer la petición al servidor
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Limpiar las opciones actuales del select de categorías
            categoriaSelect.innerHTML = '<option value="" disabled selected="true">Selecciona una opción</option>';

            // Agregar las nuevas opciones
            data.forEach(categoria => {
                var option = document.createElement('option');
                option.value = categoria.nombre;
                option.textContent = categoria.nombre;
                categoriaSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error(error);
        });
}

// Actualizar las opciones del select de categorías cuando se cambia el valor del select de tipo
tipoSelect.addEventListener('change', () => {
    cargarCategoria();
});

// Actualizar las opciones del select de categorías cuando se carga la página por primera vez
if (!window.location.href.includes('/edit/')) {
    cargarCategoria();
}

