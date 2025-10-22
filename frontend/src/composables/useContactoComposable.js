export function useContactoComposable(body)
{

  let sendData = async (body) =>{
    try{
      let respuesta  = await fetch(`${import.meta.env.VITE_API_URL}contacto/`, {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {'Content-Type': 'application/json'}

    });
    if (respuesta.status == 200){
      alert('Gracias por contactarnos, te responderemos a la brevedad');
      window.location=location.href;
  }
    }catch(error){
      throw new Error('Error enviando el formulario de contacto');
    }


  };
  return {sendData}

};

