import { Component , OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatTableModule} from '@angular/material/table';
import { HeaderComponent } from '../../header-component/header.component';
import {OrdonnanceComponent} from '../ordonnance/ordonnance.component';
import { ResumeComponent } from '../resume/resume.component';
import { MatDialog } from '@angular/material/dialog';
import {ConsulterDpiService ,ListConsultation, ListSoins , DpiDetails} from '../../services/consulter-dpi.service'
import { BilanBiologiqueComponent } from '../bilan-biologique/bilan-biologique.component';
import { BilanRadiologiqueComponent } from '../bilan-radiologique/bilan-radiologique.component';

import { ActivatedRoute ,Router ,RouterModule} from '@angular/router';

@Component({
  selector: 'app-consulter-dpi',
  imports: [CommonModule,MatTableModule,HeaderComponent,RouterModule],
  templateUrl:'./consulter-dpi.component.html' ,
  styleUrl: './consulter-dpi.component.css',
  standalone: true
})
export class ConsulterDpiComponent implements OnInit{

  displayedColumns: string[] = [ 'NConsultation','date', 'Ordo', 'Bilan_bio','Bilan_rad','Resume'];
  dataSource : ListConsultation[] = [];
  displayedColumns2: string[] = ['Date','Description','Observation'];
  dataSource2 : ListSoins[] = [];
  showButton = true ;
  dpiDetails: DpiDetails ={
    nss: '',
    nom_patient: '',
    prenom_patient: '',
    date_de_naissance: '', // You can use `Date` type if you need a Date object instead of string
    adresse: '',
    telephone: '',
    mutuelle: '',
    personne_a_contacter: '',
    nom_complet_medecin: '',
    id_dpi: '',
  };
  id!: string;
  role: string | null = '';
  currentUrl: string = '';
  constructor(private router: Router,public dialog : MatDialog , private consulterDpiService : ConsulterDpiService ,private route: ActivatedRoute, ){} ;
 
  getConsultationNumber(index: number): number {
    return index + 1; // Incrémentation à partir de 1
  }
  getdpi():number{
    return Number(this.dpiDetails?.id_dpi);
  }
   // Récupérer l'URL actuelle
   getCurrentUrl(): void {
    this.router.events.subscribe(() => {
      this.currentUrl = this.router.url;
      console.log('URL actuelle:', this.currentUrl); // Affiche l'URL dans la console
    });
  }
    
ngOnInit(): void {
  // Extract the 'id' parameter from the route
  this.id = this.route.snapshot.paramMap.get('id')!;
  console.log('Patient ID:', this.id);

  // Appel pour récupérer les détails du DPI
  this.consulterDpiService.getDpiDetails(this.id).subscribe((response: DpiDetails) => {
    this.dpiDetails = response;
    console.log("Détails du patient récupérés:", this.dpiDetails);
    
    // Appeler ici les autres fonctions après avoir récupéré dpiDetails
    this.loadConsultations();
    this.loadSoins();
    this.getCurrentUrl();

    // Écoutez les changements du fragment d'URL
    this.route.fragment.subscribe(fragment => {
      // Si un fragment est présent, effectuez le défilement vers l'élément correspondant
      if (fragment) {
        this.scrollToFragment(fragment);
      }
    });
  });
  

  // Récupérer le rôle de l'utilisateur
  this.role = this.route.snapshot.paramMap.get('role')!;
  console.log('Role:', this.role);
  if (this.role === 'patient') {
    this.showButton = false; // Afficher le bouton si l'utilisateur est médecin
  } else {
    this.showButton = true; // Sinon, ne pas afficher le bouton
  }
}
 // Fonction pour faire défiler la page vers l'élément avec l'id donné
 scrollToFragment(fragment: string): void {
  const element = document.getElementById(fragment);
  if (element) {
    // Faites défiler la page vers l'élément
    element.scrollIntoView({ behavior: 'smooth' });
  }
}
// la récupération du tableau des consultations 
loadConsultations() {
  const dpi = Number(this.dpiDetails?.id_dpi);
  console.log("DPI de la consultation:", dpi);
  
  // Effectuer l'appel pour récupérer les consultations
  this.consulterDpiService.getListConsultation(dpi).subscribe(data => {
    this.dataSource = data;
    console.log("consultData",data);
  }, error => {
    console.error('Erreur lors de la récupération des consultations:', error);
  });
}
// la récupération du tableau des soins infirmiers  
loadSoins() {
  const dpi = Number(this.dpiDetails?.id_dpi);
  console.log("DPI des soins:", dpi);
  
  // Effectuer l'appel pour récupérer les soins
  this.consulterDpiService.getListSoins(dpi).subscribe(data => {
    this.dataSource2 = data;
  }, error => {
    console.error('Erreur lors de la récupération des soins:', error);
  });
}
// navigation vers la page de l'ajout de la création du consultation 
navigateToCreationDpi(): void {
  this.router.navigate(['/creation-consult'], { queryParams: { nss: this.dpiDetails.nss } });
}

// ouvrir la fenetre du résumé 
  openOrdonnance(idConsult: number): void {
    this.dialog.open(OrdonnanceComponent, {
      width: '85%',
      height:'90%',
      data: { id_consult: idConsult }
    });
  }
  
  openResume(idConsult: number): void {
    console.log("idConsult",idConsult)
    const dialogRef = this.dialog.open(ResumeComponent, {
      width: '85%',
      height: '90%',
      data: { id_consult: idConsult } // Passer ID de la consultation vers la fenetre ordonnance 
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Data received from modal:', result);
      } else {
        console.log('Modal closed without data.');
      }
    });
  }
  openBilanBio(idConsult: number): void {
    this.dialog.open(BilanBiologiqueComponent, {
      width: '85%',
      height:'90%',
      data: { id_consult: idConsult }
    });
  }
  openBilanRad(idConsult: number): void {
    this.dialog.open(BilanRadiologiqueComponent, {
      width: '85%',
      height:'90%',
      data: { id_consult: idConsult }
    });
  }
}
