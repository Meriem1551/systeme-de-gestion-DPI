import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import {  Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ConsulterDpiService } from '../../services/consulter-dpi.service';



@Component({
  selector: 'app-resume',
  imports: [MatDialogContent ,
              MatDialogActions,
              MatDialogClose , 
              MatDialogTitle ,
              CommonModule,
            ],
  templateUrl: './resume.component.html',
  styleUrl: './resume.component.css'
})
export class ResumeComponent {
  Symptomes = "Symptomes";
  Diagnostic="Diagnostic";
  Antecedents="Antécédents";
  autres="autres";

  constructor(
    public dialogRef: MatDialogRef<ResumeComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, // Injected data
    private consulterDpiService: ConsulterDpiService // Service for API calls
  ) {}
  // requete pour la récupération du résumé 
   ngOnInit(): void {
    const id_consult = this.data.id_consult; // par le DPI du patient
      this.consulterDpiService.getResume(id_consult).subscribe(data => {
       console.log(data);
       this.Antecedents = data.antecedents ;
       this.Diagnostic = data.diagnostic;
       this.Symptomes = data.symptomes ;
       this.autres = data.autres_informations ;
    }, error => {
      console.error('Erreur lors de la récupération du résumé :', error);
    });
  }

 
}
