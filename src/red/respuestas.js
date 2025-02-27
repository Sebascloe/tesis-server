exports.success = (req,res, msj, status) => {

    const statusCode = status || 200
    const mensajeOk = msj || ""

    res.status(statusCode).send({
        error: false,
        status: statusCode,
        body: mensajeOk
    })
}

exports.error = (req,res, msj, status) => {

    const statusCode = status || 500
    const mensajeOk = msj || "Error interno"
    
    res.status(statusCode).send({
        error: false,
        status: statusCode,
        body: mensajeOk
    })
}