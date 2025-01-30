import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../header-component/header.component';
import {MatTableModule} from '@angular/material/table';
import { CommonModule } from '@angular/common';
import {Router,RouterLink, RouterLinkActive } from '@angular/router';
import { RechercheService } from '../recherche.service';

import { FormsModule } from '@angular/forms'; 
interface Patient{
  id: number;
  NSS: number;
  Nom:string;
  Prenom:string;
}

@Component({
  selector: 'app-recherche-patient',
  imports: [HeaderComponent, MatTableModule, CommonModule, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './recherche-patient.component.html',
  styleUrl: './recherche-patient.component.css'
})
export class RecherchePatientComponent implements OnInit{
  displayedColumns: string[] = ['NSS', 'Nom', 'Prenom'];
  dataSource :Patient[] = [];
  searchValue: string = '';
  selectedFile: File | null = null;

  constructor(private rechercheService: RechercheService, private router: Router) {}

  ngOnInit(): void {
    this.loadDpiList();
  }
  loadDpiList(): void {
    this.rechercheService.getDpiList().subscribe({
      next: (data) => {
        this.dataSource = data.map((item: any) => ({
          id: item.id,
          NSS: item.nss,
          Nom: item.nom_patient,
          Prenom: item.prenom_patient,
        }));
      },
      error: (err) => {
        console.error('Error fetching DPI list:', err);
      }
  });
  }

  onRowClick(row: any): void {
    this.router.navigate(['/consulter-dpi', row.id,'medecin']);

  }

  search(){
    if (!this.searchValue.trim()) {
      alert('Please enter a valid NSS.');
      return;
    }

    this.rechercheService.searchDpiByNss(this.searchValue).subscribe({
      next: (data) => {
        this.dataSource = [{
          id: data.id,

          NSS: parseInt(data.nss, 10),
          Nom: data.nom_patient,
          Prenom: data.prenom_patient,
        }];
      },
      error: (err) => {
        console.error('Search failed', err);
        alert('Erreur: NSS invalide');
      }
  });
  }
  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  scanQRCode(): void {
    if (!this.selectedFile) {
      alert('Veuillez sélectionner un fichier avant de scanner.');
      return;
    }

    this.rechercheService.scanQRCode(this.selectedFile).subscribe({
      next: (response: any) => {
        console.log(response);
        const patientData = {
          id: response.id,
          NSS: response.nss,
          Nom: response.nom_patient,
          Prenom: response.prenom_patient,
        };
        this.dataSource = [patientData];
      },
      error: (error) => {
        console.error(error);
        alert('Erreur lors du scan du QR code.');
      }
    });
  }


}

