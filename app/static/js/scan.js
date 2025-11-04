if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    Quagga.init({
        inputStream: { name: 'Live', type: 'LiveStream', target: document.querySelector('#preview') },
        decoder: { readers: ['ean_reader','ean_8_reader','code_128_reader','code_39_reader'] }
    }, function(err){
        if (err) { console.error(err); return; }
        Quagga.start();
});


Quagga.onDetected(function(result){
    const code = result.codeResult.code;
    document.getElementById('detected').value = code;
});
}