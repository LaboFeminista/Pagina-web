<script setup>
import { ref } from 'vue'
import viteLogo from '../assets/vite.svg'
import heroImg from '../assets/hero.png'
import vueLogo from '../assets/vue.svg'


const count = ref(0)
</script>

<template>
    <section id="titulo-tarjeta-dinamica">
        <div>
            <h1>TITULO</h1>
        </div>
    </section>

    <section id="imagen-tarjeta-dinamica">
        <div class="imagen-actividad">            
            <img :style="{width:'100%'}" :src="vueLogo" alt="" />
        </div>
    </section>

    <section id="actividad-tarjeta-dinamica">
        <div>
            <h1>DÍA</h1>
            <h1>HORA</h1>
            <h1>DESCRIPCIÓN</h1>
        </div>
    </section>
    


</template>