import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ConsultationHomeComponent } from './consultation-home/consultation-home.component';
import { ResumeComponent } from './resume/resume.component';
import { OrdonnanceComponent } from './ordonnance/ordonnance.component';
import { BilanBiologiqueComponent } from './bilan-biologique/bilan-biologique.component';
import { BilanRadiologiqueComponent } from './bilan-radiologique/bilan-radiologique.component';
import { PageRadiologueComponent } from './Radiologue/page-radiologue/page-radiologue.component';
import { PageLaborantinComponent } from './page-laborantin/page-laborantin.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  { path: '', component: LandingPageComponent},
  { path: 'login', component: LoginComponent },
  { path: 'resume', component: ResumeComponent },
  { path: 'ordonnance', component: OrdonnanceComponent },
  { path: 'bilan-biologique', component: BilanBiologiqueComponent },
  { path: 'bilan-radiologique', component: BilanRadiologiqueComponent },
  { path: 'creation-consult', component: ConsultationHomeComponent },
  {path:'page-radiologue' , component: PageRadiologueComponent},
  {path:'page-laborantin' , component: PageLaborantinComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }