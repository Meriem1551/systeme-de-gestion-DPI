import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { RecherchePatientComponent } from './recherche-patient/recherche-patient.component';
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RecherchePatientComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
}
