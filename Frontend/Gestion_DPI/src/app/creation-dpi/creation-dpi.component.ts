import { Component } from '@angular/core';
import { HeaderComponent } from "../header-component/header.component";

@Component({
  selector: 'app-creation-dpi',
  imports: [HeaderComponent],
  templateUrl: './creation-dpi.component.html',
  styleUrl: './creation-dpi.component.css'
})
export class CreationDPIComponent {
title="Creation du DPI";
labels = ["Nom", "Prenom", "Numero de securité sociale", "Date de naissance", "Adresse", "Téléphone", "Mutuelle", "Medecin traitant", "Personne a contacter"];
buttons = ["Ajouter le DPI", "Annuler"]
names = ["nom", "prenom", "nss", "ddn", "adresse", "tel", "mutuelle", "medecin", "contacte"];
}
