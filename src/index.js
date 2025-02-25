//import express from "express"
const express = require(`express`)
const morgan = require(`morgan`)


const app = express()

app.use(morgan(`dev`))


app.get(`/:id`, (req,res) => {

    if(req.params.id === "wa"){
        return res.send(`Loggeado`)
    }
    else{
        res.sendFile(`foxy.gif`, {
            root: __dirname
        })   
    }

    })





app.listen(3000)
console.log(`Server on port ${3000}`)