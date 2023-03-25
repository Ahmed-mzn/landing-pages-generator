const shareTemplate = {
    props: ['id'],
    delimiters: ['[[', ']]'],
    data() {
        return {
            success: false,
            showWhatsappBnt: true,
            showWhatsappSendSuccessBtn: false,
            share: {
                template: null,
                product: 0,
                phone_number: '',
                city: ''
            }
        };
    },
    created(){
        axios.defaults.baseURL = 'https://landing.socialbot.dev/api/v1/public'
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
            this.share.template = this.id
            if(valid) {
                axios.post("/create_share", this.share)
                    .then(res => {
                        this.showWhatsappBnt = true
                        this.showWhatsappSendSuccessBtn = true
                    })
                    .catch(err => {
                        console.log(err)
                    })
            }
        },
    },
    template: `
        <div>
            <section class="mt-4">
                <div class="container">
                    <div style="border-bottom: 1px solid #F2F2F2;margin-top: 25px;margin-bottom: 15px;"></div>
                    <h3 style="font-size: 16px;font-weight: bold;">حفظ هذا العرض لوقت لاحق</h3>
                    <a v-if="showWhatsappBnt && !showWhatsappSendSuccessBtn" @click="showWhatsappBnt = false" class="btn btn-primary d-flex justify-content-center align-items-end" role="button" style="width: 100%;background: #f2f2f2;border-style: none;border-radius: 4px;color: #000;padding-top: 10px;padding-bottom: 16px;">
                        <i class="fab fa-whatsapp" style="font-size: 20px;"></i>&nbsp;<span>ارسله لي عبر الوتس اب<br></span>&nbsp;
                    </a>
                    <a v-if="showWhatsappSendSuccessBtn" @click="showWhatsappBnt = true; showWhatsappSendSuccessBtn= false" class="btn btn-primary d-flex justify-content-center align-items-end" role="button" style="width: 100%;background: #f2f2f2;border-style: none;border-radius: 4px;color: #000;padding-top: 10px;padding-bottom: 16px;">
                        <i class="fas fa-check-circle" style="font-size: 20px;color: green"></i>&nbsp;<span>تم الإرسال، تحقق من الوتس اب<br></span>&nbsp;
                    </a>
                    <form id="whatsapp-form" @submit.stop.prevent="submitShare" class="my-2 mt-3" v-if="!showWhatsappBnt">
                        <div class="d-flex flex-row-reverse align-items-stretch mb-2" style="position: relative;">
                            <input @keyup="checkPhoneNumberSize('share')" v-model="share.phone_number" id="formPhone2" class="form-control py-2" type="number" pattern="[0-9]*" inputmode="tel" placeholder="5x xxx xxxx" style="background: #f2f2f2;border-style: none;padding-left: 83px;direction: ltr;">
                            <button class="btn btn-primary ms-2" type="submit" style="width: 50px;background: var(--bs-black);">
                                <i class="fas fa-level-down-alt" style="transform: rotate(90deg);"></i>
                            </button>
                            <div id="formPhoneFlag2" class="d-flex align-items-center" style="position: absolute;top: 50%;transform: translateY(-50%);left: 20px;"><span>966&nbsp;&nbsp;</span><img src="https://landing.socialbot.dev/static/assets/img/saudi-arabia-flag-icon.png" style="width: 20px;"></div>
                        </div>
                    </form>
                </div>
            </section>
        </div>
    `
}