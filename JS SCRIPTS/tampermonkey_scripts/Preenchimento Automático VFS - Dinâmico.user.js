// ==UserScript==
// @name         Preenchimento Automático VFS - Dinâmico
// @namespace    http://tampermonkey.net/
// @version      3.6
// @description  Automatiza o fluxo de agendamento no VFS, carregando clientes de um arquivo dinâmico.
// @author       Luclino Cruz
// @match        https://visa.vfsglobal.com/*
// @grant        GM_xmlhttpRequest
// @connect      localhost
// ==/UserScript==

(function() {
    'use strict';

    // Vetor de clientes carregado dinamicamente
    let clientes = [];

    // Função para buscar clientes.json de servidor local
    function fetchClientes() {
        GM_xmlhttpRequest({
            method: 'GET',
            url: 'http://localhost:3000/clientes.json',
            onload: function(res) {
                try {
                    clientes = JSON.parse(res.responseText);
                    console.log(`⚡ ${clientes.length} clientes carregados`);
                    init();
                } catch (e) {
                    console.error('Erro parsing clientes.json', e);
                }
            },
            onerror: function(err) {
                console.error('Erro fetching clientes.json', err);
            }
        });
    }

    // Inicializa interface e controle quando clientes estiverem disponíveis
    function init() {
        window.addEventListener('load', () => {
            addFloatingControl();
            addProfileSidebar();
        });
    }

    /********************* Módulos originais (A-F) *********************/
    function iniciarFluxo() {
        console.log("🚀 Fluxo de agendamento iniciado!");
        clicarStartBooking();
        manterSessaoAtiva();
        setTimeout(() => {
            const clienteAtual = clientes[0];
            selecionarSubCategoriaEAgendamento(clienteAtual);
        }, 5000);
    }

    function clicarStartBooking() {
        let btn = document.querySelector("button[mat-raised-button].btn-brand-orange.focusButton") ||
                  Array.from(document.querySelectorAll("button")).find(b =>
                      b.textContent.trim().match(/Iniciar Agendamento|Start New Booking/));
        if (btn) { btn.click(); setTimeout(selecionarDadosIniciais, 2000); }
    }

    function selecionarDadosIniciais() {
        selecionarOpcao("mat-select[formcontrolname='centerCode']", null, 0);
        selecionarOpcao("mat-select[formcontrolname='visaType']", null,
            opt => /Visto Nacional|National visa/.test(opt.textContent));
        selecionarOpcao("mat-select[formcontrolname='visaCategoryCode']", null, 0);
        setTimeout(() => clicarBotaoText('Continuar'), 2000);
    }

    function preencherFormulario(cliente) {
        document.querySelectorAll("input, select").forEach(el => el.removeAttribute("autocomplete"));
        const map = {
            firstName: ["input[name='firstName']","input[placeholder*='first name']"],
            lastName: ["input[name='lastName']","input[placeholder*='last name']"],
            birthDate: ["input[name='birthDate']","input[placeholder*='date']"],
            passportNumber: ["input[name='passportNumber']","input[placeholder*='passport']"],
            passportExpiration: ["input[name='passportExpiration']","input[placeholder*='DD/MM/YYYY']"],
            phone: ["input[name='phone']","input[placeholder*='phone']"],
            email: ["input[name='email']"],
            codigoPais: ["input[name='countryCode']"]
        };
        Object.keys(map).forEach(c => preencherCampo(map[c], cliente[c]));
        selecionarDropdown("select[name='nationality']", cliente.nationality);
        selecionarDropdown("mat-select[formcontrolname='gender']", cliente.genero);
        setTimeout(() => clicarBotaoText('Guardar') || clicarBotaoText('Save'), 2000);
    }

    // ... demais funções selecionarSubCategoriaEAgendamento, selecionarOpcao, preencherCampo, selecionarDropdown,
    // clicarBotaoText, manterSessaoAtiva, addFloatingControl, addProfileSidebar conforme script original

    /********************* Execução inicial *********************/
    fetchClientes();
})();
