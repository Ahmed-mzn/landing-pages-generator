
(() => {
    Vue.component('products-form', productsForm);
    Vue.component('products-form2', productsForm2);
    const app1 = new Vue({
      el: "#app2",
      delimiters: ['[[', ']]'],
      data() {
          return {
            id: document.getElementById("props-template-id").value,
            type: document.getElementById("props-template-code").value,
          }
      },
      template: `
        <div>
          <products-form v-if="type == 'template_one'" :id="id" />
          <products-form2 v-if="type == 'template_two'" :id="id" />
        </div>
      `
    });
  })();
