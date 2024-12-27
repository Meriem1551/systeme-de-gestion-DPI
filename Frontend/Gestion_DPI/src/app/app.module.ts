import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app.component';  // Standalone Component
import { PageInfirmierComponent } from './page-infirmier/page-infirmier.component';
import { PatientSelectionComponent } from './patient-selection/patient-selection.component';
import { SoinFormComponent } from './soin-form/soin-form.component';

// This is the new approach with standalone components
bootstrapApplication(AppComponent, {
  providers: [
    // You can add global providers here, if necessary
  ]
});
