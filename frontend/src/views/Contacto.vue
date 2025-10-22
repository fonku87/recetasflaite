<script setup>
import Cabecera from '@/components/Cabecera.vue';
import Footer from '@/components/Footer.vue';
import { useContactoComposable } from '@/composables/useContactoComposable';
import { contactoSchema } from '@/schemas/validacionesSchema';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { ref } from 'vue';

let boton = ref('block');
let preloader = ref('none');


let nombre = ref('');
let correo = ref('');
let telefono = ref('');
let mensaje = ref('');

const {sendData} = useContactoComposable()
let enviar=()=>
{
  boton.value='none';
  preloader.value='block';
sendData({nombre:nombre.value, correo:correo.value, telefono:telefono.value, mensaje:mensaje.value});
};
</script>

<template>
<Cabecera />
<div class="breadcumb-area bg-img bg-overlay" style="background-image: url(img/bg-img/breadcumb4.jpg)">
  <div class="container h-100">
      <div class="row h-100 align-items-center">
          <div class="col-12">
              <div class="breadcumb-text text-center">
                  <h2>Contáctanos</h2>
              </div>
          </div>
      </div>
  </div>
</div>


<div class="contact-information-area section-padding-80">
  <div class="container">
      <div class="row">
          <div class="col-12">
              <div class="logo mb-80">
                  <img src="/img/core-img/logo2.png" alt="" style="width: 144px;height:65px" />
              </div>
          </div>
      </div>

      <div class="row">


          <div class="col-12 col-lg-12">
            <div class="row">
              <div class="col-4">
                <div class="single-contact-information mb-30">
                  <h6>Dirección:</h6>
                  <p>Calle Real, 57 <br />San Fernando (Cádiz)</p>
                </div>
              </div>
              <div class="col-4">
                <div class="single-contact-information mb-30">
                  <h6>Teléfonos:</h6>
                  <p>666666666 <br />999999999</p>
                </div>
              </div>
              <div class="col-4">
                <div class="single-contact-information mb-30">
                  <h6>E-Mail:</h6>
                  <p>{{ 'jfonku@gmail.com' }}</p>
              </div>
              </div>
            </div>


          </div>


      </div>
  </div>
</div>
<div class="contact-area section-padding-0-80">
  <div class="container">
      <div class="row">
          <div class="col-12">
              <div class="section-heading">
                  <h3>Cuéntanos en qué te podemos ayudar!!</h3>
              </div>
          </div>
      </div>

      <div class="row">
          <div class="col-12">
              <div class="contact-form-area">
                <Form :validation-schema="contactoSchema" @submit="enviar()">
                  <div class="row">
                    <div class="col-12 col-lg-6">
                      <ErrorMessage name="nombre" class="text text-danger"/>
                      <Field type="text" class="form-control" name="nombre" id="nombre" v-model="nombre" placeholder="Nombre"  />

                    </div>

                    <div class="col-12 col-lg-6">
                      <ErrorMessage name="correo" class="text text-danger"/>
                      <Field type="text" class="form-control" name="correo" id="correo" v-model="correo" placeholder="E-Mail"  />

                    </div>
                    <div class="col-12">
                      <ErrorMessage name="telefono" class="text text-danger"/>
                      <Field type="text" class="form-control" name="telefono" id="telefono" v-model="telefono" placeholder="Teléfono"  />

                    </div>
                    <div class="col-12">
                      <ErrorMessage name="mensaje" class="text text-danger"/>
                      <Field as="textarea" class="form-control" name="mensaje" id="mensaje" v-model="mensaje" placeholder="Escribe aquí tu mensaje" cols="30" rows="10"  />

                    </div>

                    <div class="col-12 text-center" :style="'display:' +boton ">
                      <button class="btn delicious-btn mt-30" type="submit" title="Enviar">Enviar Mensaje</button>

                    </div>
                    <div class="col-12 text-center" :style="'display:' +preloader ">
                      <img src="/img/img/load.gif" >

                    </div>
                  </div>
                </Form>


              </div>
          </div>
      </div>
  </div>
</div>
<Footer/>

</template>
