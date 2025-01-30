import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../header-component/header.component';
import { PatientSelectionComponent } from '../patient-selection/patient-selection.component';
import { SoinFormComponent } from '../soin-form/soin-form.component';
import { Soin } from '../models/soin.model';
import { HttpClient } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-page-infirmier',
  imports: [HeaderComponent, PatientSelectionComponent, SoinFormComponent, CommonModule],
  templateUrl: './page-infirmier.component.html',
  styleUrls: ['./page-infirmier.component.css']
})
export class PageInfirmierComponent {
  userId: number | null = null; // ID de l'infirmier récupéré des query params
  patientSelected: number | null = null; // ID du patient sélectionné
  soins: Soin[] = []; // Liste des soins à enregistrer

  showModal: boolean = false;
  modalMessage: string = '';

  apiUrl: string = 'http://127.0.0.1:8000/api/miseajourdpi/remplirSoin/';

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit(): void {
    // Get the `id` query parameter directly
    this.route.queryParams.subscribe(params => {
      this.userId = +params['id'] || null;
      console.log('User ID:', this.userId);
    });
  }

  // Méthode appelée lorsque le patient est sélectionné
  onPatientSelected(patientId: number): void {
    this.patientSelected = patientId;
    this.soins = [];
  }

  addSoin(): void {
    this.soins.push({ description: '', observation: '' });
  }

  updateSoinData(updatedSoin: { description: string; observation: string }, index: number): void {
    this.soins[index].description = updatedSoin.description;
    this.soins[index].observation = updatedSoin.observation;
  }

  deleteSoin(index: number): void {
    this.soins.splice(index, 1);
  }

  cancel(): void {
    this.patientSelected = null;
    this.soins = [];
    this.modalMessage = 'Soins annulés!';
    this.showModal = true;
  }

  save(): void {
    // Check if all soins have both description and observation filled
    const isValid = this.soins.every(soin => soin.description.trim() !== '' && soin.observation.trim() !== '');
  
    if (!isValid) {
      this.modalMessage = 'Veuillez remplir tous les soins avant d\'enregistrer.';
      this.showModal = true;
      return;
    }
  
    if (this.soins.length === 0) {
      this.modalMessage = 'Aucun soin à enregistrer.';
      this.showModal = true;
      return;
    }
  
    if (!this.patientSelected) {
      this.modalMessage = 'Veuillez sélectionner un patient avant de sauvegarder.';
      this.showModal = true;
      return;
    }
  
    // Save each soin one by one
    this.soins.forEach((soin, index) => {
      const soinData = {
        patient: this.patientSelected,
        user: this.userId, // send user id to backend so it can fetch infirmier id
        description: soin.description,
        observation: soin.observation
      };
  
      this.http.post(this.apiUrl, soinData)
        .pipe(
          catchError(error => {
            console.error(`Erreur lors de l’enregistrement du soin ${index + 1}:`, error);
            alert(`Erreur lors de l’enregistrement du soin ${index + 1}`);
            return of(null); // Return an observable to allow the loop to continue
          })
        )
        .subscribe(response => {
          console.log(`Soin ${index + 1} enregistré avec succès:`, response);
        });
    });
  
    this.modalMessage = 'Les soins ont été enregistrés avec succès!';
    this.showModal = true;
    this.patientSelected = null;
    this.soins = [];
  }
  

  closeModal() {
    this.showModal = false;
  }
}
