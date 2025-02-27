//import express from "express"
const express = require(`express`)
const morgan = require(`morgan`)
const clientes = require('./modules/clientes/rutas.js')

const app = require('./app.js')
// const port = 3000


app.use(morgan(`dev`))

app.get(`/:id`, (req,res) => {

    if(req.params.id === "wa"){
        return res.send(`Loggeado`)
    }
    else if(req.params.id === "2") {

        res.sendFile('Foxy.wav', {
            root:__dirname
        })
    }
    else{
        // res.set('Foxy.wav')
        res.sendFile(`foxy.gif`, {
            root: __dirname
        })   
    }

    })

app.use('/api/cliente', clientes)



app.listen(app.get('port'), () => {
    console.log(`Server on port ${app.get('port')}`)
})
