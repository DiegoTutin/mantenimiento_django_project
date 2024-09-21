const txtBuscarCliente = document.getElementById("txtBuscarCliente");
const resultadosClientes = document.getElementById("resultadosClientes");

const buscarClientes = async () => {
    try {
        const response = await fetch("obtener_clientes/" + txtBuscarCliente.value);
        const data = await response.json();
        if (data.message === 'Encontrados') {
            let listaResultados = ``;
            data.clientes.forEach((cliente) => {
                listaResultados += `<div class="resultado" data-id="${cliente.id}">${cliente.nombres} ${cliente.apellidos} - ${cliente.numero_identificacion}</div>`;
            });
            resultadosClientes.innerHTML = listaResultados;
            resultadosClientes.style.display = "block";
        } else {
            resultadosClientes.innerHTML = `<div class="resultado">No encontrado</div>`;
            resultadosClientes.style.display = "block";
        }
    } catch (error) {
        console.log(error);
    }
};

txtBuscarCliente.addEventListener("input", buscarClientes);

resultadosClientes.addEventListener("click", (event) => {
    if (event.target.classList.contains("resultado")) {
        const idCliente = event.target.getAttribute("data-id"); // Obtiene el ID del cliente del atributo data-id
        const textoResultado = event.target.textContent.trim(); // Texto completo del resultado
        const nombreApellido = textoResultado.split(" - ")[0]; // Extrae nombre y apellido del resultado
        const numeroIdentificacion = textoResultado.split(" - ")[1]; // Extrae el número de identificación del resultado

        txtBuscarCliente.value = nombreApellido; // Establece el nombre y apellido en el input de búsqueda
        document.getElementById("inputNumeroIdentificacion").value = numeroIdentificacion; // Establece el número de identificación en el input dentro del div col-sm-4

        resultadosClientes.style.display = "none"; // Oculta los resultados
        console.log("ID DEL CLIENTE = ",idCliente);
    }
});

window.addEventListener("click", (event) => {
    if (!event.target.matches("#resultadosClientes") && !event.target.matches("#txtBuscarCliente")) {
        resultadosClientes.style.display = "none";
    }
});

window.addEventListener("load", async () => {
    
});
