// ==UserScript==
// @name         Login Rápido VFS
// @namespace    http://tampermonkey.net/
// @version      2.6
// @description  Faz login automaticamente no site VFS e registra a conta usada
// @match        https://visa.vfsglobal.com/*
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

(function() {
    'use strict';

    // Credenciais das contas (adicione mais se necessário)
    const contas = [
        { email: "luclinocruz@hotmail.com", senha: "Lucluk123@", nickN: "Luc Outlook" },
        { email: "luclinoc@gmail.com", senha: "Lucluk123@", nickN: "Luc C" },
        { email: "luclinor@gmail.com", senha: "Luanda1@", nickN: "Luc R" },
        { email: "kadianafigueiredotshiama@gmail.com", senha: "Lucluk123@", nickN: "Kadi Gmail" }
    ];

    // Variável para armazenar a conta logada
    let contaLogada = null;

    // Função para forçar o preenchimento dos campos
    function preencherLogin(conta) {
        // Seleciona o campo de e-mail e remove restrições
        let campoEmail = document.querySelector('#email');
        if (campoEmail) {
            campoEmail.removeAttribute('autocomplete');
            campoEmail.removeAttribute('disabled');
            campoEmail.value = conta.email;
            campoEmail.dispatchEvent(new Event('input', { bubbles: true }));
        }

        // Seleciona o campo de senha e remove restrições
        let campoSenha = document.querySelector('#password') || document.querySelector('#mat-input-4');
        if (campoSenha) {
            campoSenha.removeAttribute('autocomplete');
            campoSenha.removeAttribute('disabled');
            campoSenha.value = conta.senha;
            campoSenha.dispatchEvent(new Event('input', { bubbles: true }));
        }

        // Ativa e clica no botão de login
        setTimeout(() => {
            let botaoLogin = document.querySelector('button.btn.mat-btn-lg.btn-block.btn-brand-orange');
            if (botaoLogin) {
                botaoLogin.removeAttribute('disabled');
                botaoLogin.click();
                contaLogada = conta; // Atualiza a conta logada
                atualizarBotaoPrincipal(); // Atualiza o texto do botão principal
            }
        }, 1500); // Pequeno atraso para garantir que os campos foram preenchidos
    }

    // Função para atualizar o texto do botão principal
    function atualizarBotaoPrincipal() {
        const botaoPrincipal = document.getElementById("menuPrincipal");
        if (botaoPrincipal) {
            botaoPrincipal.textContent = contaLogada ? contaLogada.nickN : "Logins";
        }
    }

    // Função para criar o menu expansível
    function criarMenu() {
        // Cria o botão principal
        const botaoPrincipal = document.createElement("button");
        botaoPrincipal.id = "menuPrincipal";
        botaoPrincipal.textContent = "Logins";
        botaoPrincipal.style.cssText = `
            position: fixed;
            top: 10px;
            left: 10px;
            padding: 10px 15px;
            background: #007BFF;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        `;
        botaoPrincipal.addEventListener("click", () => {
            const isHidden = menu.style.left === "-220px";
            menu.style.left = isHidden ? "10px" : "-220px"; // Alternar entre visível e escondido
        });
        document.body.appendChild(botaoPrincipal);

        // Cria o menu lateral
        const menu = document.createElement("div");
        menu.id = "menuLateral";
        menu.style.cssText = `
            position: fixed;
            top: 70px;
            left: -220px; /* Inicialmente escondido */
            width: 200px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            box-shadow: 3px 0 5px rgba(0, 0, 0, 0.2);
            padding: 10px;
            transition: left 0.3s ease;
            z-index: 9999;
        `;

        // Adiciona botões para cada conta
        contas.forEach((conta, index) => {
            const btn = document.createElement("button");
            btn.textContent = conta.nickN;
            btn.style.cssText = `
                display: block;
                width: 100%;
                margin: 5px 0;
                padding: 8px;
                background: linear-gradient(45deg, #ff8c00, #ff0080);
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            `;
            btn.onmouseover = () => {
                btn.style.transform = "scale(1.05)";
                btn.style.boxShadow = "0 4px 10px rgba(255, 140, 0, 0.7)";
            };
            btn.onmouseleave = () => {
                btn.style.transform = "scale(1)";
                btn.style.boxShadow = "none";
            };
            btn.addEventListener("click", () => preencherLogin(conta));
            menu.appendChild(btn);
        });

        document.body.appendChild(menu);
    }

    // Inicializa o menu
    criarMenu();
})();