import { Component } from '@angular/core';
import { HeaderComponent } from '../../header-component/header.component';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { FenetreRadiologueComponent } from '../fenetre-radiologue/fenetre-radiologue.component';

@Component({
  selector: 'app-page-radiologue',
  imports: [HeaderComponent,CommonModule,MatTableModule],
  templateUrl: './page-radiologue.component.html',
  styleUrl: './page-radiologue.component.css'
})
export class PageRadiologueComponent {
  dropdownOpen = false;
  selectedValue: string | null = null;
  listPatients = [
    'Alice Dupont',
    'Jean Martin',
    'Sophie Bernard',
    'Paul Durand',
    'Nicolas Lambert',
    'Claire Rousseau',
    'Hugo Petit'
];
displayedColumns: string[] = ['Date', 'Type', 'Description', 'compteRendu'];
dataSource = [
  { date: '2023-12-01', type: 'Blood Test', description: 'Routine blood analysis', compteRendu: 'oui' },
  { date: '2023-12-05', type: 'X-Ray', description: 'Chest X-ray for examination', compteRendu: 'non' },
  { date: '2023-12-10', type: 'MRI', description: 'Brain MRI scan', compteRendu: 'oui' }
];

constructor(public dialog : MatDialog){} ;
  toggleDropdown() {
    this.dropdownOpen = !this.dropdownOpen;
  }

  selectItem(item: string) {
    this.selectedValue = item;
   // this.dropdownOpen = false;
   this.dropdownOpen = !this.dropdownOpen;
  }
 /* openRedactionCompteRendu(): void {
      
        this.dialog.open(FenetreRadiologueComponent, {
          width: '85%',
          height:'90%',
        });
    
  }*/
        openRedactionCompteRendu(element: any): void {
          const dialogRef = this.dialog.open(FenetreRadiologueComponent, {
            width: '85%',
            height: '90%',
            data: { element } // Envoie l'élément à modifier dans la fenêtre modale
          });
      
          // Récupère la valeur "oui" après la fermeture de la fenêtre modale
          dialogRef.afterClosed().subscribe((valeurEnvoyee: string) => {
            if (valeurEnvoyee) {
              this.enregistrer(valeurEnvoyee, element.date); // Met à jour l'élément avec la valeur envoyée
            }
          });
        }
      
        // Met à jour l'élément dans le tableau avec la valeur reçue
        enregistrer(valeur: string, date: string) {
          const index = this.dataSource.findIndex(item => item.date === date);
          if (index !== -1) {
            this.dataSource[index].compteRendu = valeur; // Met à jour la valeur de "compteRendu"
          }
        }
}
