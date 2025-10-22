import { useAuthStore } from '@/stores/authStore';
import axios from 'axios';

export function registroComposable(body) {

  let sendData = async (body) => {
    /*try{


    }catch(error){
     alert("Ocurrió un error inesperado");
     window.location.href=location.href;
    }*/
    axios.post(`${import.meta.env.VITE_API_URL}seguridad/registro/`, body, { headers: { 'Content-Type': 'application/json' } })
      .then((response) => {
        alert("Te has registrado con exito en el sistema!!/n Te hemos un mail al correo que nos proporcionaste para activar tu cuenta.");
        window.location.href = location.href;
      })
      .catch((err) => {
        alert("Ocurrió un error inesperado" +err);
        window.location.href = location.href;
      });
  };
  return { sendData, };
}

export function loginComposable(body) {

  let sendData = async (body) => {
    /*try{


    }catch(error){
     alert("Ocurrió un error inesperado");
     window.location.href=location.href;
    }*/
    axios.post(`${import.meta.env.VITE_API_URL}seguridad/login/`, body, { headers: { 'Content-Type': 'application/json' } })
      .then((response) => {
        let store = useAuthStore();
        store.iniciarSesion(response.data);
        window.location = "/panel";
      })
      .catch((err) => {
        alert("Ocurrió un error inesperado" +err);
        window.location.href = location.href;
      });
  };
  return { sendData, };
}
