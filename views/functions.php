<?php 

    function index(){
        return view('index');
    }

    function runPythonScript(){
        $output = runScript("devtopython.py","",false);
        return respond($output,200);
    }

    function addNormalCert(){
        $days = request("days");
        $country = request("country");
        $state = request("state");
        $city = request("city");
        $ou = request("ou");
        $cn = request("cn");
        $keypath = request("keypath");
        $certname = request("certname");
        
        $cmd = "openssl req -new -days $days -x509 -subj '/C=$country/ST=$state/L=$city/O=$ou/CN=$cn' -key $keypath -out $certname.crt";
        runCommand($cmd);
        runScript("devtopython.py","add_normalcert /home/liman/$certname.crt",false);
        return respond("Başarılı!");
    }
    function createCAKeyCert(){
        $bit = request("bit");
        $days = request("days");
        $country = request("country");
        $state = request("state");
        $city = request("city");
        $ou = request("ou");
        $cn = request("cn");
        $caname = request("caname");
        $pass = request("pass");
        
        $cmd = "openssl req -new -newkey rsa:$bit -days $days -x509 -subj '/C=$country/ST=$state/L=$city/O=$ou/CN=$cn' -passout pass:$pass -keyout $caname.key -out $caname.crt";
        runCommand($cmd);
        runScript("devtopython.py","add_normalcert /home/liman/$caname.crt",false);
        return respond("Başarılı!");
    }


?>