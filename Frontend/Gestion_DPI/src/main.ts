import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';  // Import BrowserAnimationsModule
import { importProvidersFrom } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { provideRouter } from '@angular/router';
import { routes } from '../src/app/app.routes';
import { provideHttpClient } from '@angular/common/http';



// Modify the bootstrapApplication to include BrowserAnimationsModule
bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    importProvidersFrom(
      BrowserAnimationsModule,  // Enable animations
      FormsModule,
      ReactiveFormsModule,
      MatFormFieldModule,
      MatSelectModule,
    ),    
  ],
}).catch((err) => console.error(err));

