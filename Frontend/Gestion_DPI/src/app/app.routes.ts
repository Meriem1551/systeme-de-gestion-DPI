import { Routes } from '@angular/router';
import { BilanRadiologiqueComponent } from './bilan-radiologique/bilan-radiologique.component';
import { OrdonnanceComponent } from './ordonnance/ordonnance.component';
import { BilanBiologiqueComponent } from './bilan-biologique/bilan-biologique.component';
import { ResumeComponent } from './resume/resume.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { LoginComponent } from './login/login.component';
import { RecherchePatientComponent } from './recherche-patient/recherche-patient.component';

import { ConsultationHomeComponent } from './consultation-home/consultation-home.component';
import { CreationDPIComponent } from './creation-dpi/creation-dpi.component';
import { ConsulterDpiComponent } from './ConsultationDPI/consulter-dpi/consulter-dpi.component';
import { PageRadiologueComponent } from './Radiologue/page-radiologue/page-radiologue.component';


import { PageInfirmierComponent } from './page-infirmier/page-infirmier.component';
import { PageLaborantinComponent } from './page-laborantin/page-laborantin.component';

export const routes: Routes = [
    { path: 'ordonnance', component: OrdonnanceComponent },
    { path: 'bilan-radiologique', component: BilanRadiologiqueComponent },
    { path: 'bilan-biologique', component: BilanBiologiqueComponent },
    { path: 'resume', component: ResumeComponent },
    { path: '', component: LandingPageComponent},
    { path: 'login', component: LoginComponent },
    { path: 'recherche-patient', component: RecherchePatientComponent },
    { path: 'creation-dpi', component: CreationDPIComponent},
    { path : 'creation-consult', component : ConsultationHomeComponent},
    { path : 'soins-infirmiers', component : PageInfirmierComponent},
    { path: 'consulter-dpi/:id/:role',component: ConsulterDpiComponent},
    { path:'page-radiologue' , component: PageRadiologueComponent},
    { path:'page-laborantin' , component: PageLaborantinComponent}
];

   



