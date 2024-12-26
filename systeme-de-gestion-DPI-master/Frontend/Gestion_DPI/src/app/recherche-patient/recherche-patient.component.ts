import { Component } from '@angular/core';
import { HeaderComponent } from '../header-component/header.component';
import {MatTableModule} from '@angular/material/table';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
export interface PeriodicElement {
  NSS: number;
  Nom: string;
  Prenom: string;
}
const ELEMENT_DATA: PeriodicElement[] = [
  {NSS: 1, Nom: 'Hydrogen', Prenom: 'Meriem' },
  {NSS: 2, Nom: 'Helium', Prenom:'Meriem'},
  {NSS: 3, Nom: 'Lithium', Prenom:'Meriem'},
  {NSS: 4, Nom: 'Beryllium', Prenom: 'Meriem'},
  {NSS: 5, Nom: 'Boron', Prenom: 'Meriem' },
  {NSS: 6, Nom: 'Carbon', Prenom:'Meriem'},
  {NSS: 7, Nom: 'Nitrogen', Prenom:'Meriem'},
  {NSS: 8, Nom: 'Oxygen', Prenom: 'Meriem'},
  {NSS: 9, Nom: 'Fluorine', Prenom: 'Meriem'},
  {NSS: 10, Nom: 'Neon', Prenom: 'Meriem'},
];

@Component({
  selector: 'app-recherche-patient',
  imports: [HeaderComponent, MatTableModule, CommonModule],
  templateUrl: './recherche-patient.component.html',
  styleUrl: './recherche-patient.component.css'
})
export class RecherchePatientComponent {
  displayedColumns: string[] = ['NSS', 'Nom', 'Prenom'];
  dataSource = ELEMENT_DATA;

  search(){
    console.log('search...');
  }
}
