export async function getDatosHome() {
  let respuesta = await fetch(`${import.meta.env.VITE_API_URL}recetas-home/`,{headers: {'content-type': 'application/json'}});
  return await respuesta.json();
}
