const {Router} = require('express')

const respuesta = require('../../red/respuestas')

const router = Router()

router.get('/', (req,res) => {
    // res.send("Bienvenido cliente")
    respuesta.success(req,res,"todo goty", 200)
})

module.exports = router