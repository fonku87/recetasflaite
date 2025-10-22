import * as yup from 'yup';
export const contactoSchema = yup.object({
  nombre: yup.string().required("El campo nombre es obligatorio"),
  correo: yup.string().required("El campo E-Mail es obligatorio").email("El E-Mail ingresado no es válido"),
  telefono: yup.string().required("El campo teléfono es obligatorio"),
  mensaje: yup.string().required("El campo mensaje es obligatorio")
});

export const registroSchema = yup.object({
  nombre: yup.string().required("El campo nombre es obligatorio"),
  correo: yup.string().required("El campo E-Mail es obligatorio").email("El E-Mail ingresado no es válido"),
  password: yup.string().required("El campo Contraseña es obligatorio")

});
export const loginSchema = yup.object({
  correo: yup.string().required("El campo E-Mail es obligatorio").email("El E-Mail ingresado no es válido"),
  password: yup.string().required("El campo Contraseña es obligatorio")

});
export const recetasSchema = yup.object({
  categoria_id:yup.string().test({
    name: 'categoria_id',
    skipAbsent:true,
    test(value, ctx){
      if(value=='0'){
        return ctx.createError({message: 'Debe seleccionar una categoría'})
      }
      return true;
    }
  }),
  nombre: yup.string().required("El campo nombre es obligatorio"),
  tiempo: yup.string().required("El campo Tiempo es obligatorio"),
  descripcion: yup.string().required("El campo Descripción es obligatorio"),


});

