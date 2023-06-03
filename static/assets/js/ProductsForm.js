const productsForm = {
    props: ['id'],
    delimiters: ['[[', ']]'],
    data() {
        return {
            route: 'form',
            success: false,
            showWhatsappBnt: true,
            showWhatsappSendSuccessBtn: false,
            form: {
                product_obj: {
                    title: '',
                    price: ''
                },
                template: 0,
                product: 0,
                quantity: 1,
                name: '',
                phone_number: '',
                city: '',
                address: '',
                payment_type: 'card',
                payment_id: ''
            },
            session: {
                template: 0,
                ip_address: '',
                city: '',
                region: '',
                country: '',
                location: '',
                duration: 0
            },
            template: {
                id: 0,
                template_code: '',
                description: '',
                meta_title: '',
                main_rating_title: '',
                meta_description: '',
                meta_keywords: '',
                logo: '',
                main_image: '',
                medals_image: '',
                second_image: '',
                review_text: '',
                feature_text: '',
                primary_color: '',
                secondary_color: '',
                products: [],
                features: [],
                reviews: [],
                created_at: '',
                updated_at: ''
            },
            share: {
                template: null,
                product: 0,
                phone_number: '',
                city: ''
            }
        };
    },
    created(){
      axios.defaults.baseURL = 'https://landing.socialbot.dev/api/v1'
        window.setInterval(() => {
            this.setDuration();
        }, 1000)
        window.addEventListener("beforeunload", this.leaving);
    },
    mounted() {
        this.getTemplate();
        this.getIpInfo();
        console.log(window.location.href)
        function parse_query_string(query) {
          var vars = query.split("&");
          var query_string = {};
          for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            var key = decodeURIComponent(pair.shift());
            var value = decodeURIComponent(pair.join("="));
            // If first entry with this name
            if (typeof query_string[key] === "undefined") {
              query_string[key] = value;
              // If second entry with this name
            } else if (typeof query_string[key] === "string") {
              var arr = [query_string[key], value];
              query_string[key] = arr;
              // If third or later entry with this name
            } else {
              query_string[key].push(value);
            }
          }
          return query_string;
        }

        var qs = parse_query_string(window.location.search.substring(1))

        if (qs.status == 'success' || qs.status == 'paid'){
            Swal.fire({
              icon: 'success',
              title: 'شكرًا',
              text: 'تم الدفع بنجاح',
              confirmButtonText: 'تمام'
            })
        }
        if (qs.status == 'failed'){
            Swal.fire({
              icon: 'error',
              title: 'نعتذر',
              text: 'هناك خطأ في الدفع',
              confirmButtonText: 'تمام'
            })
        }
        window.history.replaceState(null, '', window.location.pathname);
    },
    computed:{
      unitPrice(){
          return this.form.product_obj.price_after_discount ? this.form.product_obj.price_after_discount : this.form.product_obj.price
      },
      totalAmount(){
          return this.form.product_obj.price_after_discount ? this.form.quantity * this.form.product_obj.price_after_discount : this.form.quantity * this.form.product_obj.price
      }
    },
    methods: {
        checkPhoneNumberSize(from){
            if (from == 'share') {
                this.share.phone_number = this.share.phone_number.toString().substring(0, 9)
            }
            if (from == 'form') {
                this.form.phone_number = this.form.phone_number.toString().substring(0, 9)
            }
        },
        submitShare(){
            let valid = true;
            this.share.template = this.template.id
            this.share.city = this.session.city;
            /* let isnum = /^\d+$/.test(this.share.phone_number);

            if(this.share.phone_number == '' || !isnum || this.share.phone_number.toString().length != 8){
                valid = false;
                document.getElementById("formPhone2").style = "background: #f2f2f2;border-color: var(--bs-primary);padding-left: 83px;direction: ltr;"
                document.getElementById("formPhone2").classList.add("is-invalid");
                document.getElementById("formPhoneError2").textContent = "يرجى إدخال رقم جوال صحيح";
                document.getElementById("formPhoneFlag2").style = "position: absolute;top: 35%;transform: translateY(-50%);left: 20px;";
            } else {
                document.getElementById("formPhone2").style = "background: #f2f2f2;border-style: none;padding-left: 83px;direction: ltr;"
                document.getElementById("formPhone2").classList.remove("is-invalid");
                document.getElementById("formPhoneError2").textContent = "";
                document.getElementById("formPhoneFlag2").style = "position: absolute;top: 50%;transform: translateY(-50%);left: 20px;";
            } */
            if(valid) {
                this.share.product = this.form.product
                axios.post("/public/create_share", this.share)
                    .then(res => {
                        console.log(res)
                        this.showWhatsappBnt = true
                        this.showWhatsappSendSuccessBtn = true
                    })
                    .catch(err => {
                        console.log(err)
                    })
            }
        },
        getStars(review){
            let star = '<span style="color: var(--bs-secondary);margin-left: 5px;"><i class="fas fa-star"></i></span>'
            return star.repeat(review.rating)
        },
        selectProduct(product){
            this.form.product_obj = product;
            this.form.product = product.id;

            const slides = document.querySelectorAll('.swiper-slide');
            slides.forEach(slide => {
                slide.classList.remove('active');
            });

            document.getElementById('product-'+product.id).classList.add('active');
        },
        decreaseQty(){
            if (this.route == 'form' && this.form.quantity > 1) {
                this.form.quantity = this.form.quantity - 1;
            }
        },
        increaseQty(){
            if (this.route == 'form') {
                this.form.quantity = this.form.quantity + 1;
            }
        },
        getDivClass(index){
            if(index == 0){
                return "swiper-slide active";
            } else {
                return "swiper-slide";
            }

        },
        setDuration(){
            this.session.duration = this.session.duration + 1;
        },
        getCookie(cname){
            let name = cname + "=";
            let decodedCookie = decodeURIComponent(document.cookie);
            let ca = decodedCookie.split(';');
            for(let i = 0; i <ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
                }
            }
            return "";
        },
        submitForm(){
            var valid = true;

            if(this.form.name == ''){
                valid = false;
                document.getElementById("formName").style = "background: #f2f2f2;border-color: var(--bs-primary);"
                document.getElementById("formName").classList.add("is-invalid");
                document.getElementById("formNameError").textContent = "يرجى إدخال الاسم";
            } else {
                document.getElementById("formName").style = "background: #f2f2f2;border-style: none;"
                document.getElementById("formName").classList.remove("is-invalid");
                document.getElementById("formNameError").textContent = "";
            }

            let isnum = /^\d+$/.test(this.form.phone_number);

            if(this.form.phone_number == '' || !isnum || this.form.phone_number.toString().length != 9){
                valid = false;
                document.getElementById("formPhone").style = "background: #f2f2f2;border-color: var(--bs-primary);padding-left: 83px;direction: ltr;"
                document.getElementById("formPhone").classList.add("is-invalid");
                document.getElementById("formPhoneError").textContent = "يرجى إدخال رقم جوال صحيح";
                document.getElementById("formPhoneFlag").style = "position: absolute;top: 35%;transform: translateY(-50%);left: 20px;";
            } else {
                document.getElementById("formPhone").style = "background: #f2f2f2;border-style: none;padding-left: 83px;direction: ltr;"
                document.getElementById("formPhone").classList.remove("is-invalid");
                document.getElementById("formPhoneError").textContent = "";
                document.getElementById("formPhoneFlag").style = "position: absolute;top: 50%;transform: translateY(-50%);left: 20px;";
            }

            if(this.form.address == ''){
                valid = false;
                document.getElementById("formAddress").style = "background: #f2f2f2;border-color: var(--bs-primary);"
                document.getElementById("formAddress").classList.add("is-invalid");
                document.getElementById("formAddressError").textContent = "يرجى إدخال العنوان";
            } else {
                document.getElementById("formAddress").style = "background: #f2f2f2;border-style: none;"
                document.getElementById("formAddress").classList.remove("is-invalid");
                document.getElementById("formAddressError").textContent = "";
            }

            if(valid){
                console.log(this.form.payment_type)
                if (this.form.payment_type == 'card'){
                    this.route = 'payment'
                    console.log(this.totalAmount)
                    Moyasar.init({
                        element: '.mysr-form',
                        // Amount in the smallest currency unit.
                        // For example:
                        // 10 SAR = 10 * 100 Halalas
                        // 10 KWD = 10 * 1000 Fils
                        // 10 JPY = 10 JPY (Japanese Yen does not have fractions)
                        amount: this.totalAmount * 100,
                        currency: 'SAR',
                        description: 'Coffee Order #1',
                        language: 'ar',
                        publishable_api_key: 'pk_test_37qqSidenDWUMRKRE6pEE41BmizEyzozete7RRX7',
                        callback_url: 'http://'+window.location.host + window.location.pathname,
                        on_completed: (payment) => {
                            console.log(payment)
                            console.log(this.form)
                            this.form.payment_id = payment.id
                            axios.post('https://webhook.site/9a931dfe-3f67-4885-b951-5cce2defa35c', {pay: this.form})
                            this.createOrder()
                            return Promise.resolve({});
                          },
                        methods: ['stcpay', 'creditcard'],
                    });
                } else {
                    this.createOrder()
                    this.route = 'success'
                }
            }
        },
        createOrder(){
            this.form.template = this.template.id
            const data = {
                template: this.form.template,
                lead: {
                    name: this.form.name,
                    phone_number: this.form.phone_number,
                    city: this.form.city,
                    address: this.form.address
                },
                input_items: [
                    {
                        "id": this.form.product,
                        "quantity": this.form.quantity
                    }
                ],
                payment_type: this.form.payment_type,
                payment_id: this.form.payment_id
            }
            console.log(data)
            axios.post("https://landing.socialbot.dev/api/v1/orders/public/", data)
            .then((response) => {
                document.cookie = 'name='+this.form.name+'; expires=Thu, 01 Jan 9999 00:00:00 UTC';
                document.cookie = `phonenumber=${this.form.phone_number}; expires=Thu, 01 Jan 9999 00:00:00 UTC`;
                document.cookie = `city=${this.form.city}; expires=Thu, 01 Jan 9999 00:00:00 UTC`;
                document.cookie = `address=${this.form.address}; expires=Thu, 01 Jan 9999 00:00:00 UTC`;

                this.success = true;
            })
            .catch((error) => {
                console.log(JSON.stringify(error));
            });
        },
        leaving(){
            this.session.template = this.id
            fetch('https://landing.socialbot.dev/api/v1/public/create_visit', {
                method: 'POST',
                body: JSON.stringify(this.session),
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    'Content-Type': 'application/json'
                },
                keepalive: true,
            })
            this.session.duration = 0;
        },
        getTemplate(){
            axios
            .get(
                `/public/apps/templates/${this.id}`
            )
            .then((response) => {
                console.log(response);
                this.template = response.data;

                //let html = document.getElementById("html");
                //html.style = `--bs-secondary: #f5d260;--bs-secondary-rgb: 245,210,96;--bs-primary: ${this.template.primary_color};--bs-primary-rgb: 183,194,38;`;

                this.form.template = this.template.id;
                if(response.data.products.length != 0){
                    this.form.product = this.template.products[0].id;
                    this.form.product_obj = this.template.products[0];
                }

                if (response.data.card_payment){
                    this.form.payment_type = 'card'
                } else {
                    this.form.payment_type = 'cod'
                }

                this.form.name = this.getCookie('name');
                this.form.phone_number = this.getCookie('phonenumber');
                this.form.city = this.getCookie('city') ? this.getCookie('city') : this.template.cities[0].name;
                this.form.address = this.getCookie('address');
            })
            .catch((error) => {
                console.log(JSON.stringify(error));
            });
        },
        createVisit(){
            axios.post("/public/create_visit", this.session)
            .then((res) => {
                console.log(res);
            })
            .catch((error) =>{
                console.log(JSON.stringify(error));
            })
        },
        getIpInfo(){
            axios.get("https://ipinfo.io/?token=37b3a65957bff3")
            .then(response => {
                let data = response.data;

                this.session.ip_address = data.ip;
                this.session.location = data.loc;
                this.session.city = data.city;
                this.session.country = data.country;
                this.session.region = data.region;
                this.session.template = this.template.id;
            })
            .catch((error) =>{
                console.log(JSON.stringify(error));
            })
        }
    },
    template: `
    <div>
      <section class="mt-4">
        <div class="container">
            <h3 style="font-size: 16px;font-weight: bold;" class="mb-4">العرض</h3>
            <div id="swiperSlider" class="swiper-container" style="margin-bottom: 57px;overflow: hidden;">
                <div class="swiper-wrapper" style="cursor: pointer;">
                    <div v-for="(product, index) in template.products" :key="product.id" :id="'product-'+[[product.id.toString()]]" :class="getDivClass(index)" @click="selectProduct(product)" style="width: 145px;padding-bottom: 9px;padding-left: 8px;padding-right: 8px;padding-top: 0px;margin-left: 11px;background-color: #f2f2f2;border-radius: 8px;border-style: solid;border-color: transparent;">
                        <div style="width: 70px;height: 70px;border-radius: 10px;margin-bottom: 10px;position: relative;margin-top: 15px;">
                            <div style="position: absolute;width: 75px;left: -22px;"><img :src="product.image" style="width: 100%;"></div>
                        </div>
                        <h3 style="font-size: 16px;">[[product.title]]</h3>
                        <h4 style="font-size: 12px;">[[product.description]]</h4>
                        <template v-if="product.price_after_discount">
                            <p style="color: #999A9A;text-decoration:  line-through;">[[product.price]] ر.س</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <p style="color: #E5423B;margin-top: 0px;margin-bottom: 6px;white-space: nowrap;">[[product.price_after_discount]] ر.س</p><span v-if="product.label" style="font-size: 9px;background: #EB6A64;color: #ffff;border-radius: 17px;padding: 3px 7px 3px;white-space: nowrap;">[[product.label]]</span>
                            </div>
                        </template>
                        <template v-else>
                            <div class="d-flex justify-content-between align-items-center">
                                <p style="color: #E5423B;margin-top: 0px;margin-bottom: 6px;white-space: nowrap;">[[product.price]] ر.س</p><span v-if="product.label" style="font-size: 9px;background: #EB6A64;color: #ffff;border-radius: 17px;padding: 3px 7px 3px;white-space: nowrap;">[[product.label]]</span>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
            <div class="d-flex justify-content-between align-items-center">
                <h3 style="font-size: 16px;font-weight: bold;">الكمية</h3>
                <div class="d-flex justify-content-between align-items-center" style="width: 250px;padding: 10px 25px;border-radius: 5px;color: rgb(0,0,0);border: 1px solid #F2F2F2 ;"><i @click="decreaseQty()" class="fas fa-minus" :class="form.quantity == 1 ? 'disabled':''" id="quantity-minus" style="color: var(--bs-primary);"></i><span id="quantity-text" style="font-size: 18px;">[[form.quantity]]</span><i @click="increaseQty()" class="fas fa-plus" id="quantity-plus" style="color: var(--bs-primary);"></i></div>
            </div>
            <div id="order_now" style="border-bottom: 1px solid #F2F2F2;margin-top: 25px;margin-bottom: 15px;" class="mb-4"></div>
        </div>
    </section>

    <section v-show="route == 'form'" >
      <div class="container">
          <div style="box-shadow: 0px 5px 12px #f2f2f2;border: 1px solid #f2f2f2;border-radius: 8px;" class="px-2 pb-3">
              <h1 style="font-size: 30px;text-align: center;" class="mb-4 mt-3">اطلبه الآن</h1>
              <form>
                  <div class="mb-2">
                      <input v-model="form.name" id="formName" class="form-control py-3" type="text" placeholder="الاسم" style="background: #f2f2f2;border-style: none;">
                      <div id="formNameError" style="color: var(--bs-primary)" class="invalid-feedback"></div>
                  </div>
                  <div class="mb-2" style="position: relative;">
                      <input @keyup="checkPhoneNumberSize('form')" class="form-control py-3" maxlength="9" id="formPhone" type="number" pattern="[0-9]*" inputmode="numeric" v-model="form.phone_number" placeholder="5x xxx xxxx" style="background: #f2f2f2;border-style: none;padding-left: 83px;direction: ltr;">
                      <div id="formPhoneFlag" class="d-flex align-items-center" style="position: absolute;top: 50%;transform: translateY(-50%);left: 20px;"><span>966&nbsp;&nbsp;</span><img src="https://landing.socialbot.dev/static/assets/img/saudi-arabia-flag-icon.png" style="width: 20px;"></div>
                      <div id="formPhoneError" style="color: var(--bs-primary)" class="invalid-feedback"></div>
                  </div>
                  <div class="mb-2" style="position: relative;"><select v-model="form.city" class="form-select py-3" style="padding-right: 12px;padding-left: 34px;border-style: none;background: #f2f2f2;">
                          <option v-for="city in template.cities" :key="city.id" :value="city.id">[[city.main_city.name_ar]]</option>
                      </select><i class="fas fa-chevron-down" style="position: absolute;top: 50%;transform: translateY(-50%);left: 20px;"></i></div>
                  <div class="mb-2">
                      <input id="formAddress" v-model="form.address" class="form-control py-3" type="text" placeholder="العنوان (الحي، الشارع)" style="background: #f2f2f2;border-style: none;">
                      <div id="formAddressError" style="color: var(--bs-primary)" class="invalid-feedback"></div>
                  </div>
<!--                  <div class="mb-2" style="position: relative;">-->
<!--                      <select v-model="form.payment_type" class="form-select py-3" style="padding-right: 12px;padding-left: 34px;border-style: none;background: #f2f2f2;">-->
<!--                          <option value="cod">COD</option>-->
<!--                          <option value="card">Credit Card</option>-->
<!--                      </select><i class="fas fa-chevron-down" style="position: absolute;top: 50%;transform: translateY(-50%);left: 20px;"></i>-->
<!--                  </div>-->
                  <div class="mb-2" style="position: relative;">
                    <!-- Credit card form tabs -->
                    <ul role="tablist" class="nav bg-light nav-pills rounded nav-fill mb-3" style="padding-right: 0;">
                        <li v-show="template.card_payment" class="nav-item" @click="form.payment_type='card'">
                            <a :style="form.payment_type=='card' ? 'color:white;background-color:var(--bs-primary);':'color:var(--bs-primary)'" data-toggle="pill" href="javascript:void(0);" class="nav-link"> <i class="fas fa-credit-card mr-2"></i> الدفع الالكتروني </a>
                        </li>
                        <li v-show="template.cod_payment" class="nav-item" @click="form.payment_type='cod'">
                            <a :style="form.payment_type=='cod' ? 'color:white;background-color:var(--bs-primary);':'color:var(--bs-primary)'" data-toggle="pill" href="javascript:void(0);" class="nav-link"> <i class="fa fa-hand-holding-usd mr-2"></i> الدفع عند الاستلام </a>
                        </li>
                    </ul>
                  </div>
                  <div class="d-flex justify-content-between mt-3" style="color: #343434;"><span>[[form.product_obj.title]]</span><span>x[[form.quantity]]</span></div>
                  <div class="d-flex justify-content-between mt-2" style="color: #343434;"><span>السعر شامل الضريبة</span><span>[[unitPrice]] ر.س</span></div>
                  <div class="d-flex justify-content-between mt-2" style="color: #343434;"><span>الشحن السريع</span><span>مجاني</span></div>
                  <div style="border-bottom: 1px solid #F2F2F2;margin-top: 25px;margin-bottom: 15px;" class="mb-0"></div>
                  <div class="d-flex justify-content-between mt-2" style="color: #343434;"><span style="font-weight: bold;">الاجمالي</span><span style="font-weight: bold;">[[totalAmount]] ر.س</span></div>

                  <a @click="submitForm()" class="btn btn-primary py-3 mt-4" role="button" style="width: 100%;background: var(--bs-primary);border-style: none;border-radius: 4px;margin-top: 34px;">شراء</a>
              </form>
          </div>
      </div>
    </section>
    <section v-show="route == 'success'" >
        <div class="container">
            <div style="box-shadow: 0px 5px 12px #f2f2f2;border: 1px solid #f2f2f2;border-radius: 8px;" class="px-2 pb-3">
                <!-- <h1 style="font-size: 30px;text-align: center;" class="mb-4 mt-3">اطلبه الآن</h1> -->
                <div class="text-center p-5">
                    <span class="display-4" style="color: var(--bs-primary);margin-left: 5px;"><i class="fas fa-check-circle"></i></span>
                    <h1>شكرا لك</h1>
                    <p style="font-size: 30px">تم استقبال طلبك بنجاح</p>

                    <p>سنقوم بأكيد طلبك عبر الواتس اب</p>
                    <p style="color: var(--bs-primary);">[[this.form.phone_number]]</p>
                </div>

                <a class="btn btn-primary py-3 mt-4" role="button" style="width: 100%;background: var(--bs-primary);border-style: none;border-radius: 4px;margin-top: 34px;">شارك العرض مع صديق</a>
            </div>
        </div>
    </section>
    <section v-show="route == 'payment'">
        <div class="container mb-1 mt-2">
            <div style="box-shadow: 0px 5px 12px #f2f2f2;border: 1px solid #f2f2f2;border-radius: 8px;" class="px-2 pb-3">
                <a @click="route='form'" style="color: var(--bs-primary)" href="javascript:void(0);" class="link-underline-opacity-0 px-2"> <i class="fas fa-arrow-right mr-2"></i> العودة إلى عربة التسوق </a>
<!--                <h4 @click="route='form'" style="color: var(&#45;&#45;bs-primary)">العودة إلى عربة التسوق</h4>-->
                <div class="mysr-form" style="margin-top: 25px;"></div>
            </div>
        </div>
    </section>
  </div>
    `
}