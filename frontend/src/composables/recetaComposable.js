import { readonly,ref } from "vue";

export function recetaComposable(slug)
{
    let dato = ref({ data: {} });
    let error = ref(null);

    let getDatos = async (slug) =>
    {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}recetas/slug/${slug}/`, {headers: {'content-type': 'application/json'}});

        dato.value =await res.json();
        if (res.status == 404) {
          window.location="/error";
        }
      } catch (err) {
        error.value = err;
      }
    };
    getDatos(slug);
    return{
      dato: readonly (dato),
      error: readonly (error)
    }
}


/*export function recetasComposable()
{
    let datos = ref([]);
    let error = ref(null);

    let getDatos = async () =>
    {

    };
    return{
      datos: readonly (datos),
      error: readonly (error)

    }
}
*/

/*export function recetasComposable()
{
    let datos = ref([]);
    let error = ref(null);

    let getDatos = async () =>
    {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}recetas/`, {headers: {'content-type': 'application/json'}});
        datos.value = await res.json();
      } catch (err) {
        error.value = err;

      }
    };
    getDatos();
    return{
      datos: readonly (datos),
      error: readonly (error)

    }
}*/
