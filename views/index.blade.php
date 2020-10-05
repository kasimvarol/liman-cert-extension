<div id="createcakeycert" class="tab-pane">
        @include('modal-button',[
            "class"     =>  "btn btn-outline-primary",
            "target_id" =>  "createCAKeyCert",
            "text"      =>  "Anahtar ve Self-Signed Sertifika Oluştur",
            "icon" => "fas fa-plus"
        ])<br><br>
        <div class="table-responsive"></div> 
        <div class="messageAlert"></div> 
        @include('modal',[
            "id"=>"createCAKeyCert",
            "title" => "Anahtar ve Sertifika Oluştur",
            "url" => API('createCAKeyCert'),
            "next" => "reload",
            "inputs" => [
                "Bit Sayısı" => "bit:text:2048",
                "Gün" => "days:text:Gün Sayısı",
                "Ülke" => "country:text:2 Karakter XX",
                "Eyalet" => "state:text",
                "Şehir" => "city:text",
                "Organizasyon İsmi" => "ou:text",
                "CN" => "cn:text",
                "Otorite İsmi" => "caname:text",
                "Passphrase" => "pass:password",
            ],
            "submit_text" => "Oluştur ve Ekle"
            ])
</div>


<div id="normalcert" class="tab-pane">
        @include('modal-button',[
            "class"     =>  "btn btn-outline-primary",
            "target_id" =>  "addNormalCert",
            "text"      =>  "Anahtardan Normal Sertifika Oluştur",
            "icon" => "fas fa-plus"
        ])<br><br>
        <div class="table-responsive"></div> 
        <div class="messageAlert"></div> 
        @include('modal',[
            "id"=>"addNormalCert",
            "title" => "Sertifika Oluştur",
            "url" => API('addNormalCert'),
            "next" => "reload",
            "inputs" => [
                "Gün" => "days:text:Gün Sayısı",
                "Ülke" => "country:text:2 Karakter XX",
                "Eyalet" => "state:text",
                "Şehir" => "city:text",
                "Organizasyon İsmi" => "ou:text",
                "CN" => "cn:text",
                "Anahtar Dizin Yolu" => "keypath:text:/home/kullanici/anahtar.key",
                "Sertifika İsmi" => "certname:text",
            ],
            "submit_text" => "Oluştur ve Ekle"
            ])
</div>
<button class="btn btn-primary mb-2" onclick="runScript()">Sertifikaları Listele</button>
<div id="devtoPython"></div>

<script>
    function runScript(){
        var form = new FormData();
        request("{{API('runPythonScript')}}", form, function(response) {
            message = JSON.parse(response)["message"];
            $('#devtoPython').html(message);
        }, function(error) {
            $('#devtoPython').html("Hata oluştu");
        });
    }
</script>


