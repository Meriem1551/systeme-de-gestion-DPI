'use strict';

customElements.define('compodoc-menu', class extends HTMLElement {
    constructor() {
        super();
        this.isNormalMode = this.getAttribute('mode') === 'normal';
    }

    connectedCallback() {
        this.render(this.isNormalMode);
    }

    render(isNormalMode) {
        let tp = lithtml.html(`
        <nav>
            <ul class="list">
                <li class="title">
                    <a href="index.html" data-type="index-link">gestion-dpi documentation</a>
                </li>

                <li class="divider"></li>
                ${ isNormalMode ? `<div id="book-search-input" role="search"><input type="text" placeholder="Type to search"></div>` : '' }
                <li class="chapter">
                    <a data-type="chapter-link" href="index.html"><span class="icon ion-ios-home"></span>Getting started</a>
                    <ul class="links">
                        <li class="link">
                            <a href="overview.html" data-type="chapter-link">
                                <span class="icon ion-ios-keypad"></span>Overview
                            </a>
                        </li>
                        <li class="link">
                            <a href="index.html" data-type="chapter-link">
                                <span class="icon ion-ios-paper"></span>README
                            </a>
                        </li>
                                <li class="link">
                                    <a href="dependencies.html" data-type="chapter-link">
                                        <span class="icon ion-ios-list"></span>Dependencies
                                    </a>
                                </li>
                                <li class="link">
                                    <a href="properties.html" data-type="chapter-link">
                                        <span class="icon ion-ios-apps"></span>Properties
                                    </a>
                                </li>
                    </ul>
                </li>
                    <li class="chapter modules">
                        <a data-type="chapter-link" href="modules.html">
                            <div class="menu-toggler linked" data-bs-toggle="collapse" ${ isNormalMode ?
                                'data-bs-target="#modules-links"' : 'data-bs-target="#xs-modules-links"' }>
                                <span class="icon ion-ios-archive"></span>
                                <span class="link-name">Modules</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                        </a>
                        <ul class="links collapse " ${ isNormalMode ? 'id="modules-links"' : 'id="xs-modules-links"' }>
                            <li class="link">
                                <a href="modules/AppModule.html" data-type="entity-link" >AppModule</a>
                            </li>
                            <li class="link">
                                <a href="modules/AppRoutingModule.html" data-type="entity-link" >AppRoutingModule</a>
                            </li>
                </ul>
                </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#components-links"' :
                            'data-bs-target="#xs-components-links"' }>
                            <span class="icon ion-md-cog"></span>
                            <span>Components</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="components-links"' : 'id="xs-components-links"' }>
                            <li class="link">
                                <a href="components/AppComponent.html" data-type="entity-link" >AppComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/BilanBiologiqueComponent.html" data-type="entity-link" >BilanBiologiqueComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/BilanBiologiqueComponent-1.html" data-type="entity-link" >BilanBiologiqueComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/BilanRadiologiqueComponent.html" data-type="entity-link" >BilanRadiologiqueComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/BilanRadiologiqueComponent-1.html" data-type="entity-link" >BilanRadiologiqueComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ConsultationHomeComponent.html" data-type="entity-link" >ConsultationHomeComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ConsulterDpiComponent.html" data-type="entity-link" >ConsulterDpiComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/CreationDPIComponent.html" data-type="entity-link" >CreationDPIComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/FenetreRadiologueComponent.html" data-type="entity-link" >FenetreRadiologueComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/GenererGraphe.html" data-type="entity-link" >GenererGraphe</a>
                            </li>
                            <li class="link">
                                <a href="components/HeaderComponent.html" data-type="entity-link" >HeaderComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/HeaderComponent-1.html" data-type="entity-link" >HeaderComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/LandingPageComponent.html" data-type="entity-link" >LandingPageComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/LoginComponent.html" data-type="entity-link" >LoginComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/MainHeaderComponent.html" data-type="entity-link" >MainHeaderComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/OrdonnanceComponent.html" data-type="entity-link" >OrdonnanceComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/OrdonnanceComponent-1.html" data-type="entity-link" >OrdonnanceComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/PageInfirmierComponent.html" data-type="entity-link" >PageInfirmierComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/PageLaborantinComponent.html" data-type="entity-link" >PageLaborantinComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/PageRadiologueComponent.html" data-type="entity-link" >PageRadiologueComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/PatientSelectionComponent.html" data-type="entity-link" >PatientSelectionComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/RecherchePatientComponent.html" data-type="entity-link" >RecherchePatientComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/RemplirResultat.html" data-type="entity-link" >RemplirResultat</a>
                            </li>
                            <li class="link">
                                <a href="components/ResumeComponent.html" data-type="entity-link" >ResumeComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ResumeComponent-1.html" data-type="entity-link" >ResumeComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SoinFormComponent.html" data-type="entity-link" >SoinFormComponent</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#injectables-links"' :
                                'data-bs-target="#xs-injectables-links"' }>
                                <span class="icon ion-md-arrow-round-down"></span>
                                <span>Injectables</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="injectables-links"' : 'id="xs-injectables-links"' }>
                                <li class="link">
                                    <a href="injectables/ConsultationApiService.html" data-type="entity-link" >ConsultationApiService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ConsultationService.html" data-type="entity-link" >ConsultationService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ConsulterDpiService.html" data-type="entity-link" >ConsulterDpiService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/CreationDPIService.html" data-type="entity-link" >CreationDPIService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/LaborantinService.html" data-type="entity-link" >LaborantinService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/LoginService.html" data-type="entity-link" >LoginService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/PageRadiologueService.html" data-type="entity-link" >PageRadiologueService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/RechercheService.html" data-type="entity-link" >RechercheService</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#interfaces-links"' :
                            'data-bs-target="#xs-interfaces-links"' }>
                            <span class="icon ion-md-information-circle-outline"></span>
                            <span>Interfaces</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? ' id="interfaces-links"' : 'id="xs-interfaces-links"' }>
                            <li class="link">
                                <a href="interfaces/Bilan.html" data-type="entity-link" >Bilan</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/BilanBiologique.html" data-type="entity-link" >BilanBiologique</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/bilanData.html" data-type="entity-link" >bilanData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/bilanDataBack.html" data-type="entity-link" >bilanDataBack</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/bilanDatafront.html" data-type="entity-link" >bilanDatafront</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/BilanRadiologique.html" data-type="entity-link" >BilanRadiologique</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Consultation.html" data-type="entity-link" >Consultation</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ConsultationData.html" data-type="entity-link" >ConsultationData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/dpiData.html" data-type="entity-link" >dpiData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/DpiDetails.html" data-type="entity-link" >DpiDetails</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Graphe.html" data-type="entity-link" >Graphe</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/imageData.html" data-type="entity-link" >imageData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Img.html" data-type="entity-link" >Img</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ListConsultation.html" data-type="entity-link" >ListConsultation</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ListMeds.html" data-type="entity-link" >ListMeds</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ListSoins.html" data-type="entity-link" >ListSoins</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Ordonnance.html" data-type="entity-link" >Ordonnance</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ParametreBioMesure.html" data-type="entity-link" >ParametreBioMesure</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Patient.html" data-type="entity-link" >Patient</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Patient-1.html" data-type="entity-link" >Patient</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/patientData.html" data-type="entity-link" >patientData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Prescription.html" data-type="entity-link" >Prescription</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Resume.html" data-type="entity-link" >Resume</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Soin.html" data-type="entity-link" >Soin</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/SoinsData.html" data-type="entity-link" >SoinsData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ValeursBio.html" data-type="entity-link" >ValeursBio</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#miscellaneous-links"'
                            : 'data-bs-target="#xs-miscellaneous-links"' }>
                            <span class="icon ion-ios-cube"></span>
                            <span>Miscellaneous</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="miscellaneous-links"' : 'id="xs-miscellaneous-links"' }>
                            <li class="link">
                                <a href="miscellaneous/variables.html" data-type="entity-link">Variables</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <a data-type="chapter-link" href="coverage.html"><span class="icon ion-ios-stats"></span>Documentation coverage</a>
                    </li>
                    <li class="divider"></li>
                    <li class="copyright">
                        Documentation generated using <a href="https://compodoc.app/" target="_blank" rel="noopener noreferrer">
                            <img data-src="images/compodoc-vectorise.png" class="img-responsive" data-type="compodoc-logo">
                        </a>
                    </li>
            </ul>
        </nav>
        `);
        this.innerHTML = tp.strings;
    }
});