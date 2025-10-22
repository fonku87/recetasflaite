<script setup>
import Cabecera from '@/components/Cabecera.vue';
import Footer from '@/components/Footer.vue';
import { loginComposable } from '@/composables/useSeguridadComposable';
import { loginSchema } from '@/schemas/validacionesSchema';
import {Form, Field, ErrorMessage} from 'vee-validate';
import { ref } from 'vue';

let boton = ref('block');
let preloader = ref('none');


let nombre = ref('');
let correo = ref('');
let password = ref('');
const{sendData}= loginComposable();
let enviar = () => {
  boton.value='none';
  preloader.value='block';
sendData({nombre:nombre.value, correo:correo.value, password:password.value});
};
</script>
<template>
  <Cabecera />
  <div className="breadcumb-area bg-img bg-overlay" style="background-image: url(img/bg-img/breadcumb6.jpg)">
        <div className="container h-100">
            <div className="row h-100 align-items-center">
                <div className="col-12">
                    <div className="breadcumb-text text-center">
                        <h2>Login</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div className="contact-area section-padding-0-80">
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="section-heading">
                        <h3>Ingresa tus datos</h3>
                    </div>
                </div>
            </div>

            <div className="row">
                <div className="col-8">
                    <div className="contact-form-area">
                      <Form :validation-schema="loginSchema" @submit="enviar()">
              <div class="row">

                <div className="col-12 col-lg-12">
                  <ErrorMessage name="correo" class="text text-danger" />
                  <Field type="text"  name="correo" v-model="correo" class="form-control" placeholder="E-Mail" />
                </div>
                <div className="col-12 col-lg-12">
                  <ErrorMessage name="password" class="text text-danger" />
                  <Field type="password"  name="password" v-model="password" class="form-control" placeholder="Contraseña" />
                </div>
                <div class="col-12 text-center" :style="'display:' + boton">
                  <button class="btn delicious-btn mt-30" type="submit" title="Enviar">Enviar</button>

                </div>
                <div class="col-12 text-center" :style="'display:' + preloader">
                  <img src="/img/img/load.gif">

                </div>
              </div>
            </Form>

                    </div>
                </div>
            </div>
        </div>
    </div>
  <Footer />
</template>
