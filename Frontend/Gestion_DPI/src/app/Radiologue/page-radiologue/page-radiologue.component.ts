import { Component } from '@angular/core';
import { HeaderComponent } from '../../header-component/header.component';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { PageRadiologueService } from '../../services/page-radiologue.service';
import { FenetreRadiologueComponent } from '../fenetre-radiologue/fenetre-radiologue.component';

interface patientData {
  email : string ;
  first_name:string;
  id:number ;
  last_name : string ;
}
interface dpiData {
  utilisateur : patientData ;
  id_dpi: number ;
}
interface bilanDatafront {
  id_bilanradiologique : number ;
  consultid : number ;
  type : string ;
  description : string ;
  compteRendu : string ;
}
interface bilanDataBack {
  compte_rendu : string ;
  description : string ;
  id_bilanradiologique : number ;
  type : string ;
  images : imageData[] ;
}
interface bilanData {
  bilan_radiologique : bilanDataBack ;
  consultation_id : number ; 
}
interface imageData {
  id_image:number;
  image:string;
}
@Component({
  selector: 'app-page-radiologue',
  imports: [HeaderComponent,CommonModule,MatTableModule],
  templateUrl: './page-radiologue.component.html',
  styleUrl: './page-radiologue.component.css'
})
export class PageRadiologueComponent {
  dropdownOpen = false;
  selectedValue: { name: string; dpi: number } = { name: '', dpi: Number('') };
  listPatients: { name: string; dpi: number }[] = [];
  dpi : number = 0 ;
  /*listPatients = [
    'Alice Dupont',
    'Jean Martin',
    'Sophie Bernard',
    'Paul Durand',
    'Nicolas Lambert',
    'Claire Rousseau',
    'Hugo Petit'
];*/
displayedColumns: string[] = [ 'Type', 'Description', 'compteRendu'];
dataSource : bilanDatafront[] = [

  //{ date: '2023-12-05', type: 'X-Ray', description: 'Chest X-ray for examination', compteRendu: 'non' },
  //{ date: '2023-12-10', type: 'MRI', description: 'Brain MRI scan', compteRendu: 'oui' }
];

constructor(public dialog : MatDialog , private pageRadiologueService : PageRadiologueService ){} ;

ngOnInit(): void {
  this.dropdownOpen = false;
  // récupérer la liste des patients qui on des bilans rad du backend 
  this.pageRadiologueService.getListPatients().subscribe((data) => {
    console.log("patients Rad ",data);
    data.forEach
    ((dpi : dpiData) => {
     const patient = `${dpi.utilisateur.first_name} ${dpi.utilisateur.last_name}`
     this.listPatients.push({name : patient , dpi : dpi.id_dpi });
    })
    this.dpi = data.id_dpi ;
      console.log("this.listPatients",this.listPatients)
  });
  
}
  toggleDropdown() {
    this.dropdownOpen = !this.dropdownOpen;
  }
   // la fonction qui permet de chargé les bilan d'un patient choisit 
  selectItem(item: { name: string; dpi: number }) {
    this.selectedValue = item;
    this.dropdownOpen = !this.dropdownOpen;
  
    console.log("dpi inside", item.dpi);
  
    // Réinitialiser dataSource au début pour éviter l'accumulation
    this.dataSource = []; // Réinitialise avant de charger de nouvelles données.
  
    this.pageRadiologueService.getListBillans(item.dpi).subscribe((data) => {
      console.log("dtabilan", data);
  
      // Préparer la nouvelle liste
      const newDataSource = data.map((element: bilanData) => {
        const consult_id = element.consultation_id;
        let cr = (element.bilan_radiologique.compte_rendu === '' && element.bilan_radiologique.images.length === 0) 
                 ? 'non' 
                 : 'oui';
  
        return {
          consultid: consult_id,
          type: element.bilan_radiologique.type,
          description: element.bilan_radiologique.description,
          compteRendu: cr,
          id_bilanradiologique : element.bilan_radiologique.id_bilanradiologique,          
        };
      });
  
      // Mettre à jour dataSource avec une nouvelle instance
      this.dataSource = [...newDataSource]; // Remplacer par une copie pour déclencher le changement.
      console.log("this.dataSource", this.dataSource); // Vérification des données chargées
    });
  }
  
      // ouvrir la fenetre du radiologue 
        openRedactionCompteRendu(element: any): void {
          const dialogRef = this.dialog.open(FenetreRadiologueComponent, {
            width: '85%',
            height: '90%',
            data: { element } // Envoie l'élément à modifier dans la fenêtre modale
          });
      
          // Récupère la valeur "oui" après la fermeture de la fenêtre modale
          dialogRef.afterClosed().subscribe((valeurEnvoyee: string) => {
            if (valeurEnvoyee) {
              this.enregistrer(valeurEnvoyee, element.consultid ); // Met à jour l'élément avec la valeur envoyée
            }
          });
        }
      
        // Met à jour l'élément dans le tableau avec la valeur reçue
        enregistrer(valeur: string, id_consult: number) {
          const index = this.dataSource.findIndex(item => item.consultid === id_consult);
          if (index !== -1) {
            this.dataSource[index].compteRendu = valeur; // Met à jour la valeur de "compteRendu"
          }
        }
}
