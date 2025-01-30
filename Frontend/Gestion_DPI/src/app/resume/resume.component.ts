import { Component } from '@angular/core';
import { ConsultationService } from '../services/consultation.service';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from '../header-component/header.component';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Resume } from '../models/consultation.model';
@Component({
  selector: 'app-resume',
  templateUrl: './resume.component.html',
  imports: [HeaderComponent, FormsModule, CommonModule],
  styleUrls: ['./resume.component.css']
})

export class ResumeComponent {
  resume : Resume ;

  showModal: boolean = false; // Contrôle la visibilité de la fenêtre modale
  modalMessage: string = ''; // Message à afficher dans la modale

  constructor(private consultationService: ConsultationService, private router: Router) {
    this.resume = this.consultationService.getConsultation().resume;
  }

  saveResume() {
    const emptyFields: string[] = [];

    // Vérifie quels champs sont vides
    if (!this.resume.diagnostic.trim()) emptyFields.push('Diagnostic');
    if (!this.resume.symptomes.trim()) emptyFields.push('Symptômes');
    if (!this.resume.antecedents.trim()) emptyFields.push('Antécédents');

    if (emptyFields.length > 0) {
      const fieldMessage =
        emptyFields.length === 1
          ? `Le champ suivant est vide : ${emptyFields.join(', ')}. Veuillez le remplir avant d'enregistrer le résumé.`
          : `Les champs suivants sont vides : ${emptyFields.join(', ')}. Veuillez les remplir avant d'enregistrer le résumé.`;

      this.modalMessage = fieldMessage; // Mettre à jour le message de la modale
      this.showModal = true; // Afficher la modale
    } else {
      this.consultationService.updateConsultation('resume', this.resume);
      this.modalMessage = 'Le résumé a été enregistré avec succès !';
      this.showModal = true ;
      this.router.navigate(['/creation-consult']);
    }
  }

  closeModal() {
    this.showModal = false; // Fermer la modale
  }

  cancel() {
    this.router.navigate(['/creation-consult']);
  }
}
