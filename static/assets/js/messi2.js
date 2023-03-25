
(() => {
    Vue.component('share-template', shareTemplate);
    const app1 = new Vue({
      el: "#app2",
      delimiters: ['[[', ']]'],
      data() {
          return {
            id: document.getElementById("props-template-id").value,
            share: document.getElementById("props-share-template-code").value,
          }
      },
      template: `
        <div>
          <share-template :id="id" />
        </div>
      `
    });
  })();
